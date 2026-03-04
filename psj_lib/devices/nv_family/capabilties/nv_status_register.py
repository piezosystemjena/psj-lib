"""NV status register interpretation helpers.

This module provides flag constants and an NV-specific
:class:`~psj_lib.devices.base.capabilities.status.StatusRegister`
implementation for decoding per-channel status words.
"""

from ...base.capabilities import StatusRegister, Status

FLAG_ACTUATOR_NOT_PLUGGED = 0x0001
FLAG_ACTUATOR_SHORT = 0x0002
FLAG_EEPROM_ERROR = 0x0010
FLAG_UNDERLOAD = 0x1000
FLAG_OVERLOAD = 0x2000
FLAG_INVALID_ACTUATOR = 0x4000
FLAG_OVER_TEMPERATURE = 0x8000

class NVStatusRegister(StatusRegister):
    """NV-specific interpretation of per-channel error/status flags.

    The raw NV ``ERROR`` response contains one hexadecimal status value per
    channel. This class interprets those bit fields.

    Example:
        >>> status = await channel.status.get()
        >>> if not status.actuator_plugged:
        ...     print("No actuator connected")
        >>> if status.over_temperature:
        ...     print("Thermal warning")
    """

    def interpret_status_register(self, flag: int) -> bool:
        """Interpret a specific flag from the raw status register value.
        
        Args:
            flag: Specific flag bit to interpret (e.g. FLAG_ACTUATOR_NOT_PLUGGED)

        Returns:
            True if the specified bit is set for the current channel,
            otherwise False.

        Raises:
            ValueError: If no channel ID context is available.
        """
        if self._channel_id is None:
            raise ValueError("Channel ID is required to interpret status register for NV Family.")

        val = int(self._raw[self._channel_id], 16)
        return bool(val & flag)

    @property
    def actuator_plugged(self) -> bool:
        """Indicates whether the actuator is plugged in.

        Returns:
            True if the actuator is detected, otherwise False.
        """
        return not self.interpret_status_register(FLAG_ACTUATOR_NOT_PLUGGED)
    
    @property
    def actuator_short(self) -> bool:
        """Indicates whether a short circuit is detected on the actuator.

        Returns:
            True if a short condition is present, otherwise False.
        """
        return self.interpret_status_register(FLAG_ACTUATOR_SHORT)
    
    @property
    def eeprom_error(self) -> bool:
        """Indicates whether an EEPROM error is detected.

        Returns:
            True if EEPROM error flag is set, otherwise False.
        """
        return self.interpret_status_register(FLAG_EEPROM_ERROR)
    
    @property
    def underload(self) -> bool:
        """
        Indicates whether an underload condition is detected.

        In this case the actuator is not able to reach the setpoint even with minimum voltage.

        Returns:
            True if underload condition is active, otherwise False.
        """
        return self.interpret_status_register(FLAG_UNDERLOAD)

    @property
    def overload(self) -> bool:
        """
        Indicates whether an overload condition is detected.
    
        In this case the actuator is not able to reach the setpoint even with maximum voltage.

        Returns:
            True if overload condition is active, otherwise False.
        """
        return self.interpret_status_register(FLAG_OVERLOAD)
    
    @property
    def invalid_actuator(self) -> bool:
        """Indicates whether an invalid actuator is detected.

        Returns:
            True if actuator identification is invalid, otherwise False.
        """
        return self.interpret_status_register(FLAG_INVALID_ACTUATOR)
    
    @property
    def over_temperature(self) -> bool:
        """Indicates whether an over-temperature condition is detected.

        Returns:
            True if over-temperature flag is set, otherwise False.
        """
        return self.interpret_status_register(FLAG_OVER_TEMPERATURE)
