from ...base.capabilities import CapabilityDescriptor
from ..capabilties.nv_knob import NVKnob
from ..nv_family_device import NVFamilyDevice
from .nv120_channel import NV120Channel

class NV120Device(NVFamilyDevice):
    """Device class for NV120/1 open-loop amplifier.

    Single-channel NV family device with open-loop channel capabilities.

    Example:
        >>> device = NV120Device(TransportType.SERIAL, "COM10")
        >>> async with device:
        ...     channel = device.channels[0]
        ...     await channel.setpoint.set(15.0)
        ...     print(await channel.position.get())
    """

    DEVICE_ID = "NV120/1"
    
    NV_FAMILY_IDENTIFIER = "NV120"
    NV_CHANNEL_TYPE = NV120Channel

    MAX_CHANNEL_COUNT = 1

    @property
    def channels(self) -> dict[int, NV120Channel]:
        """Typed channel mapping for NV120/1."""
        return self._channels

    knob: NVKnob = CapabilityDescriptor(
        NVKnob, {
            NVKnob.CMD_MODE: "encmode",
            NVKnob.CMD_SAMPLE_TIME: "enctime",
            NVKnob.CMD_STEP_LIMIT: "enclim",
            NVKnob.CMD_ACCEL_EXPONENT: "encexp",
            NVKnob.CMD_STEP_OPEN_LOOP: "encstol",
        }
    )
    """Front-panel encoder knob configuration.

    Supports mode, timing, acceleration and open-loop step settings.
    """