import logging
from typing import Awaitable, Callable, List, Optional

# Global module locker
logger = logging.getLogger(__name__)


class PiezoChannel:
    type ChannelID = int
    type Command = str
    type Param = float | int | bool | str
    type WriteCallback = Callable[
        [Command, List[Param], ChannelID], 
        Awaitable[List[Param]]
    ]

    BACKUP_COMMANDS: set[str] = set()  # Commands to backup channel settings

    def __init__(self, channel_id: int, write_cb: WriteCallback):
        self._channel_id = channel_id
        self._write_cb = write_cb

    async def _write(self, cmd: str, params: Optional[List[Param]]) -> Awaitable[List[str]]:
        if not self._write_cb:
            raise RuntimeError("No write callback defined for this channel.")

        return await self._write_cb(cmd, params, self._channel_id)

    async def _capability_write(
        self,
        device_commands: dict[str, str],
        cmd: Command,
        params: list[Param]
    ) -> list[str]:
        # Check if command can be found in cmd dictionary
        if cmd not in device_commands:
            logger.warning(f"Capability requested to send unknown command: {cmd}.")
            return
        
        return await self._write(cmd, params)

    async def backup(self) -> dict[str, list[str]]:
        """Backup current channel settings. Can later be restored using the channels Device class."""
        backup: dict[str, list[str]] = {}

        for cmd in self.BACKUP_COMMANDS:
            result = await self._write(cmd, None)
            backup[cmd] = result

        return backup
    
    @property
    def id(self) -> int:
        """Returns the channel ID."""
        return self._channel_id