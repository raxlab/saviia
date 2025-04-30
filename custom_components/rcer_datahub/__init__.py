"""RCER Data Hub Integration."""

from datetime import timedelta

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from rcer_iot_client_pkg import EpiiAPI

from custom_components.rcer_datahub.const import (
    CONFIG_SCHEMA,
    DOMAIN,
    LOGGER,
    PLATFORMS,
    UPDATE_INTERVAL_HOURS,
    UPDATE_INTERVAL_MINUTES,
)

from .coordinator import RCERDatahubUpdateCoordinator
from .services import async_setup_services, async_unload_services


async def async_setup(hass: HomeAssistant, config: dict) -> bool:
    """Set up the RCER Hub component."""
    config = CONFIG_SCHEMA(config)
    if not hass.config_entries.async_entries(DOMAIN):
        hass.async_create_task(
            hass.config_entries.flow.async_init(DOMAIN, context={"source": "user"})
        )
    return True


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

    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)
    await async_setup_services(hass)

    LOGGER.debug("[init] async_setup_entry_successful")
    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload a config entry."""
    unload_ok = await hass.config_entries.async_unload_platforms(entry, PLATFORMS)
    if unload_ok:
        hass.data[DOMAIN].pop(entry.entry_id)

    await async_unload_services(hass)
    return unload_ok
