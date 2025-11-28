from enum import Enum

from ...base.capabilities import PiezoCapability, StaticWaveformGenerator


class DDriveWaveformType(Enum):
    NONE = 0
    SINE = 1
    TRIANGLE = 2
    RECTANGLE = 3
    NOISE = 4
    SWEEP = 5
    UNKNOWN = 99


class DDriveScanType(Enum):
    OFF = 0
    SINE_ONCE = 1
    TRIANGLE_ONCE = 2
    SINE_TWICE = 3
    TRIANGLE_TWICE = 4
    UNKNOWN = 99


class DDriveWaveformGenerator(PiezoCapability):
    CMD_WFG_TYPE = "WFG_TYPE"
    CMD_SINE_AMPLITUDE = "WFG_SINE_AMPLITUDE"
    CMD_SINE_OFFSET = "WFG_SINE_OFFSET"
    CMD_SINE_FREQUENCY = "WFG_SINE_FREQUENCY"
    CMD_TRI_AMPLITUDE = "WFG_TRIANGLE_AMPLITUDE"
    CMD_TRI_OFFSET = "WFG_TRIANGLE_OFFSET"
    CMD_TRI_FREQUENCY = "WFG_TRIANGLE_FREQUENCY"
    CMD_TRI_DUTY_CYCLE = "WFG_TRIANGLE_DUTY_CYCLE"
    CMD_REC_AMPLITUDE = "WFG_RECTANGLE_AMPLITUDE"
    CMD_REC_OFFSET = "WFG_RECTANGLE_OFFSET"
    CMD_REC_FREQUENCY = "WFG_RECTANGLE_FREQUENCY"
    CMD_REC_DUTY_CYCLE = "WFG_RECTANGLE_DUTY_CYCLE"
    CMD_NOISE_AMPLITUDE = "WFG_NOISE_AMPLITUDE"
    CMD_NOISE_OFFSET = "WFG_NOISE_OFFSET"
    CMD_SWEEP_AMPLITUDE = "WFG_SWEEP_AMPLITUDE"
    CMD_SWEEP_OFFSET = "WFG_SWEEP_OFFSET"
    CMD_SWEEP_TIME = "WFG_SWEEP_TIME"
    CMD_SCAN_START = "WFG_SCAN_START"
    CMD_SCAN_TYPE = "WFG_SCAN_TYPE"


    def __init__(
        self,
        write_cb,
        device_commands
    ) -> None:
        super().__init__(write_cb, device_commands)

        # Register waveform types
        self._sine = StaticWaveformGenerator(
            self._write_cb,
            {
                StaticWaveformGenerator.CMD_AMPLITUDE: self._device_commands[self.CMD_SINE_AMPLITUDE],
                StaticWaveformGenerator.CMD_OFFSET: self._device_commands[self.CMD_SINE_OFFSET],
                StaticWaveformGenerator.CMD_FREQUENCY: self._device_commands[self.CMD_SINE_FREQUENCY],
            },
            DDriveWaveformType.SINE,
        )

        self._triangle = StaticWaveformGenerator(
            self._write_cb,
            {
                StaticWaveformGenerator.CMD_AMPLITUDE: self._device_commands[self.CMD_TRI_AMPLITUDE],
                StaticWaveformGenerator.CMD_OFFSET: self._device_commands[self.CMD_TRI_OFFSET],
                StaticWaveformGenerator.CMD_FREQUENCY: self._device_commands[self.CMD_TRI_FREQUENCY],
                StaticWaveformGenerator.CMD_DUTY_CYCLE: self._device_commands[self.CMD_TRI_DUTY_CYCLE],
            },
            DDriveWaveformType.TRIANGLE,
        )

        self._rectangle = StaticWaveformGenerator(
            self._write_cb,
            {
                StaticWaveformGenerator.CMD_AMPLITUDE: self._device_commands[self.CMD_REC_AMPLITUDE],
                StaticWaveformGenerator.CMD_OFFSET: self._device_commands[self.CMD_REC_OFFSET],
                StaticWaveformGenerator.CMD_FREQUENCY: self._device_commands[self.CMD_REC_FREQUENCY],
                StaticWaveformGenerator.CMD_DUTY_CYCLE: self._device_commands[self.CMD_REC_DUTY_CYCLE],
            },
            DDriveWaveformType.RECTANGLE,
        )

        self._noise = StaticWaveformGenerator(
            self._write_cb,
            {
                StaticWaveformGenerator.CMD_AMPLITUDE: self._device_commands[self.CMD_NOISE_AMPLITUDE],
                StaticWaveformGenerator.CMD_OFFSET: self._device_commands[self.CMD_NOISE_OFFSET],
            },
            DDriveWaveformType.NOISE,
        )

        self._sweep = StaticWaveformGenerator(
            self._write_cb,
            {
                StaticWaveformGenerator.CMD_AMPLITUDE: self._device_commands[self.CMD_SWEEP_AMPLITUDE],
                StaticWaveformGenerator.CMD_OFFSET: self._device_commands[self.CMD_SWEEP_OFFSET],
                StaticWaveformGenerator.CMD_FREQUENCY: self._device_commands[self.CMD_SWEEP_TIME],
            },
            DDriveWaveformType.SWEEP,
        )

    async def set_waveform_type(self, waveform_type: DDriveWaveformType) -> None:
        await self._write(self.CMD_WFG_TYPE, [waveform_type.value])

    async def get_waveform_type(self) -> DDriveWaveformType:
        result = await self._write(self.CMD_WFG_TYPE)
        return DDriveWaveformType(int(result[0]))

    async def start_scan(self, scan_type: DDriveScanType) -> None:
        await self._write(self.CMD_SCAN_TYPE, [scan_type.value])
        await self._write(self.CMD_SCAN_START, [1])

    async def is_scan_running(self) -> bool:
        result = await self._write(self.CMD_SCAN_START)
        return int(result[0]) != 0

    @property
    def sine(self) -> StaticWaveformGenerator:
        return self._sine

    @property
    def triangle(self) -> StaticWaveformGenerator:
        return self._triangle

    @property
    def rectangle(self) -> StaticWaveformGenerator:
        return self._rectangle

    @property
    def noise(self) -> StaticWaveformGenerator:
        return self._noise

    @property
    def sweep(self) -> StaticWaveformGenerator:
        return self._sweep