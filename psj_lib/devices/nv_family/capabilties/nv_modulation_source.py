from ...base.capabilities import ModulationSource, ModulationSourceTypes

class NVModulationSourceTypes(ModulationSourceTypes):
    ENCODER_ANALOG = 0
    SERIAL = 1

class NVModulationSource(ModulationSource):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._source_cache: NVModulationSourceTypes = NVModulationSourceTypes.ENCODER_ANALOG

    async def set_source(self, source: NVModulationSourceTypes) -> None:
        await super().set_source(source)
        self._source_cache = source

    async def get_source(self) -> NVModulationSourceTypes:
        # NV does not support querying modulation source, so we return the last set value from cache
        return self._source_cache
