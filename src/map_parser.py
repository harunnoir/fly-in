from __future__ import annotations
from enum import Enum
from pydantic import BaseModel, model_validator, Field
from pathlib import Path


class ParsingError(Exception):
    """Base exception for all parsing errors, includes optional line number."""

    def __init__(self, message: str, line: int | None = None) -> None:
        """Initialize with error message and optional line number.

        Args:
            message: A description of the parsing error.
            line: The line number where the error occurred, if applicable.
        """
        super().__init__(f"Line {line}: {message}" if line else message)


class ZoneType(Enum):
    """Enum representing the type of a zone."""

    NORMAL = "normal"
    BLOCKED = "blocked"
    RESTRICTED = "restricted"
    PRIORITY = "priority"


class Connection(BaseModel):
    """Represents a bidirectional connection between two zones."""

    zone1: Zone
    zone2: Zone
    max_link_capacity: int = 1
    drones_in_transit: list[str] = []  # Track IDs of drones currently "flying"

    @model_validator(mode="after")
    def validate_connection(self) -> "Connection":
        """Validate all connection constraints."""
        if self.zone1 == self.zone2:
            raise ParsingError(f"Connection cannot link zone '{self.zone1}' to itself")
        if self.max_link_capacity < 1:
            raise ParsingError("max_link_capacity must be a positive integer")
        return self


class Link(BaseModel):
    """A directional shortcut to a neighbor."""

    target: Zone
    connection: Connection


class Zone(BaseModel):
    """Represents a zone/hub in the drone network."""

    name: str
    x: int
    y: int
    zone_type: ZoneType = ZoneType.NORMAL
    color: str | None = None
    max_drones: int = 1
    links: list[Link] = Field(default=[], exclude=True)

    @model_validator(mode="after")
    def validate_zone(self) -> "Zone":
        if "-" in self.name or " " in self.name:
            raise ParsingError(
                f"Zone name '{self.name}' must not contain dashes or spaces"
            )
        if self.max_drones < 1:
            raise ParsingError("max_drones must be a positive integer")
        if self.color is not None and " " in self.color:
            raise ParsingError("color must be a single-word string")
        return self

    def get_travel_cost(self) -> int:
        if self.zone_type == ZoneType.RESTRICTED:
            return 2
        return 1

    def is_accessible(self) -> bool:
        return self.zone_type != ZoneType.BLOCKED


class Graph(BaseModel):
    """Represents the full drone network graph."""

    nb_drones: int
    start_hub: Zone
    end_hub: Zone
    zones: dict[str, Zone] = {}
    connections: list[Connection] = []

    def reset(self) -> None:
        """Clears all drones from zones and connections."""
        for conn in self.connections:
            conn.drones_in_transit.clear()


class MapParser:
    """Parses a map file and builds a Graph object."""

    @staticmethod
    def __load_file(filepath: str) -> Path:
        file = Path(filepath)

        if not file.exists():
            raise ParsingError(f"Map file '{file}' not found")

        if file.suffix != ".txt":
            raise ParsingError(f"Expected .txt file, got '{file}'")
        return file

    @staticmethod
    def __remove_comments(map_data: str) -> str:
        return "\n".join(
            line.split("#", 1)[0].strip()
            for line in map_data.splitlines()
            if line.split("#", 1)[0].strip()
        )

    @staticmethod
    def __parse_hub(line: str, linenb: int, zones: dict[str, Zone]) -> Zone:
        parts = line.split()[1:]
        try:
            name = parts[0]
            x = int(parts[1])
            y = int(parts[2])
        except (IndexError, ValueError) as e:
            raise ParsingError(f"Invalid hub format: {e}", linenb)
        zone_type = ZoneType.NORMAL
        color = None
        max_drones = 1
        meta_str = " ".join(parts[3:])
        if meta_str:
            for kv in meta_str.removeprefix("[").removesuffix("]").split():
                key, val = kv.split("=", 1)
                if key == "zone":
                    try:
                        zone_type = ZoneType(val)
                    except ValueError:
                        raise ParsingError(
                            f"Invalid zone type '{val}', must be one"
                            + "of: normal, blocked, restricted, priority",
                            linenb,
                        )
                elif key == "color":
                    color = val
                elif key == "max_drones":
                    try:
                        max_drones = int(val)
                    except ValueError:
                        raise ParsingError(
                            f"max_drones must be a positive integer, got '{val}'",
                            linenb,
                        )
                else:
                    raise ParsingError(f"Unknown metadata key '{key}'", linenb)
        if name in zones:
            raise ParsingError(f"Zone '{name}' already exists", linenb)
        if any(z.x == x and z.y == y for z in zones.values()):
            raise ParsingError(f"Zone at coordinates ({x}, {y}) already exists", linenb)
        return Zone(
            name=name,
            x=x,
            y=y,
            zone_type=zone_type,
            color=color,
            max_drones=max_drones,
        )

    @staticmethod
    def __parse_connection(
        line: str,
        linenb: int,
        zones: dict[str, Zone],
        connections: list[Connection],
    ) -> Connection:
        content = line.removeprefix("connection:").strip()
        parts = content.split()

        zone1, zone2 = parts[0].split("-", 1)

        if zone1 not in zones or zone2 not in zones:
            raise ParsingError(f"Unknown zone in connection '{zone1}-{zone2}'", linenb)
        if any(
            (c.zone1.name == zone1 and c.zone2.name == zone2)
            or (c.zone2.name == zone1 and c.zone1.name == zone2)
            for c in connections
        ):
            raise ParsingError(
                f"Connection between '{zone1}-{zone2}' already exists", linenb
            )
        capacity = 1
        if len(parts) > 1:
            meta_str = parts[1].strip("[]")
            if "=" not in meta_str:
                raise ParsingError("Invalid metadata format", linenb)
            key, val = meta_str.split("=", 1)
            if key != "max_link_capacity":
                raise ParsingError(f"Unknown connection metadata key '{key}'", linenb)
            try:
                capacity = int(val)
                if capacity < 1:
                    raise ParsingError(
                        "max_link_capacity should be positive integer", linenb
                    )
            except ValueError:
                raise ParsingError(
                    f"max_link_capacity must be an integer, got '{val}'",
                    linenb,
                )

        conn = Connection(
            zone1=zones[zone1],
            zone2=zones[zone2],
            max_link_capacity=capacity,
        )
        zones[zone1].links.append(Link(target=zones[zone2], connection=conn))
        zones[zone2].links.append(Link(target=zones[zone1], connection=conn))
        return conn

    def parse(self, filepath: str) -> Graph:
        lines = self.__remove_comments(
            self.__load_file(filepath).read_text()
        ).splitlines()
        if not lines:
            raise ParsingError("Map file is empty")
        start_hub: Zone | None = None
        end_hub: Zone | None = None
        nb_drones: int | None = None
        zones: dict[str, Zone] = {}
        connections: list[Connection] = []

        if lines[0].startswith("nb_drones:"):
            try:
                nb_drones = int(lines[0][len("nb_drones:") :].strip())
            except (ValueError, IndexError) as e:
                raise ParsingError(
                    f"Invalid nb_drones value or format in the map file: {e}"
                )
            if nb_drones < 1:
                raise ParsingError("nb_drones must be at least 1")
        else:
            raise ParsingError("File should start with the number of drones first")
        for linenb, line in enumerate(lines[1:], start=2):
            if (
                line.startswith("start_hub:")
                or line.startswith("end_hub:")
                or line.startswith("hub:")
            ):
                hub = self.__parse_hub(line, linenb, zones)
                zones[hub.name] = hub
                if line.startswith("start_hub"):
                    if start_hub is not None:
                        raise ParsingError(
                            "Multiple start_hub definitions found", linenb
                        )
                    start_hub = hub
                elif line.startswith("end_hub"):
                    if end_hub is not None:
                        raise ParsingError("Multiple end_hub definitions found", linenb)
                    end_hub = hub

            elif line.startswith("connection:"):
                connections.append(
                    self.__parse_connection(line, linenb, zones, connections)
                )

            else:
                raise ParsingError(f"Unrecognized line: {line}")

        if start_hub is None:
            raise ParsingError(
                "start_hub is required but was not found in the map file"
            )
        if end_hub is None:
            raise ParsingError("end_hub is required but was not found in the map file")

        return Graph(
            nb_drones=nb_drones,
            start_hub=start_hub,
            end_hub=end_hub,
            zones=zones,
            connections=connections,
        )


Zone.model_rebuild()
Connection.model_rebuild()
Link.model_rebuild()
