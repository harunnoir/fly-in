from enum import Enum
from pydantic import BaseModel
from pathlib import Path

from exceptions import ParsingError


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
            raise FileNotFoundError(f"Map file '{self._filepath}' not found")

        if self._filepath.suffix != ".txt":
            raise ValueError(
                f"Expected .txt file, got '{self._filepath.suffix}'"
            )

    def __remove_comments(self, map_data: str) -> str:
        return "\n".join(
            line.split("#", 1)[0].strip()
            for line in map_data.splitlines()
            if line.split("#", 1)[0].strip()
        )

    def parse(self) -> Graph | None:
        lines = self.__remove_comments(self._filepath.read_text())
        if not lines.strip():
            raise ValueError("Map file is empty")
        nb_drones: int | None = None
        start_hub: Zone | None = None
        end_hub: Zone | None = None
        zones: dict[str, Zone] = {}
        connections: list[Connection] = []

        for i, line in enumerate(lines, start=1):
            if line.startswith("nb_drones"):
                if nb_drones is not None:
                    raise ValueError("Duplicate nb_drones definition")
                nb_drones = int(line.split(":")[1].strip())
            if line.startswith("nb_drones:"):
                if nb_drones is not None:
                    raise ParsingError(i, "Duplicate nb_drones definition")
                ...
            elif line.startswith("start_hub:"):
                ...
            elif line.startswith("end_hub:"):
                ...
            elif line.startswith("hub:"):
                ...
            elif line.startswith("connection:"):
                ...
            else:
                raise ParsingError(i, f"Unrecognized line: {line}")

        # validate required fields
        ...

        return Graph(
            nb_drones=nb_drones,
            start_hub=start_hub,
            end_hub=end_hub,
            zones=zones,
            connections=connections,
        )
