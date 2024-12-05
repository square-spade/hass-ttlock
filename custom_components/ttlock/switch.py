from __future__ import annotations

from typing import Any

from homeassistant.components.switch import SwitchEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from .coordinator import lock_coordinators
from .entity import BaseLockEntity


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up all the locks for the config entry."""

    async_add_entities(
        [
            entity
            for coordinator in lock_coordinators(hass, entry)
            for entity in (
                LockAutoLock(coordinator),
            )
        ]
    )
    
class LockAutoLock(BaseLockEntity, SwitchEntity):
    """Representation of the Autolock Switch"""

    def _update_from_coordinator(self) -> None:
        """Fetch state from the device."""
        self._attr_name = f"{self.coordinator.data.name} Autolock"
        self._attr_is_on = self.coordinator.data.auto_lock

    async def async_turn_on(self, **kwargs: Any) -> None:
        """Try to turn on Autolock."""
        await self.coordinator.autolock_on()

    async def async_turn_off(self, **kwargs: Any) -> None:
        """Try to unlock the lock."""
        await self.coordinator.autolock_off()  



