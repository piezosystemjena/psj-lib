from enum import Enum

from .piezo_capability import PiezoCapability


class ModulationSourceTypes(Enum):
    UNKNOWN = 99


class ModulationSource(PiezoCapability):
    CMD_SOURCE = "MODULATION_SOURCE"

    def __init__(
        self,
        write_cb,
        device_commands,
        sources: type[ModulationSourceTypes]
    ) -> None:
        super().__init__(write_cb, device_commands)
        self._sources = sources

    async def set_source(self, source: ModulationSourceTypes) -> None:
        if type(source) is not self._sources:
            raise ValueError(f"Invalid modulation source type: {type(source)} (Expected: {self._sources})")

        await self._write(self.CMD_SOURCE, [source.value])

    async def get_source(self) -> ModulationSourceTypes:
        result = await self._write(self.CMD_SOURCE)
        value = int(result[0])

        try:
            return self._sources(value)
        except ValueError:
            return self._sources.UNKNOWN