"""Switch platform for Dreame Air Purifier."""
import logging
from typing import Any
from homeassistant.components.switch import SwitchEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import CoordinatorEntity
from .api import DreameAirPurifier
from .const import DOMAIN

_LOGGER = logging.getLogger(__name__)

async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry, async_add_entities: AddEntitiesCallback) -> None:
    data = hass.data[DOMAIN][entry.entry_id]
    entities = []
    for p in data["purifiers"]:
        entities.extend([DreameChildLockSwitch(data["coordinator"], p), DreamePlayModeSwitch(data["coordinator"], p),
                         DreameVoiceInteractionSwitch(data["coordinator"], p), DreameKeypressToneSwitch(data["coordinator"], p)])
    async_add_entities(entities)

class DreameBaseSwitch(CoordinatorEntity, SwitchEntity):
    _attr_has_entity_name = True
    def __init__(self, coordinator, purifier: DreameAirPurifier, key: str, name: str):
        super().__init__(coordinator)
        self._purifier = purifier
        self._attr_unique_id = f"{purifier.unique_id}_{key}"
        self._attr_name = name
    @property
    def device_info(self):
        return {"identifiers": {(DOMAIN, self._purifier.unique_id)}, "name": self._purifier.name, "manufacturer": "Dreame", "model": self._purifier.model}
    @property
    def available(self): return self._purifier.available

class DreameChildLockSwitch(DreameBaseSwitch):
    _attr_icon = "mdi:lock"
    def __init__(self, c, p): super().__init__(c, p, "child_lock", "Child Lock")
    @property
    def is_on(self): return self._purifier.child_lock
    async def async_turn_on(self, **kwargs): await self.hass.async_add_executor_job(self._purifier.set_child_lock, True); await self.coordinator.async_request_refresh()
    async def async_turn_off(self, **kwargs): await self.hass.async_add_executor_job(self._purifier.set_child_lock, False); await self.coordinator.async_request_refresh()

class DreamePlayModeSwitch(DreameBaseSwitch):
    _attr_icon = "mdi:play-circle"
    def __init__(self, c, p): super().__init__(c, p, "play_mode", "Play Mode")
    @property
    def is_on(self): return self._purifier.play_mode
    async def async_turn_on(self, **kwargs): await self.hass.async_add_executor_job(self._purifier.set_play_mode, True); await self.coordinator.async_request_refresh()
    async def async_turn_off(self, **kwargs): await self.hass.async_add_executor_job(self._purifier.set_play_mode, False); await self.coordinator.async_request_refresh()

class DreameVoiceInteractionSwitch(DreameBaseSwitch):
    _attr_icon = "mdi:microphone"
    def __init__(self, c, p): super().__init__(c, p, "voice_interaction", "Voice Interaction")
    @property
    def is_on(self): return self._purifier.voice_interaction
    async def async_turn_on(self, **kwargs): await self.hass.async_add_executor_job(self._purifier.set_voice_interaction, True); await self.coordinator.async_request_refresh()
    async def async_turn_off(self, **kwargs): await self.hass.async_add_executor_job(self._purifier.set_voice_interaction, False); await self.coordinator.async_request_refresh()

class DreameKeypressToneSwitch(DreameBaseSwitch):
    _attr_icon = "mdi:volume-high"
    def __init__(self, c, p): super().__init__(c, p, "keypress_tone", "Keypress Tone")
    @property
    def is_on(self): return self._purifier.keypress_tone
    async def async_turn_on(self, **kwargs): await self.hass.async_add_executor_job(self._purifier.set_keypress_tone, True); await self.coordinator.async_request_refresh()
    async def async_turn_off(self, **kwargs): await self.hass.async_add_executor_job(self._purifier.set_keypress_tone, False); await self.coordinator.async_request_refresh()
