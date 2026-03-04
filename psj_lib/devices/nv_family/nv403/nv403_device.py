from ...base.capabilities import CapabilityDescriptor, MultiPosition, MultiSetpoint
from ..nv_family_device import NVFamilyDevice
from ..capabilties.nv_knob import NVKnob
from .nv403_channel import NV403Channel

class NV403Device(NVFamilyDevice):
    """Device class for NV40/3 open-loop 3-channel amplifier.

    Provides three channel instances plus coordinated multi-channel helpers.

    Example:
        >>> device = NV403Device(TransportType.SERIAL, "COM10")
        >>> async with device:
        ...     await device.multi_setpoint.set([10.0, 20.0, 30.0])
        ...     print(await device.multi_position.get())
    """

    DEVICE_ID = "NV40/3"

    NV_FAMILY_IDENTIFIER = "NV403"
    NV_CHANNEL_TYPE = NV403Channel
    
    MAX_CHANNEL_COUNT = 3

    @property
    def channels(self) -> dict[int, NV403Channel]:
        """Typed channel mapping for NV40/3."""
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
    """Front-panel encoder knob configuration."""
    
    multi_setpoint: MultiSetpoint = CapabilityDescriptor(
        MultiSetpoint, {
            MultiSetpoint.CMD_SETPOINTS: "setall",
        },
        channel_count=MAX_CHANNEL_COUNT
    )
    """Synchronous setpoint write for all three channels."""

    multi_position: MultiPosition = CapabilityDescriptor(
        MultiPosition, {
            MultiPosition.CMD_POSITIONS: "measure",
        },
    )
    """Single-command position readback for all three channels."""
