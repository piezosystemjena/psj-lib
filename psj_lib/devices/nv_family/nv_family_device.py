from ..base.capabilities import *
from ..base.exceptions import *
from ..base.piezo_device import PiezoDevice
from ..transport_protocol import TransportProtocol
from .capabilties.nv_display import NVDisplay
from .capabilties.nv_knob import NVKnob
from .capabilties.nv_modulation_source import NVModulationSourceTypes
from .capabilties.nv_monitor_output import NVMonitorOutputSource
from .nv_family_channel import NVFamilyChannel

class NVFamilyDevice(PiezoDevice):
    DEVICE_ID = "NV Family Device"
    """Device type identifier used for device discovery and type checking."""

    BACKUP_COMMANDS = set()
    """Global device commands to include in backup operations (currently none for NV Family)."""

    NV_FAMILY_IDENTIFIER = "INVALID_STRING"
    """Internal identifier string used to recognize different NV Family devices. Overridden in subclasses."""

    NV_CHANNEL_TYPE = NVFamilyChannel
    """Channel class type used for instantiating channels in this device family. Overridden in subclasses."""

    MAX_CHANNEL_COUNT = 0
    """Maximum number of channels supported by this device family. Overridden in subclasses."""

    CACHEABLE_COMMANDS = [
        "light",
        "encmode",
        "enctime",
        "enclim",
        "encexp",
        "encstol",
        "setk",
        "monwpa",
    ]
    """Commands whose responses can be cached to optimize performance."""

    BACKUP_COMMANDS = [
        "light",
        "encmode",
        "enctime",
        "enclim",
        "encexp",
        "encstol",
    ]

    ERROR_MAP = {
        11: ErrorCode.UNKNOWN_COMMAND,
        15: ErrorCode.UNKNOWN_CHANNEL,
        16: ErrorCode.UNKNOWN_CHANNEL,
        17: ErrorCode.PARAMETER_MISSING,
        18: ErrorCode.ADMISSIBLE_PARAMETER_RANGE_EXCEEDED,
        25: ErrorCode.ACTUATOR_NOT_CONNECTED
    }

    FRAME_DELIMITER_WRITE = TransportProtocol.CR
    FRAME_DELIMITER_READ = TransportProtocol.XON

    SERIAL_BAUDRATE = 19200
    """Baudrate for serial communication during device identification. NV Family devices respond at 19200 baud."""

    @classmethod
    async def _is_device_type(cls, tp: TransportProtocol) -> str | None:
        initial_baudrate = tp.get_property("baudrate")
        tp.set_property("baudrate", cls.SERIAL_BAUDRATE)

        try:
            await tp.write("\r")
            msg = await tp.read_until(cls.FRAME_DELIMITER_READ, timeout=1.0)
            
            tp.set_property("baudrate", initial_baudrate)
            return cls.NV_FAMILY_IDENTIFIER if (cls.NV_FAMILY_IDENTIFIER + ">") in msg else None
        except TimeoutError:
            print("No response received during device identification.")

            tp.set_property("baudrate", initial_baudrate)
            return None
    
    async def _discover_channels(self):
        self._channels = {}

        for channel_id in range(self.MAX_CHANNEL_COUNT):
            self._channels[channel_id] = self.NV_CHANNEL_TYPE(channel_id, self._write_channel)

    async def _handle_error(self, response):
        if not response.startswith("ErrorCode"):
            return
        
        try:
            parts = response.split(',', 1)
            error_code = int(parts[1])
            ErrorCode.raise_error(error_code)
        except Exception:
            ErrorCode.raise_error(ErrorCode.ERROR_NOT_SPECIFIED)

    @property
    def channels(self) -> dict[int, NVFamilyChannel]:
        return self._channels

    display: NVDisplay = CapabilityDescriptor(
        NVDisplay, {
            NVDisplay.CMD_BRIGHTNESS: "light",
        },
    )
