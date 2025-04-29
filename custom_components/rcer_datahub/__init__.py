"""RCER Data Hub Integration."""

from datetime import timedelta

from dotenv import load_dotenv
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from rcer_iot_client_pkg import EpiiAPI
from custom_components.rcer_datahub.const import (
    DOMAIN,
    LOGGER,
    UPDATE_INTERVAL_HOURS,
    UPDATE_INTERVAL_MINUTES,
)

from .coordinator import RCERDatahubUpdateCoordinator

load_dotenv()


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up RCER Datahub API from a config entry."""
    hass.data.setdefault(DOMAIN, {})
    LOGGER.debug("[init] async_setup_entry_started")
    api = EpiiAPI()
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

    LOGGER.debug("[init] async_setup_entry_successful")
    return True
