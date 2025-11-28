from .piezo_capability import PiezoCapability


class FactoryReset(PiezoCapability):
    CMD_RESET = "FACTORY_RESET"

    async def execute(self) -> None:
        await self._write(self.CMD_RESET)