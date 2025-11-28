"""
Command cache for piezo devices to reduce redundant read operations.
"""

import logging
from typing import Dict, Optional, Set

logger = logging.getLogger(__name__)


class CommandCache:
    """
    A cache for device commands to reduce redundant read operations over
    the communication interface.
    
    This cache stores command responses and only serves cached values for
    commands marked as cacheable. It supports individual command invalidation
    and full cache clearing.
    
    Warning:
        Caching should only be used when no other external application modifies
        the device state in parallel, as this can lead to stale cached data.
    """
    
    def __init__(self, cacheable_commands: Set[str], enabled: bool = True):
        """
        Initialize the command cache.

        Args:
            cacheable_commands: Set of command names that are allowed to be cached
            enabled: Whether caching is enabled (default: True)
        """
        self._cache: Dict[str, list[str]] = {}
        self._cacheable_commands = cacheable_commands
        self._enabled = enabled

    @property
    def enabled(self) -> bool:
        """Returns whether caching is enabled."""
        return self._enabled

    @enabled.setter
    def enabled(self, value: bool) -> None:
        """
        Enable or disable caching.
        
        Args:
            value: True to enable, False to disable
        """
        self._enabled = value
        if not value:
            self.clear()

    def is_cacheable(self, cmd: str) -> bool:
        """
        Check if a command can be cached.

        Args:
            cmd: The command string

        Returns:
            True if the base command is in the cacheable commands set
        """
        # Check exact match
        if cmd in self._cacheable_commands:
            return True

        # Check for base command match (before any commas)
        base_cmd = cmd.split(",")[0]
        return base_cmd in self._cacheable_commands

    def get(self, cmd: str) -> Optional[list[str]]:
        """
        Retrieve cached values for a command.
        
        Args:
            cmd: The command string
            
        Returns:
            Cached response values if available and caching is enabled,
            None otherwise
        """
        if not self._enabled:
            return None

        if cmd in self._cache:
            logger.debug(f"Cache hit for command: {cmd} -> {self._cache[cmd]}")
            return self._cache[cmd]

        return None

    def set(self, cmd: str, values: list[str]) -> None:
        """
        Store values in cache for a command.
        
        Args:
            cmd: The command string
            values: The response values to cache
        """
        if not self._enabled:
            return
            
        if not self.is_cacheable(cmd):
            logger.debug(f"Command {cmd} is not cacheable, skipping cache")
            return
        
        self._cache[cmd] = values
        logger.debug(f"Cached values for {cmd}: {values}")
    
    
    def invalidate(self, cmd: str) -> None:
        """
        Invalidate (remove) a specific command from the cache.
        
        Args:
            cmd: The command string to invalidate
        """
        if cmd in self._cache:
            del self._cache[cmd]
            logger.debug(f"Invalidated cache for command: {cmd}")
    
    
    def invalidate_pattern(self, prefix: str) -> None:
        """
        Invalidate all cached commands starting with a given prefix.
        
        Useful when a write operation affects multiple related parameters.
        
        Args:
            prefix: Command prefix to match
        """
        invalidated = [cmd for cmd in self._cache.keys() if cmd.startswith(prefix)]
        for cmd in invalidated:
            del self._cache[cmd]
        
        if invalidated:
            logger.debug(f"Invalidated {len(invalidated)} commands with prefix '{prefix}'")
    
    
    def clear(self) -> None:
        """Clear all cached values."""
        self._cache.clear()
        logger.debug("Command cache cleared")
    
    
    def __len__(self) -> int:
        """Returns the number of cached entries."""
        return len(self._cache)
    
    
    def __contains__(self, cmd: str) -> bool:
        """Check if a command is in the cache."""
        return cmd in self._cache
    
    
    def __repr__(self) -> str:
        return f"CommandCache(enabled={self._enabled}, size={len(self._cache)})"