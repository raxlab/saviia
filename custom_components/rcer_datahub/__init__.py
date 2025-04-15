"""RCER Data Hub Integration."""

import os
from datetime import timedelta

from dotenv import load_dotenv
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant

from custom_components.rcer_datahub.api import ConfigAPI, RCERDatahubAPI
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

    api = RCERDatahubAPI(
        ConfigAPI(
            ftp_host=os.getenv("FTP_HOST"),
            ftp_password=os.getenv("FTP_PASSWORD"),
            ftp_user=os.getenv("FTP_USER"),
            ftp_port=os.getenv("FTP_PORT"),
        )
    )
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
