from ...base.capabilities import CapabilityDescriptor, MultiPosition, MultiSetpoint
from ..nv_family_device import NVFamilyDevice
from ..capabilties.nv_knob import NVCLEKnob
from .nv403_cle_channel import NV403CLEChannel

class NV403CLEDevice(NVFamilyDevice):
    DEVICE_ID = "NV40/3CLE"
    
    NV_FAMILY_IDENTIFIER = "NV403CLE"
    NV_CHANNEL_TYPE = NV403CLEChannel

    MAX_CHANNEL_COUNT = 3

    @property
    def channels(self) -> dict[int, NV403CLEChannel]:
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
