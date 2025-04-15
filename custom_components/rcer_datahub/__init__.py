"""RCER Data Hub Integration"""

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant, ServiceCall
from homeassistant.helpers.typing import ConfigType

from .api.rcer_datahub_api import RCERDatahubAPI
from .coordinator import RCERDatahubUpdateCoordinator

from .const import DOMAIN, LOGGER, UPDATE_INTERVAL_HOURS, UPDATE_INTERVAL_MINUTES
from datetime import timedelta


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up RCER Datahub API from a config entry."""
    hass.data.setdefault(DOMAIN, {})

    api = RCERDatahubAPI()
    coordinator = RCERDatahubUpdateCoordinator(
        hass=hass,
        api=api,
        logger=LOGGER,
        name=DOMAIN,
        update_interval=timedelta(
            hours=UPDATE_INTERVAL_HOURS, minutes=UPDATE_INTERVAL_MINUTES
        ),
    )
    # Fetch data
    await coordinator.async_config_entry_first_refresh()
    # Save data in Hassio
    hass.data[DOMAIN][entry.entry_id] = coordinator
    # TODO: Load sensors: Starlink and VRM

    return True
