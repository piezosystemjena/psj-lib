from .piezo_capability import PiezoCapability


class ActuatorDescription(PiezoCapability):
    CMD_DESCRIPTION = "actuator_description"

    async def get(self) -> str:
        result = await self._write(self.CMD_DESCRIPTION)
        return result[0]