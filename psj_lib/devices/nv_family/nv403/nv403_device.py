from ...base.capabilities import CapabilityDescriptor, MultiPosition, MultiSetpoint
from ..nv_family_device import NVFamilyDevice
from ..capabilties.nv_knob import NVKnob
from .nv403_channel import NV403Channel

class NV403Device(NVFamilyDevice):
    DEVICE_ID = "NV40/3"

    NV_FAMILY_IDENTIFIER = "NV403"
    NV_CHANNEL_TYPE = NV403Channel
    
    MAX_CHANNEL_COUNT = 3

    @property
    def channels(self) -> dict[int, NV403Channel]:
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
    
    multi_setpoint: MultiSetpoint = CapabilityDescriptor(
        MultiSetpoint, {
            MultiSetpoint.CMD_SETPOINTS: "setall",
        },
        channel_count=MAX_CHANNEL_COUNT
    )

    multi_position: MultiPosition = CapabilityDescriptor(
        MultiPosition, {
            MultiPosition.CMD_POSITIONS: "measure",
        },
    )
