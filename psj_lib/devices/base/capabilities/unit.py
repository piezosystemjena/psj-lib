"""Unit information capability for device measurements."""

from .piezo_capability import PiezoCapability


class Unit(PiezoCapability):
    """Query device measurement units for voltage and position.
    
    Provides methods to retrieve the units of measurement used by the
    device for voltage and position values. Units may vary by device
    configuration or hardware model.
    
    Example:
        >>> units = device.units
        >>> openloop_unit = await units.get_openloop_unit()
        >>> closedloop_unit = await units.get_closedloop_unit()
        >>> print(f"Voltage: {openloop_unit}, Position: {closedloop_unit}")
        >>> # Voltage: V, Position: µm
    
    Note:
        - Units are device-specific and may be configurable
        - Common voltage units: V, mV
        - Common position units: µm, mrad
    """
    
    CMD_UNIT = "UNIT"

    async def get(self) -> str:
        """Get the unit of measurement for the specified capability.
        
        Returns:
            Unit string (e.g., 'V', 'mV')
        
        Example:
            >>> unit = await device.units.get_unit()
            >>> print(f"Voltage is measured in {unit}")
        """
        result = await self._write(self.CMD_UNIT)

        if not result:
            return "Unknown"
        
        return result[0].strip()
    