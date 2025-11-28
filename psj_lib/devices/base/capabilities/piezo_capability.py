from typing import Callable

type Command = str
type DeviceCommands = dict[str, str]
type Param = float | int | bool | str

type WriteCallback = Callable[[DeviceCommands, Command, list[Param] | None], list[str]]
type ProgressCallback = Callable[[int, int], None]


class PiezoCapability:
    def __init__(
        self, 
        write_cb: WriteCallback,
        device_commands: DeviceCommands,
    ):
        self._write_cb = write_cb
        self._device_commands = device_commands

    def _write(self, command: str, params: list[Param] | None = None) -> list[str]:
        return self._write_cb(self._device_commands, command, params)