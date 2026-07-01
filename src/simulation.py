from __future__ import annotations
from src.map_parser import Graph, Zone


class DroneState:
    """Tracks a single drone's position and status during simulation."""

    def __init__(self, drone_id: str, start_zone: Zone) -> None: ...

    def is_delivered(self) -> bool:
        """Returns True if this drone has reached the goal."""
        ...

    def current_zone(self) -> Zone:
        """Returns the zone this drone is currently in."""
        ...


class TurnResult:
    """Snapshot of all drone movements that happened in one turn."""

    def __init__(self) -> None: ...

    def add_move(self, drone_id: str, zone_name: str) -> None:
        """Record that a drone moved to a zone this turn."""
        ...

    def to_output_line(self) -> str:
        """Format as required output: 'D1-zone D2-zone ...'"""
        ...


class Simulator:
    """Executes drone movement turn by turn along a given path.

    Responsibilities:
        - Assign paths to drones
        - Move drones each turn respecting capacity constraints
        - Track which zones are occupied
        - Detect when all drones are delivered
    """

    def __init__(self, graph: Graph) -> None: ...

    def run(self, path: list[Zone]) -> list[TurnResult]:
        """Run the full simulation, returning one TurnResult per turn.

        Args:
            path: Ordered list of zones from start to goal (from pathfinder).

        Returns:
            List of TurnResult, one per simulation turn.
        """
        ...

    def _assign_drones(self, start_zone: Zone) -> list[DroneState]:
        """Create N drones all starting at start_zone."""
        ...

    def _run_turn(
        self,
        drones: list[DroneState],
        zone_occupancy: dict[str, int],
    ) -> TurnResult:
        """Move all drones one step forward if capacity allows.

        Args:
            drones: All active (non-delivered) drones.
            zone_occupancy: Current drone count per zone.

        Returns:
            TurnResult recording all moves this turn.
        """
        ...

    def _can_enter(self, zone: Zone, zone_occupancy: dict[str, int]) -> bool:
        """Check if a zone has capacity for one more drone."""
        ...
