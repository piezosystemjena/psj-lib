from enum import Enum
from typing import Type


class DeviceError(Exception):
    """Base class for device-related errors."""

    pass


class ErrorNotSpecified(DeviceError):
    """Error not specified."""

    pass


class UnknownCommand(DeviceError):
    """Unknown command."""

    pass


class ParameterMissing(DeviceError):
    """Parameter missing."""

    pass


class AdmissibleParameterRangeExceeded(DeviceError):
    """Admissible parameter range exceeded."""

    pass


class CommandParameterCountExceeded(DeviceError):
    """Command's parameter count exceeded."""

    pass


class ParameterLockedOrReadOnly(DeviceError):
    """Parameter is locked or read only."""

    pass


class Underload(DeviceError):
    """Underload."""

    pass


class Overload(DeviceError):
    """Overload."""

    pass


class ParameterTooLow(DeviceError):
    """Parameter too low."""

    pass


class ParameterTooHigh(DeviceError):
    """Parameter too high."""

    pass


class ErrorCode(Enum):
    """
    ErrorCode(Enum):
        An enumeration representing various error codes and their corresponding descriptions.
    """
    ERROR_NOT_SPECIFIED = 1
    UNKNOWN_COMMAND = 2
    PARAMETER_MISSING = 3
    ADMISSIBLE_PARAMETER_RANGE_EXCEEDED = 4
    COMMAND_PARAMETER_COUNT_EXCEEDED = 5
    PARAMETER_LOCKED_OR_READ_ONLY = 6
    UNDERLOAD = 7
    OVERLOAD = 8
    PARAMETER_TOO_LOW = 9
    PARAMETER_TOO_HIGH = 10

    DESCRIPTIONS = {
        ERROR_NOT_SPECIFIED: "Error not specified",
        UNKNOWN_COMMAND: "Unknown command",
        PARAMETER_MISSING: "Parameter missing",
        ADMISSIBLE_PARAMETER_RANGE_EXCEEDED: "Admissible parameter range exceeded",
        COMMAND_PARAMETER_COUNT_EXCEEDED: "Command's parameter count exceeded",
        PARAMETER_LOCKED_OR_READ_ONLY: "Parameter is locked or read only",
        UNDERLOAD: "Underload",
        OVERLOAD: "Overload",
        PARAMETER_TOO_LOW: "Parameter too low",
        PARAMETER_TOO_HIGH: "Parameter too high"
    }


    @classmethod
    def from_value(cls, value: int) -> 'ErrorCode':
        """
        Converts an integer value to its corresponding ErrorCode enum member.

        Args:
            value (int): The integer value representing the error code.

        Returns:
            ErrorCode: The corresponding ErrorCode enum member.

        Raises:
            ValueError: If the value does not correspond to any ErrorCode member.
        """
        for member in cls:
            if member.value == value:
                return member

        raise ValueError(f"No ErrorCode member with value {value}")

    @classmethod
    def get_exception_class(cls, error_code) -> Type[DeviceError]:
        """
        Returns the appropriate exception class for a given error code.

        Args:
            error_code (ErrorCode or int): The error code for which to get the exception class.

        Returns:
            Type[DeviceError]: The exception class corresponding to the error code.
        """
        # Convert int to ErrorCode if needed
        if isinstance(error_code, int):
            error_code = cls.from_value(error_code)

        exception_map = {
            cls.ERROR_NOT_SPECIFIED: ErrorNotSpecified,
            cls.UNKNOWN_COMMAND: UnknownCommand,
            cls.PARAMETER_MISSING: ParameterMissing,
            cls.ADMISSIBLE_PARAMETER_RANGE_EXCEEDED: AdmissibleParameterRangeExceeded,
            cls.COMMAND_PARAMETER_COUNT_EXCEEDED: CommandParameterCountExceeded,
            cls.PARAMETER_LOCKED_OR_READ_ONLY: ParameterLockedOrReadOnly,
            cls.UNDERLOAD: Underload,
            cls.OVERLOAD: Overload,
            cls.PARAMETER_TOO_LOW: ParameterTooLow,
            cls.PARAMETER_TOO_HIGH: ParameterTooHigh
        }

        return exception_map.get(error_code, ErrorNotSpecified)

    @classmethod
    def raise_error(cls, error_code, message=None):
        """
        Raises the appropriate exception for a given error code.

        Args:
            error_code (ErrorCode or int): The error code to raise.
            message (str, optional): Custom error message. If not provided, uses default description.

        Raises:
            DeviceError: The specific exception corresponding to the error code.
        """
        # Convert int to ErrorCode if needed
        if isinstance(error_code, int):
            error_code = cls.from_value(error_code)

        actual_message = message or cls.DESCRIPTIONS.get(error_code, "Unknown error")

        exception_class = cls.get_exception_class(error_code)
        raise exception_class(actual_message)