# psj-lib AI Agent Instructions

## Project Overview
Python library for piezoelectric amplifier control (d-Drive and future devices) by piezosystem jena GmbH. Built on async/await pattern with modular capability architecture.

## Architecture

### Three-Layer Hierarchy
```
PiezoDevice (e.g., DDriveDevice)
  ├─ Transport protocol (serial/Telnet) with command caching
  └─ PiezoChannels (e.g., DDriveChannel)
      └─ Capabilities (Position, PID, WaveformGenerator, etc.)
```

### Key Design Patterns

**Capability-Based Architecture**: Features are modular `PiezoCapability` subclasses, declared as `CapabilityDescriptor` class attributes on channels for lazy initialization. Example:
```python
class DDriveChannel(PiezoChannel):
    position = CapabilityDescriptor(Position, {Position.CMD_POSITION: "pos"})
    pid_controller = CapabilityDescriptor(PIDController, {...})
```

**Device Registration**: Devices auto-register by setting `DEVICE_ID` class attribute (e.g., `DEVICE_ID = "D-Drive"`), populating `DEVICE_MODEL_REGISTRY` via `__init_subclass__`. Used by `DeviceFactory` for discovery-based instantiation.

**Command Caching**: `CommandCache` stores read responses to reduce serial/Telnet latency. Only commands in `CACHEABLE_COMMANDS` set are cached; writes auto-invalidate. Enable/disable per-instance via `enable_cmd_cache()`. **Critical**: Disable if multiple applications access same device.

**Async Everywhere**: All device I/O is async. Use `asyncio.run(main())` pattern in examples. Context manager support via `async with device:` for auto-connect/disconnect.

## Project-Specific Conventions

### Async Patterns
- Always use `await` for device operations: `await channel.position.get()`
- Standard entry point: `asyncio.run(main())` 
- Cleanup pattern: `async with device:` or explicit `try/finally` with `device.disconnect()`

### Type Annotations
- Modern Python 3.12+ syntax: `type ChannelID = int`, generics as `[T: PiezoCapability]`
- All public APIs fully type-hinted for IDE support

### Command Protocol
- Commands are device-specific strings (e.g., `"pos"`, `"kp"`) mapped in `CapabilityDescriptor` 
- Format: `cmd,channel_id,param1,param2,...\r\n` (CRLF delimiter)
- Responses parsed in `PiezoDevice.write()` method

### Error Handling
- Device errors inherit from `DeviceError` (see `psj_lib/devices/base/exceptions.py`)
- Common errors: `UnknownCommand`, `ParameterMissing`, `AdmissibleParameterRangeExceeded`
- Transport errors: `DeviceUnavailableException`, `TimeoutException`, `ProtocolException`

## Developer Workflows

### Building Documentation
```bash
# Primary method (from project root):
poetry run sphinx-build -b html doc/ doc/_build/

# Alternative (from doc/ directory):
./make.bat html  # Windows only

# View: open doc/_build/index.html
```

### Testing & Validation
- No automated tests currently (manual testing with hardware)
- Examples in `examples/` serve as integration tests
- Run example: `poetry run python examples/01_device_discovery_and_connection.py`

### Adding New Devices
**Must-read**: `psj_lib/devices/ADDING_NEW_DEVICES.md` (1000+ lines, step-by-step guide)

Quick checklist:
1. Create `psj_lib/devices/new_device/` with `new_device_device.py`, `new_device_channel.py`
2. Set `DEVICE_ID` class attribute for auto-registration
3. Define capabilities as `CapabilityDescriptor` attributes on channel
4. Implement device-specific capabilities in `capabilities/` subfolder
5. Export public API in `__init__.py` and `psj_lib/__init__.py`
6. Update `CACHEABLE_COMMANDS` and `BACKUP_COMMANDS` sets

### Dependency Management
- Poetry for all dependencies (`pyproject.toml`)
- Dev dependencies: Sphinx + themes for documentation
- Runtime: `aioserial`, `telnetlib3`, `psutil`
- Version: Dynamic from git tags via `poetry-dynamic-versioning`

### Publishing
- PyPI package name: `psj-lib`
- Readme: `README_PYPI.md` (minimal), `README.md` (full)
- Classifiers indicate production stability

## Critical Implementation Details

### Transport Layer (`devices/transport_protocol/`)
- **Internal API**: Not exposed to end users except types (`TransportType`, `DiscoverFlags`)
- Discovery via `DeviceDiscovery.discover_devices()` - runs concurrently across serial/Telnet
- Serial: Auto-detects FTDI USB adapters (115200 baud, no flow control)
- Telnet: UDP broadcast discovery of Lantronix XPORT modules, auto-configures flow control

### Reentrant Locking
- `_ReentrantAsyncLock` in `_internal/` allows same task to acquire lock multiple times
- All device operations auto-locked; use `async with device.lock:` for multi-command atomicity

### Channel Discovery Pattern
Devices must implement `_discover_channels()` to populate `self._channels` dict. Example from d-Drive:
```python
async def _discover_channels(self):
    response = await self.write("chnrall", [])
    channel_ids = [int(ch) for ch in response]
    for ch_id in channel_ids:
        self._channels[ch_id] = DDriveChannel(ch_id, self._channel_write_cb)
```

### Backup/Restore
- Commands in `BACKUP_COMMANDS` (device-level) and `PiezoChannel.BACKUP_COMMANDS` are saved/restored
- Format: `{channel_id: {cmd: [params], ...}, ...}` dictionary
- Use `await device.backup()` / `await device.restore(backup_data)`

## File Structure Conventions

### Public vs Internal
- **Public**: `psj_lib/__init__.py` exports, `devices/base/capabilities/`, `devices/d_drive/`
- **Internal**: `_internal/`, `devices/base/command_cache.py`, `devices/transport_protocol/` (except types)
- Users import from top-level: `from psj_lib import DDriveDevice, PiezoChannel`

### Naming Conventions
- Device classes: `{Name}Device` (e.g., `DDriveDevice`)
- Channel classes: `{Name}Channel` (e.g., `DDriveChannel`)
- Capabilities: Descriptive nouns (`Position`, `PIDController`, `WaveformGenerator`)
- Device-specific capabilities: Prefix with device name (`DDriveStatusRegister`)

### Documentation
- Google-style docstrings with comprehensive examples
- Sphinx + RTD theme + dark mode
- API reference auto-generated from docstrings
- Manual pages: `doc/*.rst` (getting_started, api, examples, etc.)

## Common Pitfalls

1. **Forgetting `await`**: All device methods are async - missing `await` returns coroutine, not value
2. **Caching with shared access**: Disable cache if multiple apps access device simultaneously
3. **Not using lock for atomicity**: Multi-command sequences need explicit `async with device.lock:`
4. **Transport types**: Serial uses port names (`COM3`, `/dev/ttyUSB0`); Telnet uses IP addresses
5. **DEVICE_ID registration**: Must be exact match for discovery - case-sensitive string comparison
6. **Channel numbering**: Zero-based, but not all numbers may exist (sparse array)

## Quick Reference

### Discovery & Connection
```python
devices = await PiezoDevice.discover_devices(DiscoverFlags.ALL_INTERFACES)
device = devices[0]
await device.connect()
channel = device.channels[0]
```

### Capability Access Pattern
```python
await channel.setpoint.set(50.0)           # Write
position = await channel.position.get()     # Read
await channel.pid_controller.set(p=10, i=5, d=0.5)  # Multi-param
```

### Data Recorder & Waveform
```python
# Configure 1-second capture at 50kHz
await channel.data_recorder.set(memory_length=50000, stride=1)
data = await channel.data_recorder.capture()  # Returns dict with ch1/ch2 arrays

# Generate sine wave
await channel.waveform_generator.sine.set(amplitude=20, offset=50, frequency=10)
```
