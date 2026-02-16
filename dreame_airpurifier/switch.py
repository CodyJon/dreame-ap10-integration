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
        entities.extend([DreameIonizerSwitch(data["coordinator"], p), DreameLEDSwitch(data["coordinator"], p),
                         DreameBuzzerSwitch(data["coordinator"], p), DreameChildLockSwitch(data["coordinator"], p)])
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

class DreameIonizerSwitch(DreameBaseSwitch):
    _attr_icon = "mdi:creation"
    def __init__(self, c, p): super().__init__(c, p, "ionizer", "Ionizer")
    @property
    def is_on(self): return self._purifier.ionizer
    async def async_turn_on(self, **kwargs): await self.hass.async_add_executor_job(self._purifier.set_ionizer, True); await self.coordinator.async_request_refresh()
    async def async_turn_off(self, **kwargs): await self.hass.async_add_executor_job(self._purifier.set_ionizer, False); await self.coordinator.async_request_refresh()

class DreameLEDSwitch(DreameBaseSwitch):
    _attr_icon = "mdi:led-on"
    def __init__(self, c, p): super().__init__(c, p, "led", "LED Indicator")
    @property
    def is_on(self): return self._purifier.led
    async def async_turn_on(self, **kwargs): await self.hass.async_add_executor_job(self._purifier.set_led, True); await self.coordinator.async_request_refresh()
    async def async_turn_off(self, **kwargs): await self.hass.async_add_executor_job(self._purifier.set_led, False); await self.coordinator.async_request_refresh()

class DreameBuzzerSwitch(DreameBaseSwitch):
    _attr_icon = "mdi:volume-high"
    def __init__(self, c, p): super().__init__(c, p, "buzzer", "Buzzer")
    @property
    def is_on(self): return self._purifier.buzzer
    async def async_turn_on(self, **kwargs): await self.hass.async_add_executor_job(self._purifier.set_buzzer, True); await self.coordinator.async_request_refresh()
    async def async_turn_off(self, **kwargs): await self.hass.async_add_executor_job(self._purifier.set_buzzer, False); await self.coordinator.async_request_refresh()

class DreameChildLockSwitch(DreameBaseSwitch):
    _attr_icon = "mdi:lock"
    def __init__(self, c, p): super().__init__(c, p, "child_lock", "Child Lock")
    @property
    def is_on(self): return self._purifier.child_lock
    async def async_turn_on(self, **kwargs): await self.hass.async_add_executor_job(self._purifier.set_child_lock, True); await self.coordinator.async_request_refresh()
    async def async_turn_off(self, **kwargs): await self.hass.async_add_executor_job(self._purifier.set_child_lock, False); await self.coordinator.async_request_refresh()
