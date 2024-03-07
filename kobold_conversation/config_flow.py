 
from homeassistant import config_entries
from .const import DOMAIN
import voluptuous as vol
from homeassistant.core import HomeAssistant
from typing import Any

from .const import (
    CONF_ATTACH_USERNAME,
    CONF_MAX_TOKENS,
    CONF_PROMPT,
    CONF_TEMPERATURE,
    CONF_TOP_P,
    CONF_MAX_FUNCTION_CALLS_PER_CONVERSATION,
    CONF_FUNCTIONS,
    CONF_BASE_URL,
    DEFAULT_ATTACH_USERNAME,
    DEFAULT_MAX_TOKENS,
    DEFAULT_PROMPT,
    DEFAULT_TEMPERATURE,
    DEFAULT_TOP_P,
    DEFAULT_MAX_FUNCTION_CALLS_PER_CONVERSATION,
    DEFAULT_CONF_FUNCTIONS,
    DEFAULT_CONF_BASE_URL,
    DOMAIN,
    DEFAULT_NAME,
    CONF_NAME,
    CONF_API_KEY
)

async def validate_input(hass: HomeAssistant, data: dict[str, Any]) -> None:

    api_key = data[CONF_API_KEY]
    base_url = data.get(CONF_BASE_URL)

    if base_url == DEFAULT_CONF_BASE_URL:
        base_url = None
        data.pop(CONF_BASE_URL)


    
STEP_USER_DATA_SCHEMA = vol.Schema(
    {
        vol.Optional(CONF_NAME, default="User friendly name for assistant selection."): str,
        vol.Required(CONF_API_KEY, default="0000000000"): str,
        vol.Optional(CONF_BASE_URL, default=DEFAULT_CONF_BASE_URL): str
    }
)
        
        
class config_flow(config_entries.ConfigFlow, domain=DOMAIN):
    async def async_step_user(self, info):
        if info is not None:
            #if user_input is None:
            return self.async_create_entry(
                title=info.get(CONF_NAME, DEFAULT_NAME), data=info
            )

        return self.async_show_form(
            step_id="user", data_schema=STEP_USER_DATA_SCHEMA
        )




