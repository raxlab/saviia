"""Provides services for SAVIIA integration."""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from homeassistant.core import HomeAssistant, ServiceCall


from http import HTTPStatus

from homeassistant.components import persistent_notification
from saviialib import SaviiaAPI

from . import const as c


def _ensure_domain_setup(hass) -> None:
    if c.DOMAIN not in hass.data:
        c.LOGGER.error(
            f"[service] No data found for {c.DOMAIN}. Please ensure the integration is set up first."
        )
        error_message = (
            f"[service] No data found for {c.DOMAIN}. "
            "Ensure the integration is properly set up before calling this service."
        )
        raise ValueError(error_message)


async def async_sync_thies_files(call: ServiceCall) -> None:
    """File synchronization."""
    c.LOGGER.info("[service] sync_thies_files_started")
    hass = call.hass
    _ensure_domain_setup(hass)

    for entry_id in hass.data[c.DOMAIN]:
        if entry_id == "services_registered":
            continue

        coordinator = hass.data[c.DOMAIN][entry_id]["thies_coordinator"]
        if not coordinator:
            continue
        try:
            success = await coordinator.async_request_refresh()
            c.LOGGER.info("[service] sync_thies_files_successful")
            if success:
                metadata = coordinator.data.get("metadata")
                c.LOGGER.debug("[service] sync_thies_files_response: %s", metadata)
        except Exception as e:
            c.LOGGER.error(f"[service] sync_thies_files_error: {e}")
            raise


async def async_local_backup(call: ServiceCall) -> None:
    c.LOGGER.info("[service] async_local_backup_started")
    hass = call.hass
    _ensure_domain_setup(hass)

    for entry_id in hass.data[c.DOMAIN]:
        coordinator = hass.data[c.DOMAIN][entry_id]["local_backup_coordinator"]
        try:
            success = await coordinator.async_request_refresh()
            c.LOGGER.info("[service] local_backup_successful")
            if success:
                metadata = coordinator.data.get("metadata")
                c.LOGGER.debug("[service] local_backup_response: %s", metadata)
        except Exception as e:
            c.LOGGER.error(f"[service] local_backup_error: {e}")
            raise


async def async_create_task(call: ServiceCall) -> None:
    hass = call.hass
    _ensure_domain_setup(hass)

    for entry_data in hass.data[c.DOMAIN].values():
        api: SaviiaAPI = entry_data["api"]
        tasks_service = api.get("tasks")  # type: ignore

        task = {
            "name": call.data["name"],
            "description": call.data["description"],
            "due_date": call.data["due_date"],
            "priority": call.data["priority"],
            "assignee": call.data["assignee"],
            "category": call.data["category"],
            "images": call.data["images"],
        }
        try:
            response = await tasks_service.create_task(
                channel_id=call.data["channel_id"],
                task=task,
            )
            tasks_coordinator = entry_data.get("tasks_coordinator")
            if tasks_coordinator:
                await tasks_coordinator.async_request_refresh()

            if response["status"] == HTTPStatus.OK.value:
                persistent_notification.async_create(
                    hass,
                    message="✅ La tarea fue creada correctamente.",
                    title="SAVIIA - Tarea creada",
                    notification_id="saviia_create_task_success",
                )
            else:
                error = response["metadata"]["error"]
                message = (
                    "❌ No se pudo crear la tarea.\n\n"
                    f"**Error:** {error}\n\n"
                    "Revisa los datos ingresados o la conexión con Discord."
                )
                persistent_notification.async_create(
                    hass,
                    message=message,
                    title="SAVIIA - Error al crear tarea",
                    notification_id="saviia_create_task_error",
                )
                hass.bus.async_fire(
                    "saviia_task_failed",
                    {"error": error},
                )

        except Exception as e:
            c.LOGGER.error(f"[service] local_backup_error: {e}")
            raise


async def async_setup_services(hass: HomeAssistant) -> None:
    """Set up services for the SAVIIA integration."""
    hass.services.async_register(
        c.DOMAIN,
        c.SERVICE_SYNC_FILES,
        async_sync_thies_files,
        schema=c.SERVICE_SYNC_FILES_SCHEMA,
    )
    hass.services.async_register(
        c.DOMAIN,
        c.SERVICE_LOCAL_BACKUP,
        async_local_backup,
        schema=c.SERVICE_LOCAL_BACKUP_SCHEMA,
    )
    hass.services.async_register(
        c.DOMAIN,
        c.SERVICE_CREATE_TASK,
        async_create_task,
        schema=c.SERVICE_CREATE_TASK_SCHEMA,
    )


async def async_unload_services(hass: HomeAssistant) -> None:
    """Unload services for the SAVIIA integration."""
    hass.services.async_remove(c.DOMAIN, c.SERVICE_SYNC_FILES)
    hass.services.async_remove(c.DOMAIN, c.SERVICE_LOCAL_BACKUP)
    hass.services.async_remove(c.DOMAIN, c.SERVICE_CREATE_TASK)
