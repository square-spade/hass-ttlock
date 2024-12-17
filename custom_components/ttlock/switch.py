"""Switch setup for our Integration."""

from __future__ import annotations

from typing import Any

from homeassistant.components.switch import SwitchDeviceClass, SwitchEntity
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
                AutoLock(coordinator),
                LockSound(coordinator),
            )
        ]
    )


class AutoLock(BaseLockEntity, SwitchEntity):
    """The entity object for a switch."""

    _attr_device_class = SwitchDeviceClass.SWITCH

    def _update_from_coordinator(self) -> None:
        """Fetch state from the device."""
        self._attr_name = f"{self.coordinator.data.name} Auto Lock"
        self._attr_is_on = self.coordinator.data.auto_lock

    async def async_turn_on(self, **kwargs: Any) -> None:
        """Turn the entity on."""
        await self.coordinator.auto_lock_on()

    async def async_turn_off(self, **kwargs: Any) -> None:
        """Turn the entity off."""
        await self.coordinator.auto_lock_off()


class LockSound(BaseLockEntity, SwitchEntity):
    """The entity object for a switch."""

    _attr_device_class = SwitchDeviceClass.SWITCH

    def _update_from_coordinator(self) -> None:
        """Fetch state from the device."""
        self._attr_name = f"{self.coordinator.data.name} Lock Sound"
        self._attr_is_on = self.coordinator.data.lock_sound

    async def async_turn_on(self, **kwargs: Any) -> None:
        """Turn the entity on."""
        await self.coordinator.lock_sound_on()

    async def async_turn_off(self, **kwargs: Any) -> None:
        """Turn the entity off."""
        await self.coordinator.lock_sound_off()
