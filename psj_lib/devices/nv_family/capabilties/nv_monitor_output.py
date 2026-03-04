from psj_lib.devices.base.capabilities.monitor_output import MonitorOutput

from ...base.capabilities import MonitorOutput, MonitorOutputSource

class NVMonitorOutputSource(MonitorOutputSource):
    ACTUATOR_VOLTAGE = 0
    POSITION_VOLTAGE = 1
    MODE_DEPENDENT = 2

class NVMonitorOutput(MonitorOutput):
    _source_cache: NVMonitorOutputSource = NVMonitorOutputSource.ACTUATOR_VOLTAGE

    async def set_source(self, source: NVMonitorOutputSource) -> None:
        if type(source) is not NVMonitorOutputSource:
            raise ValueError(f"Invalid monitor source type: {type(source)} (Expected: NVMonitorOutputSource)")

        await self._write(self.CMD_OUTPUT_SRC, [source.value])
        self._source_cache = source

    async def get_source(self) -> NVMonitorOutputSource:
        return self._source_cache
