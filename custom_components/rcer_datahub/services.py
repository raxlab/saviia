"""Provides services for RCER Data Hub integration."""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from homeassistant.core import HomeAssistant

from .const import DOMAIN, LOGGER, SERVICE_SYNC_FILES, SERVICE_SYNC_FILES_SCHEMA


async def async_sync_thies_files(hass: HomeAssistant) -> None:
    """File synchronization."""
    LOGGER.debug("Service sync_files called")
    for entry_id in hass.data[DOMAIN]:
        coordinator = hass.data[DOMAIN][entry_id]
        try:
            LOGGER.info("File synchronization initiated by service call")
            await coordinator.async_request_refresh()
        except Exception as e:
            LOGGER.error(f"Error during file synchronization: {e}")
            raise


async def async_setup_services(hass: HomeAssistant) -> None:
    """Set up services for the RCER Data Hub integration."""
    await async_sync_thies_files(hass)
    hass.services.async_register(
        DOMAIN,
        SERVICE_SYNC_FILES,
        async_sync_thies_files,
        schema=SERVICE_SYNC_FILES_SCHEMA,
        description="Initiates file synchronization with the FTP server and cloud storage.",
    )


async def async_unload_services(hass: HomeAssistant) -> None:
    """Unload services for the RCER Data Hub integration."""
    hass.services.async_remove(DOMAIN, SERVICE_SYNC_FILES)
