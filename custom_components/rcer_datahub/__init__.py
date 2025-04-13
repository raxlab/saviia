"""RCER Data Hub Integration"""

import logging

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant, ServiceCall
from homeassistant.helpers.typing import ConfigType

from .const import DOMAIN

_LOGGER = logging.getLogger(__name__)

async def async_setup(hass: HomeAssistant, config: ConfigType) -> bool: 
    return True

async def async_setup_entry(hass: HomeAssistant, config: ConfigType) -> bool:
    pass