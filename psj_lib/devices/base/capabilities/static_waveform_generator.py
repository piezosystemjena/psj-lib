from .piezo_capability import PiezoCapability


class StaticWaveformGenerator(PiezoCapability):
    CMD_FREQUENCY = "STATIC_WAVEFORM_FREQUENCY"
    CMD_AMPLITUDE = "STATIC_WAVEFORM_AMPLITUDE"
    CMD_OFFSET = "STATIC_WAVEFORM_OFFSET"
    CMD_DUTY_CYCLE = "STATIC_WAVEFORM_DUTY_CYCLE"

    async def set(
        self,
        frequency: float | None = None,
        amplitude: float | None = None,
        offset: float | None = None,
        duty_cycle: float | None = None
    ) -> None:
        if frequency is not None:
            await self._write(self.CMD_FREQUENCY, [frequency])

        if amplitude is not None:
            await self._write(self.CMD_AMPLITUDE, [amplitude])

        if offset is not None:
            await self._write(self.CMD_OFFSET, [offset])

        if duty_cycle is not None:
            await self._write(self.CMD_DUTY_CYCLE, [duty_cycle])

    async def get_frequency(self) -> float:
        result = await self._write(self.CMD_FREQUENCY)
        return float(result[0])

    async def get_amplitude(self) -> float:
        result = await self._write(self.CMD_AMPLITUDE)
        return float(result[0])

    async def get_offset(self) -> float:
        result = await self._write(self.CMD_OFFSET)
        return float(result[0])

    async def get_duty_cycle(self) -> float:
        result = await self._write(self.CMD_DUTY_CYCLE)
        return float(result[0])

