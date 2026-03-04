from typing import List, Awaitable

from ..base.piezo_channel import PiezoChannel
from ..base.capabilities import *
from .capabilties.nv_setpoint import NVSetpoint
from .capabilties.nv_modulation_source import NVModulationSource, NVModulationSourceTypes
from .capabilties.nv_monitor_output import NVMonitorOutputSource, NVMonitorOutput
from .capabilties.nv_status_register import NVStatusRegister

class NVFamilyChannel(PiezoChannel):
    BACKUP_COMMANDS = [
        "monwpa",
        "setk",
        "cloop"
    ]

    # Capability descriptors
    setpoint: NVSetpoint = CapabilityDescriptor(
        NVSetpoint, {
            NVSetpoint.CMD_SETPOINT: "set",
        }
    )

    position: Position = CapabilityDescriptor(
        Position, {
            Position.CMD_POSITION: "rk"
        }
    )

    modulation_source: NVModulationSource = CapabilityDescriptor(
        NVModulationSource, {
            NVModulationSource.CMD_SOURCE: "setk"
        },
        sources=NVModulationSourceTypes
    )

    monitor_output: NVMonitorOutput = CapabilityDescriptor(
        NVMonitorOutput, {
            NVMonitorOutput.CMD_OUTPUT_SRC: "monwpa"
        },
        sources=NVMonitorOutputSource
    )

    voltage_unit: Unit = CapabilityDescriptor(
        Unit, {
            Unit.CMD_UNIT: "unitol"
        }
    )

    voltage_limits: Limits = CapabilityDescriptor(
        Limits, {
            Limits.CMD_LOWER_LIMIT: "dspolmin",
            Limits.CMD_UPPER_LIMIT: "dspolmax"
        }
    )

    status: Status = CapabilityDescriptor(
        Status, {
            Status.CMD_STATUS: "ERROR"
        },
        register_type=NVStatusRegister,
    )
    
    async def _write(self, cmd: str, params: List[PiezoChannel.Param] | None) -> Awaitable[List[str]]:
        if not self._write_cb:
            raise RuntimeError("No write callback defined for this channel.")

        # Special handling for NV families ERROR command: 
        # Do not send channel ID for this command, as it is a global status register
        if cmd == "ERROR":
            return await self._write_cb(None, cmd, params)

        return await self._write_cb(self._channel_id, cmd, params)
