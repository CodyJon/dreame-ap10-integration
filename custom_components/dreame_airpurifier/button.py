"""Button platform for Dreame Air Purifier."""
from homeassistant.components.button import ButtonEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import CoordinatorEntity
from .api import DreameAirPurifier
from .const import DOMAIN

async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry, async_add_entities: AddEntitiesCallback) -> None:
    data = hass.data[DOMAIN][entry.entry_id]
    async_add_entities([DreameFilterResetButton(data["coordinator"], p) for p in data["purifiers"]])

class DreameFilterResetButton(CoordinatorEntity, ButtonEntity):
    _attr_has_entity_name = True
    _attr_icon = "mdi:filter-sync"
    _attr_name = "High Efficiency Composite Filter Reset"
    def __init__(self, coordinator, purifier: DreameAirPurifier):
        super().__init__(coordinator)
        self._purifier = purifier
        self._attr_unique_id = f"{purifier.unique_id}_filter_reset"
    @property
    def device_info(self):
        return {"identifiers": {(DOMAIN, self._purifier.unique_id)}, "name": self._purifier.name, "manufacturer": "Dreame", "model": self._purifier.model}
    @property
    def available(self): return self._purifier.available
    async def async_press(self) -> None:
        await self.hass.async_add_executor_job(self._purifier.reset_filter)
        await self.coordinator.async_request_refresh()
