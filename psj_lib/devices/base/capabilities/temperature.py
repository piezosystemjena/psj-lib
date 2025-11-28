from .piezo_capability import PiezoCapability


class Temperature(PiezoCapability):
    CMD_TEMPERATURE = "TEMPERATURE"


    async def get(self) -> float:
        result = await self._write(self.CMD_TEMPERATURE)
        return float(result[0])