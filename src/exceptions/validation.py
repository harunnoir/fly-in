from exceptions.parsing import FlyInError


class ValidationError(FlyInError):
    """Base exception for all validation errors."""

    def __init__(self, message: str) -> None:
        """Initialize with error message.

        Args:
            message: A description of the validation error.
        """
        super().__init__(message)
