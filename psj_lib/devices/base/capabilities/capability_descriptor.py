from typing import Self, overload

from .piezo_capability import DeviceCommands, PiezoCapability


class CapabilityDescriptor[T: PiezoCapability]:  # Python 3.12+ syntax
    def __init__(self, capability_class: type[T], device_commands: DeviceCommands, **kwargs):
        self.capability_class = capability_class
        self.device_commands = device_commands
        self.kwargs = kwargs
    
    def __set_name__(self, owner, name):
        self.attr_name = f"_{name}"
    
    @overload
    def __get__(self, instance: None, owner: type) -> Self: ...
    
    @overload  
    def __get__(self, instance: object, owner: type) -> T: ...
    
    def __get__(self, instance, owner) -> T | Self:
        if instance is None:
            return self
        
        if not hasattr(instance, self.attr_name):
            capability = self.capability_class(
                instance._capability_write,
                self.device_commands,
                **self.kwargs
            )
            setattr(instance, self.attr_name, capability)
        
        return getattr(instance, self.attr_name)