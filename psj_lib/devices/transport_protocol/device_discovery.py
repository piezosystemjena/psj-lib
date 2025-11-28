"""
This module provides asynchronous device discovery functionality for the NV200 library.
It concurrently scans for devices available via Telnet and Serial protocols, returning
a unified list of detected devices. Each detected device is represented by a :class:`.DetectedDevice`
instance, annotated with its transport type (TELNET or SERIAL), identifier (such as IP address
or serial port), and optionally a MAC address.
"""

import asyncio
import logging
from enum import Flag, auto
from typing import List, Optional

from .transport_protocol import TRANSPORT_REGISTRY, DiscoveryCallback, TransportType
from .transport_types import DetectedDevice

# Global module locker
logger = logging.getLogger(__name__)

class DiscoverFlags(Flag):
    """
    Flags to configure the behavior of the device discovery process.

    These flags can be combined using the bitwise OR (``|``) operator.

    Attributes:
        DETECT_SERIAL: Enables detection of serial devices.
        DETECT_ETHERNET: Enables detection of ethernet devices.
        READ_DEVICE_INFO: Enriches discovered devices with additional information such as actuator name and actuator serial number.
        ADJUST_COMM_PARAMS: Automatically adjusts communication parameters for discovered devices. This may take some
           additional time, as it may involve reading and writing to the device or even resetting it.
        ALL: Enables all discovery actions (serial, ethernet, and enrichment).
    """
    DETECT_SERIAL = auto()
    DETECT_ETHERNET = auto()
    ADJUST_COMM_PARAMS = auto()  # Adjust communication parameters automatically
    ALL_INTERFACES = DETECT_SERIAL | DETECT_ETHERNET
    ALL = ALL_INTERFACES | ADJUST_COMM_PARAMS

    @staticmethod
    def flags_for_transport(transport: Optional[TransportType] = None) -> 'DiscoverFlags':
        """
        Maps a TransportType to the appropriate DiscoverFlags.

        Args:
            transport: The transport type (e.g., SERIAL or TELNET)

        Returns:
            DiscoverFlags corresponding to the selected transport type.
        """
        if transport is None:
            return DiscoverFlags.ALL_INTERFACES
        elif transport == TransportType.SERIAL:
            return DiscoverFlags.DETECT_SERIAL
        elif transport == TransportType.TELNET:
            return DiscoverFlags.DETECT_ETHERNET
        else:
            raise ValueError(f"Unsupported transport type: {transport}")


class DeviceDiscovery:
    """
    A class providing asynchronous device discovery functionality for NV200 devices.
    It scans for devices available via Telnet and Serial protocols, returning a unified
    list of detected devices.
    """
    @staticmethod
    async def discover_devices(
        discovery_cb: DiscoveryCallback,
        flags: DiscoverFlags = DiscoverFlags.ALL_INTERFACES,
    ) -> List[DetectedDevice]:
        """
        Asynchronously discovers devices on available interfaces based on the specified discovery flags and optional device class.

        The discovery process can be customized using flags to enable or disable:

        - `DiscoverFlags.DETECT_ETHERNET` - detect devices connected via Ethernet
        - `DiscoverFlags.DETECT_SERIAL` - detect devices connected via Serial
        - `DiscoverFlags.READ_DEVICE_INFO` - enrich device information with additional details such as actuator name and actuator serial number    

        Args:
            flags (DiscoverFlags, optional): Flags indicating which interfaces to scan and whether to read device info. Defaults to DiscoverFlags.ALL_INTERFACES.
            device_class (Optional[Type[PiezoDeviceBase]], optional): If specified, only devices matching this class will be returned. Also ensures device info is read.

        Returns:
            List[DetectedDevice]: A list of detected devices, optionally enriched with detailed information and filtered by device class.

        Raises:
            Any exceptions raised by underlying protocol discovery or enrichment functions.

        Notes:
            - Device discovery is performed in parallel for supported interfaces (Ethernet, Serial).
            - If READ_DEVICE_INFO is set, each detected device is enriched with additional information.
            - If device_class is specified, only devices matching the class's DEVICE_ID are returned.

        Examples:
            Discover all Devices on all interfaces

            >>> device = await nv200.device_discovery.discover_devices(DiscoverFlags.ALL_INTERFACES | DiscoverFlags.READ_DEVICE_INFO)

            Discover NV200 Devices connected via serial interface

            >>> device = await nv200.device_discovery.discover_devices(DiscoverFlags.DETECT_SERIAL | DiscoverFlags.READ_DEVICE_INFO, NV200Device)
        """

        devices: List[DetectedDevice] = []

        # Create discovery tasks for each enabled transport type
        tasks = [
            protocol.discover_devices(discovery_cb)
            for transport_type, protocol in TRANSPORT_REGISTRY.items()
            if flags & DiscoverFlags.flags_for_transport(transport_type)
        ]

        # Run all discovery tasks concurrently and gather results
        results = await asyncio.gather(*tasks)

        for result in results:
            devices.extend(result)

        return devices