from exceptions.parsing import FlyInError


class SimulationError(FlyInError):
    """Base exception for all simulation errors."""

    def __init__(self, message: str) -> None:
        """Initialize with error message.

        Args:
            message: A description of the simulation error.
        """
        super().__init__(message)
