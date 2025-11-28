"""
Provides classes and enumerations for communicating with and interpreting responses from NV200 devices.

This module includes an asynchronous client for issuing commands and parsing responses
from NV200 devices over supported transport protocols (e.g., serial, Telnet).
"""

import logging
from typing import Awaitable, Self

from ..._internal._reentrant_lock import _ReentrantAsyncLock
from ..transport_protocol import (
    DeviceDiscovery,
    DeviceUnavailableException,
    DiscoverFlags,
    TransportFactory,
    TransportProtocol,
    TransportType,
)
from .command_cache import CommandCache
from .device_factory import DeviceFactory
from .exceptions import ErrorCode
from .piezo_channel import PiezoChannel
from .piezo_types import DeviceInfo

# Global module locker
logger = logging.getLogger(__name__)

DEVICE_MODEL_REGISTRY: dict[str, type["PiezoDevice"]] = {}


class PiezoDevice:
    """
    Generic piezosystem device base class.

    PiezoDeviceBase provides an asynchronous interface for communicating with a piezoelectric device
    over various transport protocols (such as serial or telnet). It encapsulates low-level device commands,
    response parsing, synchronization mechanisms, and optional command result caching.

    This class is intended to be subclassed by concrete device implementations (e.g., `NV200Device`),
    which define specific device behaviors and cacheable commands.

    Concrete device classes support caching of command parameters/values. This mechanism is designed 
    to reduce frequent read access over the physical communication interface by serving previously 
    retrieved values from a local cache. Since each read operation over the interface introduces latency, 
    caching can significantly improve the performance of parameter access — particularly in scenarios 
    like graphical user interfaces where many values are queried repeatedly.

    Note:
        Caching should only be used if it is guaranteed that no other external application modifies the 
        device state in parallel. For example, if access is made via the Python library over a Telnet 
        connection, no other software (e.g., via a serial interface) should modify the same parameters 
        concurrently. In such multi-access scenarios, caching can lead to inconsistent or outdated data. 
        To ensure correctness, disable caching globally by setting the class variable 
        `CMD_CACHE_ENABLED` to ``False``.

    Attributes:
        CMD_CACHE_ENABLED (bool): 
            Class-level flag that controls whether command-level caching is enabled. When set to True 
            (default), values read from or written to the device for cacheable commands will be stored 
            and retrieved from an internal cache. Setting this to ``False`` disables the caching 
            behavior globally for all instances unless explicitly overridden at the instance level.
    """
    DEVICE_ID = None  # Placeholder for device ID, to be set in subclasses

    CACHEABLE_COMMANDS: set[str] = set()  # set of commands that can be cached
    BACKUP_COMMANDS: set[str] = set()  # set of commands to backup device settings

    DEFAULT_TIMEOUT_SECS = 0.6
    FRAME_DELIMITER_WRITE = TransportProtocol.CRLF  # Default frame delimiter for writing commands
    FRAME_DELIMITER_READ = TransportProtocol.CRLF

    _channels: dict[int, PiezoChannel] = {}  # Dictionary to store channels by their number


    def __init__(
        self,
        transport_type: TransportType,
        identifier: str
    ):
        # Initialize transport
        self._transport: TransportProtocol = TransportFactory.from_transport_type(
            transport_type,
            identifier
        )

        self._cache: CommandCache = CommandCache(self.CACHEABLE_COMMANDS)
        self._lock = _ReentrantAsyncLock()
        self._transport.rx_delimiter = self.FRAME_DELIMITER_READ

    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        if cls.DEVICE_ID:
            DEVICE_MODEL_REGISTRY[cls.DEVICE_ID] = cls


    @classmethod
    async def discover_devices(cls, flags: DiscoverFlags = DiscoverFlags.ALL_INTERFACES) -> list[Self]:
        """
        Asynchronously discovers devices available via supported transport protocols.

        This method scans for devices connected through various transport protocols
        (e.g., serial, Telnet) and returns a unified list of detected devices.

        Returns:
            List[Self]: A list of PiezoDeviceBase instances representing the discovered devices.
        """
        discovered_devices = await DeviceDiscovery.discover_devices(flags, cls._is_device_type)
        devices = []

        for device in discovered_devices:
            devices.append(DeviceFactory.from_detected_device(device))

        return devices


    @classmethod
    async def _is_device_type(cls, tp: TransportProtocol) -> bool:
        """
        Checks if the connected device matches the expected device type. For base class,
        this method will run a check for every subclass.
        Override this in subclasses to implement specific device type checks.

        Args:
            tp (TransportProtocol): The transport protocol instance to check.

        Returns:
            bool: True if the device type matches, False otherwise.
        """

        if cls.DEVICE_ID is None:
            for subclass in DEVICE_MODEL_REGISTRY.values():
                if subclass._is_device_type(tp):
                    return True

            return False

    @property
    def lock(self) -> _ReentrantAsyncLock:
        """
        Lock that can be used by external code to synchronize access to the device.

        Use with ``async with client.lock:`` to group operations atomically.
        """
        return self._lock


    @property
    def device_info(self) -> DeviceInfo:
        """
        Returns detailed information about the connected device.

        This property provides a DeviceInfo object that includes
        the device's identifier and transport metadata. It requires
        that the transport layer is initialized and connected.

        Raises:
            RuntimeError: If the transport is not initialized or the device
                        is not connected.

        Returns:
            DeviceInfo: An object containing the device ID and transport info.
        """
        if self._transport is None or not self._transport.is_connected:
            raise DeviceUnavailableException("Cannot access device_info: transport is not initialized or device is not connected.")

        return DeviceInfo(
            device_id=self.DEVICE_ID,
            transport_info=self._transport.get_info()
        )

    @property
    def channels(self) -> dict[int, PiezoChannel]:
        """
        Returns a dictionary of available channels for the device.

        The keys are channel numbers (int), and the values are PiezoChannel instances.

        Returns:
            dict[int, PiezoChannel]: A dictionary mapping channel numbers to PiezoChannel instances.
        """
        return self._channels
    

    def _parse_response(self, response: str) -> list[str]:
        """
        Parses the response from the device and extracts the command and parameters.
        If the response indicates an error (starts with "error"), it raises a DeviceError
        with the corresponding error code. If the error code is invalid or unspecified,
        a default error code of 1 is used.
        Args:
            response (bytes): The response received from the device as a byte string.
        Returns:
            tuple: A tuple containing the command (str) and a list of parameters (list of str).
        Raises:
            DeviceError: If the response indicates an error.
        """
        # Check if the response indicates an error
        # TODO: Check d-drive error behavior
        if response.startswith("error"):
            self._raise_error(response)
            return  # This line will never be reached due to the exception being raised
            
        # Else, Normal response, split the command and parameters
        parts = response.split(',', 1)
        parameters = []

        if len(parts) > 1:
            parameters = [param.strip("\x01\n\r\x00") for param in parts[1].split(',')]

        return parameters
    

    def _raise_error(self, response: str):
        """
        Parses the response from the device and raises a DeviceError if an error is indicated.

        Args:
            response (str): The response received from the device as a string.
        Raises:
            DeviceError: If the response indicates an error.
        """
        parts = response.split(',', 1)
        
        # Check if error code is present
        if len(parts) < 2:
            ErrorCode.raise_error(ErrorCode.ERROR_NOT_SPECIFIED)  # Default error: Error not specified
            return

        # Try to parse the error code
        try:
            error_code = int(parts[1].strip("\x01\n\r\x00"))

            # Raise a DeviceError with the error code
            ErrorCode.raise_error(error_code)
            return
        except ValueError:
            # In case the error code isn't valid
            ErrorCode.raise_error(ErrorCode.ERROR_NOT_SPECIFIED)  # Default error: Error not specified
            return
        

    async def _discover_channels(self):
        """
        Asynchronously discovers and initializes channels for the device.

        This method must be overridden in subclasses to implement specific
        channel discovery logic based on the device's capabilities.
        """
        raise NotImplementedError("Channel discovery must be implemented in subclasses.")
    

    async def _write_channel(
        self,
        channel_id: int,
        cmd: str,
        params: list[int | float | str | bool] | None = None
    ) -> list[str]:
        full_cmd = f"{cmd},{channel_id}"

        return await self.write(full_cmd, params)

    async def _capability_write(
        self,
        device_commands: dict[str, str],
        cmd: str,
        params: list[int | float | str | bool]
    ):
        # Check if command can be found in cmd dictionary
        if cmd not in device_commands:
            logger.warning(f"Capability requested to send unknown command: {cmd}.")
            return
        
        return await self.write(device_commands[cmd], params)
    

    async def connect(self, auto_adjust_comm_params: bool = True):
        """
        Establishes a connection using the transport layer.

        This asynchronous method initiates the connection process by calling
        the `connect` method of the transport instance.

        Args:
            auto_adjust_comm_params (bool): If True, the Telnet transport will
                automatically adjust the internal communication parameters of
                the XPORT ethernet module. It will set the flow control mode to
                ``XON_XOFF_PASS_TO_HOST``. This is required for the library to work
                properly.

        Raises:
            Exception: If the connection fails, an exception may be raised
                       depending on the implementation of the transport layer.
        """
        if self._transport is None:
            raise DeviceUnavailableException("Cannot connect: transport is not initialized.")

        if self._transport.is_connected:
            logger.debug("Device is already connected.")
            return

        await self._transport.connect(auto_adjust_comm_params, self)
        is_match = await self._is_device_type()
        
        if not is_match:
            await self._transport.close()
            raise DeviceUnavailableException(
                f"Device type mismatch. Expected device ID: {self.DEVICE_ID}. "
                "Please check the device connection and ensure the correct device is connected."
            )
        
        await self._discover_channels()

    async def _write_and_parse(
        self,
        cmd: str,
        timeout: float = DEFAULT_TIMEOUT_SECS
    ) -> list[str]:
        response = await self.write_raw(cmd, timeout=timeout)
        return self._parse_response(response)

    async def _read_with_cache(
        self,
        cmd: str,
        timeout: float = DEFAULT_TIMEOUT_SECS
    ) -> list[str]:
        values = self._cache.get(cmd)

        if values is not None:
            return values

        logger.debug("Reading string values for command: %s", cmd)

        values = await self._write_and_parse(cmd, timeout=timeout)[1]

        for i in range(len(values)):
            values[i] = values[i].rstrip()  # strip trailing whitespace - some strings like units may contain trailing spaces

        self._cache.set(cmd, values)
        
        return values
    
    async def _write_with_cache(
        self,
        cmd: str,
        values: list[int | float | str | bool],
        timeout: float = DEFAULT_TIMEOUT_SECS
    ) -> list[str]:
        str_values = []

        # Convert all values to strings, handling booleans as integers
        for value in values:
            if isinstance(value, bool):
                str_values.append(str(int(value)))
            else:
                str_values.append(str(value))

        response = await self._write_and_parse(f"{cmd},{','.join(str_values)}", timeout=timeout)

        self._cache.set(cmd, str_values)

        return response
    

    async def write(
        self,
        cmd: str,
        params: list[int | float | str | bool] | None = None,
        timeout: float = DEFAULT_TIMEOUT_SECS
    ) -> list[str]:
        # If params is None, perform a read operation
        if params is None:
            return await self._read_with_cache(cmd, timeout=timeout)
        
        # Else, perform a write operation
        return await self._write_with_cache(cmd, params, timeout=timeout)
        
        
    async def write_raw(
        self,
        cmd: str,
        timeout: float = DEFAULT_TIMEOUT_SECS
    ) -> Awaitable[str]:
        logger.debug("Writing cmd.: %s", cmd)
        response = None

        if self._transport is None or not self._transport.is_connected:
            raise DeviceUnavailableException("Cannot write to device: transport is not initialized or device is not connected.")

        async with self.lock:
            try:
                await self._transport.write(cmd + self.FRAME_DELIMITER_WRITE)
                response = await self._transport.read_message(timeout=timeout)
            except Exception as e:
                raise DeviceUnavailableException(f"Failed to write/read from device: {e}") from e

        return response


    async def close(self):
        """
        Asynchronously closes the transport connection.

        This method ensures that the transport layer is properly closed,
        releasing any resources associated with it.
        """
        if self._transport is None or not self._transport.is_connected:
            logger.debug("Transport is already closed or not initialized.")
            return

        await self._transport.close()

    
    def clear_cmd_cache(self):
        """
        Clears the cache of previously issued commands.
        """
        self._cache.clear()
        logger.debug("Command cache cleared.")

    def enable_cmd_cache(self, enable: bool):
        """
        Enables or disables command caching for this device instance.

        Args:
            enable (bool): If True, enables command caching; if False, disables it.
        """
        self._cache.enabled = enable
        logger.debug(f"Command cache enabled: {enable}")

    async def backup(self, backup_list: list[str] | None = None) -> dict[str, str]:
        """
        Asynchronously backs up device settings by reading response parameters for each command in the provided list.

        Use the restore_parameters method to restore the settings later from the backup.

        Args:
            backup_list (list[str]): A list of command strings for which to back up settings.

        Returns:
            dict[str, str]: A dictionary mapping each command to its corresponding response string from the device.

        Example:
            >>> backup_list = [
            >>>     "modsrc", "notchon", "sr", "poslpon", "setlpon", "cl", "reclen", "recstr"]
            >>> await self.backup_settings(backup_list)
        """
        backup: dict[str, list[str]] = {}

        # Invalidate cache to make sure we read fresh values
        self.clear_cmd_cache()

        # Backup every channel
        for channel in self._channels.values():
            channel_backup = await channel.backup()

            for cmd, values in channel_backup.items():
                backup[f"{cmd},{channel.id}"] = values

        # Go through every command in the backup list and read its value
        for cmd in backup_list:
            backup[cmd] = await self.write(cmd)

        return backup

    async def restore(self, backup: dict[str, list[str]]):
        """
        Asynchronously restores device parameters from a backup created with `backup_parameters`.

        Iterates over the provided backup dictionary, writing each parameter value to the device.
        """
        for cmd, values in backup.items():
            await self.write(cmd, values)