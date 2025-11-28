from .piezo_capability import PiezoCapability


class NotchFilter(PiezoCapability):
    CMD_ENABLE = "NOTCH_FILTER_ENABLE"
    CMD_FREQUENCY = "NOTCH_FILTER_FREQUENCY"    
    CMD_BANDWIDTH = "NOTCH_FILTER_BANDWIDTH"


    async def set(
        self,
        enabled: bool | None = None,
        frequency: float | None = None,
        bandwidth: float | None = None,
    ) -> None:
        if enabled is not None:
            await self._write(self.CMD_ENABLE, [enabled])
    
        if frequency is not None:
            await self._write(self.CMD_FREQUENCY, [frequency])
    
        if bandwidth is not None:
            await self._write(self.CMD_BANDWIDTH, [bandwidth])


    async def get_enabled(self) -> bool:
        result = await self._write(self.CMD_ENABLE)
        return bool(result[0])
    

    async def get_frequency(self) -> float:
        result = await self._write(self.CMD_FREQUENCY)
        return float(result[0])
    

    async def get_bandwidth(self) -> float:
        result = await self._write(self.CMD_BANDWIDTH)
        return float(result[0])