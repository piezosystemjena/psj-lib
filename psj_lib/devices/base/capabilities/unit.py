"""Unit information capability for device measurements."""

from .piezo_capability import PiezoCapability


class Unit(PiezoCapability):
    """Query device measurement units for voltage and position.
    
    Provides methods to retrieve the units of measurement for a device's operation mode.
    
    Example:
        >>> unit = device.openloop_unit
        >>> openloop_unit = await unit.get()
        >>> print(f"Voltage: {openloop_unit}")
        >>> # Voltage: V or mV depending on device configuration
    
    Note:
        - Units are device-specific and may be configurable
        - Common voltage units: V, mV
        - Common position units: µm, mrad
    """
    
    CMD_UNIT = "UNIT"

    async def get(self) -> str:
        """Get the unit of measurement for the specified capability.
        
        Returns:
            Unit string (e.g., 'V', 'mV', 'µm', 'mrad') or 'Unknown' if not available.
        
        Example:
            >>> unit = await device.openloop_unit.get()
            >>> print(f"Voltage is measured in {unit}")
        """
        result = await self._write(self.CMD_UNIT)

        if not result:
            return "Unknown"
        
        return result[0].strip()
    