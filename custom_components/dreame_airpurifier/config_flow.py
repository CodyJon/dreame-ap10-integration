"""Config flow for Dreame Air Purifier."""
import logging
import voluptuous as vol
from homeassistant import config_entries
from homeassistant.const import CONF_USERNAME, CONF_PASSWORD
from .api import DreameCloudAPI
from .const import DOMAIN, CONF_COUNTRY, COUNTRY_OPTIONS

_LOGGER = logging.getLogger(__name__)

class DreameAirPurifierConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    VERSION = 1

    async def async_step_user(self, user_input=None):
        errors = {}
        if user_input is not None:
            api = DreameCloudAPI(user_input[CONF_USERNAME], user_input[CONF_PASSWORD], user_input[CONF_COUNTRY])
            success = await self.hass.async_add_executor_job(api.login)
            if success:
                purifiers = await self.hass.async_add_executor_job(api.get_purifiers)
                if purifiers:
                    return self.async_create_entry(title=f"Dreame Air Purifier ({user_input[CONF_USERNAME]})", data=user_input)
                errors["base"] = "no_devices"
            else:
                errors["base"] = "invalid_auth"

        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema({
                vol.Required(CONF_USERNAME): str,
                vol.Required(CONF_PASSWORD): str,
                vol.Required(CONF_COUNTRY, default="us"): vol.In(COUNTRY_OPTIONS),
            }),
            errors=errors,
        )
