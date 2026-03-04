from .piezo_capability import PiezoCapability

class Limits(PiezoCapability):
    CMD_UPPER_LIMIT = "UPPER_LIMIT"
    CMD_LOWER_LIMIT = "LOWER_LIMIT"

    async def get_lower(self) -> float:
        """Get the lower limit for the specified capability.
        
        Returns:
            The lower limit value as a float.
        """
        result = await self._write(self.CMD_LOWER_LIMIT)

        try:
            return float(result[0])
        except Exception:
            return float('nan')

    async def get_upper(self) -> float:
        """Get the upper limit for the specified capability.
        
        Returns:
            The upper limit value as a float.
        """
        result = await self._write(self.CMD_UPPER_LIMIT)
        
        try:
            return float(result[0])
        except Exception:
            return float('nan')
    
    async def get_range(self) -> tuple[float, float]:
        """Get the lower and upper limits as a tuple.
        
        Returns:
            A tuple containing (lower_limit, upper_limit).
        """
        lower = await self.get_lower()
        upper = await self.get_upper()
        return (lower, upper)