from ..base.piezo_device import PiezoDevice
from ..transport_protocol import TransportProtocol
from .d_drive_channel import DDriveChannel


class DDriveDevice(PiezoDevice):
    """
    Represents a D-Drive piezo device.
    """

    DEVICE_ID = "D-Drive"

    BACKUP_COMMANDS = set()
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
        "trgoffs",
        "recstride",
        "bright",
    }


    @classmethod
    async def _is_device_type(cls, tp: TransportProtocol) -> bool:
        """
        Checks if the connected device matches the d-drive device type.

        Args:
            tp (TransportProtocol): The transport protocol instance to check.

        Returns:
            bool: True if the device type matches, False otherwise.
        """
        # Check if the device returns the expected device string
        await tp.write("\n")
        msg = await tp.read_message()

        return "DSM V" in msg

    async def _discover_channels(self):
        response = await self.write_raw("stat")
        self._parse_channel_status(response)

    def _parse_channel_status(self, response: str):
        lines = response.split("\n")

        # Reset all channels
        self._channels = {
            0: None,
            1: None,
            2: None,
            3: None,
            4: None,
            5: None
        }

        # Go through every line in the response
        for line in lines:
            # Check if line is empty
            if len(line) == 0:
                continue

            index = line.find("stat,")

            # Check if channel was not detected
            if index < 0:
                continue

            # Extract channel number from detected channel
            index += len("stat,")
            channel_number = int(line[index])

            self.channels[channel_number] = DDriveChannel(
                channel_number, 
                self._write_channel
            )


    # Override to provide typed channels
    @property
    def channels(self) -> dict[int, DDriveChannel]:
        """Returns the device channels."""
        return self._channels