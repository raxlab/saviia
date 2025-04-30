"""RCER Data Hub Integration."""

from datetime import timedelta

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from rcer_iot_client_pkg import EpiiAPI

from custom_components.rcer_datahub.const import (
    DOMAIN,
    LOGGER,
    PLATFORMS,
    UPDATE_INTERVAL_HOURS,
    UPDATE_INTERVAL_MINUTES,
)

from .coordinator import RCERDatahubUpdateCoordinator


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
    hass.data[DOMAIN][entry.entry_id]["coordinator"] = coordinator
    # Load sensors: Starlink and VRM [TODO]

    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)

    LOGGER.debug("[init] async_setup_entry_successful")
    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload a config entry."""
    unload_ok = await hass.config_entries.async_unload_platforms(entry, PLATFORMS)
    if unload_ok:
        hass.data[DOMAIN].pop(entry.entry_id)

    return unload_ok
