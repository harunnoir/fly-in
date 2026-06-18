from enum import Enum
from pydantic import BaseModel
from pathlib import Path


class ParsingError(Exception):
    """Base exception for all parsing errors, includes line number."""

    def __init__(self, line: int, message: str) -> None:
        """Initialize with line number and error message.

        Args:
            line: The line number where the error occurred.
            message: A description of the parsing error.
        """
        super().__init__(f"Line {line}: {message}")


class ZoneType(Enum):
    """Enum representing the type of a zone."""

    NORMAL = "normal"
    BLOCKED = "blocked"
    RESTRICTED = "restricted"
    PRIORITY = "priority"


class Zone(BaseModel):
    """Represents a zone/hub in the drone network."""

    name: str
    x: int
    y: int
    zone_type: ZoneType = ZoneType.NORMAL
    color: str | None = None
    max_drones: int = 1


class Connection(BaseModel):
    """Represents a bidirectional connection between two zones."""

    zone1: str
    zone2: str
    max_link_capacity: int = 1


class Graph(BaseModel):
    """Represents the full drone network graph."""

    nb_drones: int
    start_hub: Zone
    end_hub: Zone
    zones: dict[str, Zone] = {}
    connections: list[Connection] = []


class MapParser:
    """Parses a map file and builds a Graph object."""

    _filepath: Path

    def __init__(self, filepath: str) -> None:
        self._filepath = Path(filepath)

        if not self._filepath.exists():
            raise ParsingError(0, f"Map file '{self._filepath}' not found")

        if self._filepath.suffix != ".txt":
            raise ParsingError(
                0, f"Expected .txt file, got '{self._filepath.suffix}'"
            )

    def __remove_comments(self, map_data: str) -> str:
        return "\n".join(
            line.split("#", 1)[0].strip()
            for line in map_data.splitlines()
            if line.split("#", 1)[0].strip()
        )

    def __parse_hub(self, line: str, zones: dict[str, Zone]) -> Zone:
        parts = line.split()
        name = parts[0]
        x = int(parts[1])
        y = int(parts[2])
        zone_type = ZoneType.NORMAL
        color = None
        max_drones = 1
        meta_str = " ".join(parts[3:])
        if meta_str:
            for kv in meta_str.strip("[]").split():
                key, val = kv.split("=", 1)
                if key == "zone":
                    zone_type = ZoneType(val)
                elif key == "color":
                    color = val
                elif key == "max_drones":
                    max_drones = int(val)
                else:
                    raise ValueError(f"Unknown metadata key '{key}'")
        if name in zones:
            raise ValueError(f"Zone '{name}' already exists")
        if any(z.x == x and z.y == y for z in zones.values()):
            raise ValueError(f"Zone at coordinates ({x}, {y}) already exists")
        return Zone(
            name=name,
            x=x,
            y=y,
            zone_type=zone_type,
            color=color,
            max_drones=max_drones,
        )

    def __parse_connection(self, line: str) -> Connection:
        content = line.removeprefix("connection:").strip()
        parts = content.split()

        zone1, zone2 = parts[0].split("-", 1)

        capacity = 1
        if len(parts) > 1:
            meta = parts[1][1:-1]  # remove [ ]
            capacity = int(meta.split("=", 1)[1])

        return Connection(
            zone1=zone1,
            zone2=zone2,
            max_link_capacity=capacity,
        )

    def parse(self) -> Graph:
        lines = self.__remove_comments(self._filepath.read_text()).splitlines()
        if not lines:
            raise ValueError("Map file is empty")
        nb_drones: int | None = None
        zones: dict[str, Zone] = {}
        connections: list[Connection] = []

        if lines[0].startswith("nb_drones:"):
            try:
                nb_drones = int(lines[0][len("nb_drones:") :].strip())
            except (ValueError, IndexError) as e:
                raise ValueError(
                    f"Invalid nb_drones value or format in the map file: {e}"
                )
            if nb_drones < 1:
                raise ValueError("nb_drones must be at least 1")
        else:
            raise ValueError(
                "File should start with the number of drones first"
            )
        for line in lines[1:]:
            if (
                line.startswith("start_hub:")
                or line.startswith("end_hub:")
                or line.startswith("hub:")
            ):
                hub = self.__parse_hub(line, zones)
                zones[hub.name] = hub

            elif line.startswith("connection:"):
                connections.append(self.__parse_connection(line))

            else:
                raise ValueError(f"Unrecognized line: {line}")

        if "start" not in zones:
            raise ValueError(
                "start_hub is required but was not found in the map file"
            )
        if "goal" not in zones:
            raise ValueError(
                "end_hub is required but was not found in the map file"
            )

        return Graph(
            nb_drones=nb_drones,
            start_hub=zones["start_hub"],
            end_hub=zones["end_hub"],
            zones=zones,
            connections=connections,
        )
