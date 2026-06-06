"""Number platform for Dreame Air Purifier."""
from homeassistant.components.number import NumberEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import UnitOfTime
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import CoordinatorEntity
from .api import DreameAirPurifier, TIMER_MAX_HOURS, TIMER_MIN_HOURS
from .const import DOMAIN

async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry, async_add_entities: AddEntitiesCallback) -> None:
    data = hass.data[DOMAIN][entry.entry_id]
    async_add_entities([DreameTimerNumber(data["coordinator"], p) for p in data["purifiers"]])

class DreameTimerNumber(CoordinatorEntity, NumberEntity):
    _attr_has_entity_name = True
    _attr_icon = "mdi:timer-outline"
    _attr_name = "Timer"
    _attr_native_min_value = TIMER_MIN_HOURS
    _attr_native_max_value = TIMER_MAX_HOURS
    _attr_native_step = 1
    _attr_native_unit_of_measurement = UnitOfTime.HOURS
    def __init__(self, coordinator, purifier: DreameAirPurifier):
        super().__init__(coordinator)
        self._purifier = purifier
        self._attr_unique_id = f"{purifier.unique_id}_timer"
    @property
    def device_info(self):
        return {"identifiers": {(DOMAIN, self._purifier.unique_id)}, "name": self._purifier.name, "manufacturer": "Dreame", "model": self._purifier.model}
    @property
    def available(self): return self._purifier.available
    @property
    def native_value(self): return self._purifier.timer_hours
    async def async_set_native_value(self, value: float) -> None:
        await self.hass.async_add_executor_job(self._purifier.set_timer, round(value))
        await self.coordinator.async_request_refresh()
