from exceptions.parsing import FlyInError


class SimulationError(FlyInError):
    """Base exception for all simulation errors."""

    def __init__(self, message: str) -> None:
        """Initialize with error message.

        Args:
            message: A description of the simulation error.
        """
        super().__init__(message)


class DeadlockError(SimulationError):
    """Raised when drones are deadlocked and cannot move."""

    def __init__(self) -> None:
        """Initialize with default deadlock message."""
        super().__init__("Drones are deadlocked and cannot move")


class BlockedPathError(SimulationError):
    """Raised when no valid path exists from start to end."""

    def __init__(self, start: str, end: str) -> None:
        """Initialize with start and end zone names.

        Args:
            start: The name of the start zone.
            end: The name of the end zone.
        """
        super().__init__(f"No valid path from '{start}' to '{end}'")
