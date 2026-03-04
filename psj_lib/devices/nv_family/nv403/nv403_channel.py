from ..nv_family_channel import NVFamilyChannel

class NV403Channel(NVFamilyChannel):
    """Open-loop channel model used by NV40/3 devices.

    Each NV40/3 channel exposes the shared NV channel capabilities for
    open-loop operation.

    Example:
        >>> ch1 = device.channels[1]
        >>> await ch1.setpoint.set(18.0)
        >>> print(await ch1.openloop_unit.get())
    """

    pass 