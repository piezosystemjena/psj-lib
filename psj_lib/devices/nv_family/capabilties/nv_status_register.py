from typing import List

from ...base.capabilities import StatusRegister, Status

FLAG_ACTUATOR_NOT_PLUGGED = 0x0001
FLAG_ACTUATOR_SHORT = 0x0002
FLAG_EEPROM_ERROR = 0x0010
FLAG_UNDERLOAD = 0x1000
FLAG_OVERLOAD = 0x2000
FLAG_INVALID_ACTUATOR = 0x4000
FLAG_OVER_TEMPERATURE = 0x8000

class NVStatusRegister(StatusRegister):
    def interpret_status_register(self, flag: int) -> bool:
        """Interpret a specific flag from the raw status register value.
        
        Args:
            flag: Specific flag bit to interpret (e.g. FLAG_ACTUATOR_NOT_PLUGGED)
        Returns:
            bool: True if the specified flag is set in the status register, False otherwise
        """
        if self._channel_id is None:
            raise ValueError("Channel ID is required to interpret status register for NV Family.")

        val = int(self._raw[self._channel_id], 16)
        return bool(val & flag)

    @property
    def actuator_plugged(self) -> bool:
        """Indicates whether the actuator is plugged in."""
        return not self.interpret_status_register(FLAG_ACTUATOR_NOT_PLUGGED)
    
    @property
    def actuator_short(self) -> bool:
        """Indicates whether a short circuit is detected on the actuator."""
        return self.interpret_status_register(FLAG_ACTUATOR_SHORT)
    
    @property
    def eeprom_error(self) -> bool:
        """Indicates whether an EEPROM error is detected."""
        return self.interpret_status_register(FLAG_EEPROM_ERROR)
    
    @property
    def underload(self) -> bool:
        """
        Indicates whether an underload condition is detected.

        In this case the actuator is not able to reach the setpoint even with minimum voltage.
        """
        return self.interpret_status_register(FLAG_UNDERLOAD)

    @property
    def overload(self) -> bool:
        """
        Indicates whether an overload condition is detected.
    
        In this case the actuator is not able to reach the setpoint even with maximum voltage.
        """
        return self.interpret_status_register(FLAG_OVERLOAD)
    
    @property
    def invalid_actuator(self) -> bool:
        """Indicates whether an invalid actuator is detected."""
        return self.interpret_status_register(FLAG_INVALID_ACTUATOR)
    
    @property
    def over_temperature(self) -> bool:
        """Indicates whether an over-temperature condition is detected."""
        return self.interpret_status_register(FLAG_OVER_TEMPERATURE)
