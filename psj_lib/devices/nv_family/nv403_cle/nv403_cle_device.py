from ...base.capabilities import CapabilityDescriptor, MultiPosition, MultiSetpoint
from ..nv_family_device import NVFamilyDevice
from ..capabilities.nv_knob import NVCLEKnob
from .nv403_cle_channel import NV403CLEChannel

class NV403CLEDevice(NVFamilyDevice):
    """Device class for NV40/3CLE closed-loop 3-channel amplifier.

    Provides three closed-loop capable channels and coordinated multi-channel
    helper capabilities.

    Example:
        >>> device = NV403CLEDevice(TransportType.SERIAL, "COM10")
        >>> async with device:
        ...     ch0 = device.channels[0]
        ...     await ch0.closed_loop_controller.set(True)
        ...     await device.multi_setpoint.set([5.0, 10.0, 15.0])
    """

    DEVICE_ID = "NV40/3CLE"
    
    NV_FAMILY_IDENTIFIER = "NV403CLE"
    NV_CHANNEL_TYPE = NV403CLEChannel

    MAX_CHANNEL_COUNT = 3

    @property
    def channels(self) -> dict[int, NV403CLEChannel]:
        """Typed channel mapping for NV40/3CLE."""
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
    """Front-panel encoder knob configuration including closed-loop step size."""
    
    multi_setpoint: MultiSetpoint = CapabilityDescriptor(
        MultiSetpoint, {
            MultiSetpoint.CMD_SETPOINTS: "setall",
        },
        channel_count=MAX_CHANNEL_COUNT
    )
    """Synchronous setpoint write for all three channels.
    
    Note: To use this capability, all 3 channels must have an actuator connected and their modulation mode
    set to SERIAL. Otherwise, the amplifier will ignore the command.
    """

    multi_position: MultiPosition = CapabilityDescriptor(
        MultiPosition, {
            MultiPosition.CMD_POSITIONS: "measure",
        },
    )
    """Single-command position readback for all three channels."""
