from enum import Enum

from .piezo_capability import PiezoCapability


class MonitorOutputSource(Enum):
    UNKNOWN = 99


class MonitorOutput(PiezoCapability):
    CMD_OUTPUT_SRC = "MONITOR_OUTPUT_SRC"

    def __init__(
        self,
        write_cb,
        device_commands,
        sources: type[MonitorOutputSource]
    ) -> None:
        super().__init__(write_cb, device_commands)
        self._sources = sources

    async def set_source(self, source: MonitorOutputSource) -> None:
        if type(source) is not self._sources:
            raise ValueError(f"Invalid monitor source type: {type(source)} (Expected: {self._sources})")

        await self._write(self.CMD_OUTPUT_SRC, [source.value])

    async def get_source(self) -> MonitorOutputSource:
        result = await self._write(self.CMD_OUTPUT_SRC)
        value = int(result[0])

        try:
            return self._sources(value)
        except ValueError:
            return self._sources.UNKNOWN