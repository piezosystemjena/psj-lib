from ...base.capabilities import CapabilityDescriptor
from ..nv_family_device import NVFamilyDevice
from ..capabilties.nv_knob import NVCLEKnob
from .nv120_cle_channel import NV120CLEChannel

class NV120CLEDevice(NVFamilyDevice):
    """Device class for NV120CLE closed-loop amplifier.

    Single-channel NV family device with additional closed-loop channel
    capabilities.

    Example:
        >>> device = NV120CLEDevice(TransportType.SERIAL, "COM10")
        >>> async with device:
        ...     channel = device.channels[0]
        ...     await channel.closed_loop_controller.set(True)
        ...     await channel.setpoint.set(8.0)
    """

    DEVICE_ID = "NV120CLE"
    
    NV_FAMILY_IDENTIFIER = "NV120CLE"
    NV_CHANNEL_TYPE = NV120CLEChannel
    
    MAX_CHANNEL_COUNT = 1

    @property
    def channels(self) -> dict[int, NV120CLEChannel]:
        """Typed channel mapping for NV120CLE."""
        return self._channels

    knob: NVCLEKnob = CapabilityDescriptor(
        NVCLEKnob, {
            NVCLEKnob.CMD_MODE: "encmode",
            NVCLEKnob.CMD_SAMPLE_TIME: "enctime",
            NVCLEKnob.CMD_STEP_LIMIT: "enclim",
            NVCLEKnob.CMD_ACCEL_EXPONENT: "encexp",
            NVCLEKnob.CMD_STEP_OPEN_LOOP: "encstol",
            NVCLEKnob.CMD_STEP_CLOSED_LOOP: "encstcl",
        }
    )
    """Front-panel encoder knob configuration (including CLE step setting)."""
