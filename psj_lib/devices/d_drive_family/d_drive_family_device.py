"""Piezosystem Jena d-Drive modular piezo amplifier device implementation.

The d-Drive is a modular, expandable piezoelectric amplifier system designed
for high-precision nanopositioning. It features:

- 20-bit resolution with 50 kHz sampling rate (50 kSPS)
- 1 to 6 amplifier channels per system
- Digital PID controllers with several filter stages
- Integrated waveform generator (sine, triangle, rectangle, sweep, noise)
- Two-channel data recorder (500k maximum samples per channel)
- Modular architecture with hot-swappable amplifier modules
- RS-232/USB connectivity options

For detailed hardware specifications, refer to the d-Drive Instruction Manual.
(https://www.piezosystem.com/products/amplifiers/modular/50ma-300ma-ddrive-digital-systems/)
"""

from ..base.exceptions import ErrorCode
from ..base.piezo_device import PiezoDevice
from ..transport_protocol import TransportProtocol
from .d_drive_family_channel import DDriveFamilyChannel


class DDriveFamilyDevice(PiezoDevice):
    """Piezosystem Jena d-Drive modular amplifier system.
    
    Represents a complete d-Drive system with 1-6 amplifier channels.
    Each channel provides independent control of a piezoelectric actuator
    with digital PID control, waveform generation, and data recording.
    
    The d-Drive system features:
    - 20-bit resolution
    - 50 kHz sampling rate (20µs control loop period)
    - Digital PID controllers with feedforward
    - Multiple filter stages (notch, low-pass, error filter)
    - Integrated waveform generator (sine, triangle, rectangle, sweep, noise)
    - Two-channel data recorder (500k samples per channel)
    - Hardware trigger output
    - Analog monitor output
    - Modulation input
    
    Attributes:
        DEVICE_ID: Device type identifier string
        BACKUP_COMMANDS: Commands excluded from backup operations
        CACHEABLE_COMMANDS: Commands whose responses can be cached
    
    Example:
        >>> from psj_lib import DDriveDevice, TransportType
        >>> # Connect to d-Drive via serial port
        >>> device = DDriveDevice(TransportType.SERIAL, 'COM3')
        >>> await device.connect()
        >>> print(f"Found {len(device.channels)} channels")
        >>> 
        >>> # Access channel 0
        >>> channel = device.channels[0]
        >>> # Enable closed-loop control
        >>> await channel.closed_loop_controller.set(True)
        >>> # Move to position
        >>> await channel.setpoint.set(50.0)  # 50 µm
        >>> # Read actual position
        >>> pos = await channel.position.get()
        >>> print(f"Position: {pos:.3f} µm")
    
    Note:
        - System supports 1-6 channels (hardware dependent)
        - Channels are numbered 0-5
        - Not all channel numbers may be populated
        - Use device.channels dict to access available channels
    """

    DEVICE_ID = "d-Drive Family Device"
    """Device type identifier used for device discovery and type checking."""

    BACKUP_COMMANDS = set()
    """Global device commands to include in backup operations (currently none for d-Drive)."""

    D_DRIVE_IDENTIFIER = "INVALID_STRING"
    """Internal identifier string used to recognize different d-Drive family devices. Overridden in subclasses."""
    
    CACHEABLE_COMMANDS = {
        "acdescr",
        "acolmas",
        "acclmas",
        "set",
        "fan",
        "modon",
        "monsrc",
        "cl",
        "sr",
        "pcf",
        "errlpf",
        "elpor",
        "kp",
        "ki",
        "kd",
        "tf",
        "notchon",
        "notchf",
        "notchb",
        "lpon",
        "lpf",
        "gfkt",
        "gasin",
        "gosin",
        "gfsin",
        "gatri",
        "gotri",
        "gftri",
        "gstri",
        "garec",
        "gorec",
        "gfrec",
        "gsrec",
        "ganoi",
        "gonoi",
        "gaswe",
        "goswe",
        "gtswe",
        "sct",
        "trgss",
        "trgse",
        "trgsi",
        "trglen",
        "trgedge",
        "trgsrc",
        "trgos",
        "recstride",
        "bright",
    }
    """Commands whose responses can be cached for performance optimization.
    
    These commands return relatively static configuration values that don't
    change frequently. Caching reduces communication overhead for reads.
    """

    DEFAULT_TIMEOUT_SECS = 0.5
    FRAME_DELIMITER_WRITE = TransportProtocol.CRLF
    FRAME_DELIMITER_READ = TransportProtocol.XON

    ERROR_MAP = {
        "command not found": ErrorCode.UNKNOWN_COMMAND,
        "command mismatch": ErrorCode.COMMAND_PARAMETER_COUNT_EXCEEDED,
        " not present": ErrorCode.UNKNOWN_CHANNEL,
        "unit not available": ErrorCode.ACTUATOR_NOT_CONNECTED,
    }

    FRAME_DELIMITER_MAP = {
        "ktemp": TransportProtocol.CR,
        "m": TransportProtocol.CR,
        "u": TransportProtocol.CR,
        "modon": TransportProtocol.CR,
        "monsrc": TransportProtocol.CR,
        "pcf": TransportProtocol.CR,
        "errlpf": TransportProtocol.CR,
        "elpor": TransportProtocol.CR,
        "sr": TransportProtocol.CR,
        "kp": TransportProtocol.CR,
        "ki": TransportProtocol.CR,
        "kd": TransportProtocol.CR,
        "tf": TransportProtocol.CR,
        "notchon": TransportProtocol.CR,
        "notchf": TransportProtocol.CR,
        "notchb": TransportProtocol.CR,
        "lpon": TransportProtocol.CR,
        "lpf": TransportProtocol.CR,
        "gfkt": TransportProtocol.CR,
        "gasin": TransportProtocol.CR,
        "gosin": TransportProtocol.CR,
        "gfsin": TransportProtocol.CR,
        "gatri": TransportProtocol.CR,
        "gotri": TransportProtocol.CR,
        "gftri": TransportProtocol.CR,
        "gstri": TransportProtocol.CR,
        "garec": TransportProtocol.CR,
        "gorec": TransportProtocol.CR,
        "gfrec": TransportProtocol.CR,
        "gsrec": TransportProtocol.CR,
        "ganoi": TransportProtocol.CR,
        "gonoi": TransportProtocol.CR,
        "gaswe": TransportProtocol.CR,
        "goswe": TransportProtocol.CR,
        "gtswe": TransportProtocol.CR,
        "sct": TransportProtocol.CR,
        "trgss": TransportProtocol.CR,
        "trgse": TransportProtocol.CR,
        "trgsi": TransportProtocol.CR,
        "trglen": TransportProtocol.CR,
        "trgedge": TransportProtocol.CR,
        "trgsrc": TransportProtocol.CR,
        "trgos": TransportProtocol.CR,
    }

    @classmethod
    async def _is_device_type(cls, tp: TransportProtocol) -> str | None:
        """Check if connected device is a d-Drive amplifier.
        
        Sends a probe command and checks the response for d-Drive identification.
        This is used during device discovery to identify d-Drive systems.

        Args:
            tp: Transport protocol instance connected to device

        Returns:
            Device ID string if device responds as d-Drive system, None otherwise
        
        Note:
            - Checks for string "DSM V" in response
            - This is an internal method used by device factory
        """
        # Check if the device returns the expected device string
        try:
            await tp.write("\r\n")
            msg = await tp.read_message()
            return cls.DEVICE_ID if (cls.D_DRIVE_IDENTIFIER + " V") in msg else None
        except TimeoutError as e:
            return None
        
    def _parse_response(self, response: str) -> list[str]:
        """"""
        # Check for error strings in response
        for err_str, err_code in self.ERROR_MAP.items():
            if err_str in response.lower():
                ErrorCode.raise_error(err_code)

        # Default parsing (comma-separated values)
        return super()._parse_response(response)

    async def write_raw(
        self, 
        cmd, 
        timeout: float = DEFAULT_TIMEOUT_SECS, 
        rx_delimiter: bytes = FRAME_DELIMITER_READ
    ) -> str:
        # Override frame delimiter if command has specific mapping (but only for reading or "m" or "u" commands)
        if cmd.count(",") <= 1 or cmd.startswith(("m,", "u,")):
            raw_cmd = cmd.split(",")[0].lower()
        
            if raw_cmd in self.FRAME_DELIMITER_MAP:
                rx_delimiter = self.FRAME_DELIMITER_MAP[raw_cmd]

        return await super().write_raw(cmd, timeout, rx_delimiter)

    # Override to provide typed channels
    @property
    def channels(self) -> dict[int, DDriveFamilyChannel]:
        """Get dictionary of available d-Drive amplifier channels.
        
        Returns:
            Dictionary mapping channel number (0-5) to DDriveFamilyChannel instance,
            or None for unpopulated slots
        
        Example:
            >>> # Iterate over all available channels
            >>> for ch_num, channel in device.channels.items():
            ...     if channel is not None:
            ...         pos = await channel.position.get()
            ...         print(f"Channel {ch_num}: {pos} µm")
            >>> 
            >>> # Access specific channel
            >>> if device.channels[0] is not None:
            ...     await device.channels[0].setpoint.set(75.0)
        
        Note:
            - Channel numbers 0-5
            - None values indicate empty amplifier slots
            - Check for None before accessing channel
        """
        return self._channels