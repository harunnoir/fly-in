class FlyInError(Exception):
    """Base exception for the Fly-in project."""

    pass


class EmptyFileError(FlyInError):
    """Raised when the input file is empty."""

    def __init__(self, message: str = "The input file is empty.") -> None:
        super().__init__(message)


class ParsingError(FlyInError):
    """Base exception for all parsing errors, includes line number."""

    def __init__(self, line: int, message: str) -> None:
        """Initialize with line number and error message.

        Args:
            line: The line number where the error occurred.
            message: A description of the parsing error.
        """
        super().__init__(f"Line {line}: {message}")


class MissingDronesError(ParsingError):
    """Raised when the first line is not a valid nb_drones definition."""

    pass


class InvalidDronesError(ParsingError):
    """Raised when nb_drones is not a positive integer."""

    pass


class InvalidNameError(ParsingError):
    """Raised when a zone name contains a dash or space."""

    pass


class InvalidCoordinateError(ParsingError):
    """Raised when x or y coordinate is missing or not an integer."""

    pass


class InvalidZoneTypeError(ParsingError):
    """Raised when zone type is not one of normal/blocked/restricted/priority."""

    pass


class InvalidCapacityError(ParsingError):
    """Raised when max_drones or max_link_capacity is not a positive integer."""

    pass


class InvalidMetadataError(ParsingError):
    """Raised when a metadata block [...] is malformed or contains unknown keys."""

    pass


class DuplicateZoneError(ParsingError):
    """Raised when a zone name is defined more than once."""

    pass


class MissingHubError(ParsingError):
    """Raised when no start_hub or no end_hub is found after full parse."""

    pass


class DuplicateHubError(ParsingError):
    """Raised when more than one start_hub or end_hub is defined."""

    pass


class UndefinedZoneError(ParsingError):
    """Raised when a connection references a zone that has not been defined."""

    pass


class DuplicateConnectionError(ParsingError):
    """Raised when the same connection is defined twice (a-b and b-a)."""

    pass


class SelfConnectionError(ParsingError):
    """Raised when a zone is connected to itself (a-a)."""

    pass


class InvalidLineError(ParsingError):
    """Raised when a line does not match any known syntax pattern."""

    pass
