from ..nv_family_channel import NVFamilyChannel
from ...base.capabilities import *

class NV120CLEChannel(NVFamilyChannel):
    """Single-channel closed-loop channel for NV120CLE devices.

    Extends :class:`NVFamilyChannel` with closed-loop specific capabilities.

    Example:
        >>> channel = device.channels[0]
        >>> await channel.closed_loop_controller.set(True)
        >>> await channel.setpoint.set(6.0)
        >>> print(await channel.closedloop_unit.get())
    """

    closed_loop_controller: ClosedLoopController = CapabilityDescriptor(
        ClosedLoopController, {
            ClosedLoopController.CMD_ENABLE: "cloop",
        },
        sample_period=0
    )
    """Closed-loop feedback control enable/disable."""

    closedloop_unit: Unit = CapabilityDescriptor(
        Unit, {
            Unit.CMD_UNIT: "unitcl"
        }
    )
    """Closed-loop unit readback capability."""

    closedloop_limits: Limits = CapabilityDescriptor(
        Limits, {
            Limits.CMD_LOWER_LIMIT: "dspclmin",
            Limits.CMD_UPPER_LIMIT: "dspclmax"
        }
    )
    """Closed-loop lower and upper limit queries."""
    