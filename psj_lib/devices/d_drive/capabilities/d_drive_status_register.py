from enum import Enum

from ...base.capabilities import StatusRegister
from ...base.piezo_types import SensorType


class DDriveWaveformGeneratorStatus(Enum):
    INACTIVE = 0
    SINE = 1
    TRIANGLE = 2
    RECTANGLE = 3
    NOISE = 4
    SWEEP = 5
    UNKNOWN = 99


class DDriveStatusRegister(StatusRegister):
    """
    Represents the status register for a D-Drive channel.
    """

    @property
    def actor_plugged(self) -> bool:
        val = int(self._raw[0])
        return bool(val & 0x0001)

    @property
    def sensor_type(self) -> SensorType:
        val = int(self._raw[0])
        return SensorType((val & 0x0006) >> 1)

    @property
    def piezo_voltage_enabled(self) -> bool:
        val = int(self._raw[0])
        return bool(val & 0x0040)

    @property
    def closed_loop(self) -> bool:
        val = int(self._raw[0])
        return bool(val & 0x0080)

    @property
    def waveform_generator_status(self) -> DDriveWaveformGeneratorStatus:
        val = int(self._raw[0])
        wg_status = (val & 0x0E00) >> 9

        try:
            return DDriveWaveformGeneratorStatus(wg_status)
        except ValueError:
            return DDriveWaveformGeneratorStatus.UNKNOWN

    @property
    def notch_filter_active(self) -> bool:
        val = int(self._raw[0])
        return bool(val & 0x1000)

    @property
    def low_pass_filter_active(self) -> bool:
        val = int(self._raw[0])
        return bool(val & 0x2000)