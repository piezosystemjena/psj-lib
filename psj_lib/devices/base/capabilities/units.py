from .piezo_capability import PiezoCapability


class Units(PiezoCapability):
    CMD_UNIT_VOLTAGE = "UNIT_VOLTAGE"
    CMD_UNIT_POSITION = "UNIT_POSITION"

    async def get_voltage_unit(self) -> str:
        result = await self._write(self.CMD_UNIT_VOLTAGE)
        return result[0]

    async def get_position_unit(self) -> str:
        result = await self._write(self.CMD_UNIT_POSITION)
        return result[0]