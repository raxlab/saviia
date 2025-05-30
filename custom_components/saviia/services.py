"""Provides services for SAVIIA integration."""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from homeassistant.core import HomeAssistant, ServiceCall

from .const import (
    DOMAIN,
    LOGGER,
    SERVICE_LOCAL_BACKUP,
    SERVICE_LOCAL_BACKUP_SCHEMA,
    SERVICE_SYNC_FILES,
    SERVICE_SYNC_FILES_SCHEMA,
)


def _is_coordinator_in_hass_data(hass) -> None:
    if DOMAIN not in hass.data:
        LOGGER.error(
            f"[service] No data found for {DOMAIN}. Please ensure the integration is set up first."
        )
        error_message = (
            f"[service] No data found for {DOMAIN}. "
            "Ensure the integration is properly set up before calling this service."
        )
        raise ValueError(error_message)


async def async_sync_thies_files(call: ServiceCall) -> None:
    """File synchronization."""
    LOGGER.info("[service] sync_thies_files_started")
    hass = call.hass
    _is_coordinator_in_hass_data(hass)

    for entry_id in hass.data[DOMAIN]:
        coordinator = hass.data[DOMAIN][entry_id]["thies_coordinator"]
        try:
            success = await coordinator.async_request_refresh()
            LOGGER.info("[service] sync_thies_files_successful")
            if success:
                metadata = coordinator.data.get("metadata")
                LOGGER.debug("[service] sync_thies_files_response: %s", metadata)
        except Exception as e:
            LOGGER.error(f"[service] sync_thies_files_error: {e}")
            raise


async def async_local_backup(call: ServiceCall) -> None:
    LOGGER.info("[service] async_local_backup_started")
    hass = call.hass
    _is_coordinator_in_hass_data(hass)

    for entry_id in hass.data[DOMAIN]:
        coordinator = hass.data[DOMAIN][entry_id]["local_backup_coordinator"]
        try:
            success = await coordinator.async_request_refresh()
            LOGGER.info("[service] local_backup_successful")
            if success:
                metadata = coordinator.data.get("metadata")
                LOGGER.debug("[service] local_backup_response: %s", metadata)
        except Exception as e:
            LOGGER.error(f"[service] local_backup_error: {e}")
            raise


async def async_setup_services(hass: HomeAssistant) -> None:
    """Set up services for the SAVIIA integration."""
    hass.services.async_register(
        DOMAIN,
        SERVICE_SYNC_FILES,
        async_sync_thies_files,
        schema=SERVICE_SYNC_FILES_SCHEMA,
    )
    hass.services.async_register(
        DOMAIN,
        SERVICE_LOCAL_BACKUP,
        async_local_backup,
        schema=SERVICE_LOCAL_BACKUP_SCHEMA,
    )


async def async_unload_services(hass: HomeAssistant) -> None:
    """Unload services for the SAVIIA integration."""
    hass.services.async_remove(DOMAIN, SERVICE_SYNC_FILES)
    hass.services.async_remove(DOMAIN, SERVICE_LOCAL_BACKUP)
