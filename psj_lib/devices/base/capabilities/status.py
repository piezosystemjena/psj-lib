from .piezo_capability import PiezoCapability


class StatusRegister:
    def __init__(self, value: list[str]) -> None:
        self._raw = value


class Status(PiezoCapability):
    CMD_STATUS = "STATUS"

    def __init__(
        self,
        write_cb,
        device_commands,
        register_type: type[StatusRegister]
    ) -> None:
        super().__init__(write_cb, device_commands)
        self._register_type = register_type

    async def get(self) -> None:
        response = await self._write(self.CMD_STATUS)
        return self._register_type(response[0])