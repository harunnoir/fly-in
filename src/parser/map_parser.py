from enum import Enum
from pydantic import BaseModel
from pathlib import Path


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

    def __remove_comments(self, map_data) -> None:
        pass

    def parse(self) -> Graph | None:
        content = self._filepath.read_text()
        self.__remove_comments(content)
        return None
