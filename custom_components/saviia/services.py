"""Provides services for SAVIIA integration."""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from homeassistant.core import (
        HomeAssistant,
        ServiceCall,
        ServiceResponse,
    )


from http import HTTPStatus

from homeassistant.core import (
    SupportsResponse,
)
from saviialib import SaviiaAPI

from custom_components.saviia.const import (
    GeneralParams,
    ServicesParams,
)
from custom_components.saviia.libs.log_client import (
    DebugArgs,
    ErrorArgs,
    InfoArgs,
    LogClient,
    LogClientArgs,
    LogStatus,
)

HTTP_OK = 200

logclient = LogClient(
    LogClientArgs(client_name="logging", service_name="services", class_name="services")
)


def _ensure_domain_setup(hass) -> None:
    logclient.method_name = "_ensure_domain_setup"
    if GeneralParams.DOMAIN not in hass.data:
        error_message = (
            f"[service] No data found for {GeneralParams.DOMAIN}. "
            "Ensure the integration is properly set up before calling this service."
        )
        logclient.error(
            ErrorArgs(
                status=LogStatus.ERROR,
                metadata={"msg": error_message},
            )
        )
        raise ValueError(error_message)


def _check_api_in_entry(hass) -> SaviiaAPI:
    api_exists = False
    api: SaviiaAPI
    for entry_data in hass.data[GeneralParams.DOMAIN].values():
        if entry_data.get("api"):
            api_exists = True
            api = entry_data["api"]
            break
    if not api_exists:
        error_message = "No API instance found in any config entry"
        logclient.error(
            ErrorArgs(
                status=LogStatus.ERROR,
                metadata={"msg": error_message},
            )
        )
        raise ValueError(error_message)
    return api


async def async_sync_thies_files(call: ServiceCall) -> None:
    """File synchronization."""
    logclient.method_name = "async_sync_thies_files"
    logclient.debug(DebugArgs(status=LogStatus.STARTED))
    hass = call.hass
    _ensure_domain_setup(hass)

    for entry_id in hass.data[GeneralParams.DOMAIN]:
        if entry_id == "services_registered":
            continue

        coordinator = hass.data[GeneralParams.DOMAIN][entry_id]["thies_coordinator"]
        if not coordinator:
            continue
        try:
            success = await coordinator.async_request_refresh()
            logclient.info(
                InfoArgs(
                    status=LogStatus.SUCCESSFUL,
                    metadata={"msg": "File sync successful"},
                )
            )
            if success:
                metadata = coordinator.data.get("metadata")
                logclient.debug(
                    DebugArgs(
                        status=LogStatus.SUCCESSFUL,
                        metadata={"msg": f"Metadata: {metadata}"},
                    )
                )

        except Exception as e:
            logclient.error(
                ErrorArgs(
                    status=LogStatus.ERROR,
                    metadata={"msg": e.__str__()},
                )
            )
            raise


async def async_local_backup(call: ServiceCall) -> None:
    logclient.method_name = "async_local_backup"
    logclient.debug(DebugArgs(status=LogStatus.STARTED))
    hass = call.hass
    _ensure_domain_setup(hass)

    for entry_id in hass.data[GeneralParams.DOMAIN]:
        if entry_id == "services_registered":
            continue
        coordinator = hass.data[GeneralParams.DOMAIN][entry_id][
            "local_backup_coordinator"
        ]
        try:
            success = await coordinator.async_request_refresh()
            logclient.info(
                InfoArgs(
                    status=LogStatus.SUCCESSFUL,
                    metadata={"msg": "Local backup successful"},
                )
            )
            if success:
                metadata = coordinator.data.get("metadata")
                logclient.debug(
                    DebugArgs(
                        status=LogStatus.SUCCESSFUL,
                        metadata={"msg": f"Metadata: {metadata}"},
                    )
                )
        except Exception as e:
            logclient.error(
                ErrorArgs(
                    status=LogStatus.ERROR,
                    metadata={"msg": e.__str__()},
                )
            )
            raise


async def async_get_netcamera_rates(call: ServiceCall) -> ServiceResponse:
    """Get camera rates service."""
    logclient.method_name = "async_get_camera_rates"
    logclient.debug(DebugArgs(status=LogStatus.STARTED))
    _ensure_domain_setup(call.hass)
    api = _check_api_in_entry(call.hass)
    camera_services = api.get("netcamera")
    try:
        result = await camera_services.get_camera_rates()
        logclient.info(
            InfoArgs(
                status=LogStatus.SUCCESSFUL,
                metadata={"msg": f"Camera rates retrieved: {result.get('metadata')}"},
            )
        )
        if result.get("status") == HTTPStatus.OK.value:
            rate_status, photo_rate, video_rate = result.get("metadata").values()
            return {
                "status": rate_status,
                "photo_rate": photo_rate,
                "video_rate": video_rate,
            }
        logclient.error(
            ErrorArgs(
                status=LogStatus.ERROR,
                metadata={"msg": result["message"]},
            )
        )
        return result

    except Exception as e:
        logclient.error(
            ErrorArgs(
                status=LogStatus.ERROR,
                metadata={"msg": f"Error retrieving camera rates: {e}"},
            )
        )
        raise


async def async_update_task(call: ServiceCall) -> ServiceResponse:
    """Update a Task in a Discord channel."""
    logclient.method_name = "async_update_task"
    logclient.debug(DebugArgs(status=LogStatus.STARTED))
    _ensure_domain_setup(call.hass)
    api = _check_api_in_entry(call.hass)
    task_service = api.get("tasks")
    try:
        webhook_url, task, completed, channel_id = (
            call.data.get("webhook_url"),
            call.data.get("task"),
            call.data.get("completed"),
            call.data.get("channel_id", ""),
        )
        result = await task_service.update_task(
            webhook_url, task, completed, channel_id
        )
        if result.get("status") != HTTPStatus.OK.value:
            logclient.error(
                ErrorArgs(
                    status=LogStatus.ERROR,
                    metadata={"msg": result["message"]},
                )
            )
        else:
            logclient.info(
                InfoArgs(
                    status=LogStatus.SUCCESSFUL,
                    metadata={
                        "msg": f"Task updated successfully: {result.get('metadata')}"
                    },
                )
            )
        return {
            "api_status": result.get("status"),
            "api_message": result.get("message"),
            "api_metadata": result.get("metadata"),
        }
    except Exception as e:
        logclient.error(
            ErrorArgs(
                status=LogStatus.ERROR,
                metadata={"msg": f"Error updating task: {e}"},
            )
        )
        raise


async def async_delete_task(call: ServiceCall) -> ServiceResponse:
    """Delete a Task in a Discord channel."""
    logclient.method_name = "async_delete_task"
    logclient.debug(DebugArgs(status=LogStatus.STARTED))
    _ensure_domain_setup(call.hass)
    api = _check_api_in_entry(call.hass)
    task_service = api.get("tasks")
    try:
        webhook_url, task_id, channel_id = (
            call.data.get("webhook_url"),
            call.data.get("task_id"),
            call.data.get("channel_id", ""),
        )
        result = await task_service.delete_task(webhook_url, task_id, channel_id)
        if result.get("status") != HTTPStatus.OK.value:
            logclient.error(
                ErrorArgs(
                    status=LogStatus.ERROR,
                    metadata={"msg": result["message"]},
                )
            )
        else:
            logclient.info(
                InfoArgs(
                    status=LogStatus.SUCCESSFUL,
                    metadata={
                        "msg": f"Task deleted successfully: {result.get('metadata')}"
                    },
                )
            )
        return {
            "api_status": result.get("status"),
            "api_message": result.get("message"),
            "api_metadata": result.get("metadata"),
        }
    except Exception as e:
        logclient.error(
            ErrorArgs(
                status=LogStatus.ERROR,
                metadata={"msg": f"Error deleting task: {e}"},
            )
        )
        raise


async def async_setup_services(hass: HomeAssistant) -> None:
    """Set up services for the SAVIIA integration."""
    hass.services.async_register(
        GeneralParams.DOMAIN,
        ServicesParams.SERVICE_SYNC_FILES,
        async_sync_thies_files,
        schema=ServicesParams.SERVICE_SYNC_FILES_SCHEMA,
    )
    hass.services.async_register(
        GeneralParams.DOMAIN,
        ServicesParams.SERVICE_LOCAL_BACKUP,
        async_local_backup,
        schema=ServicesParams.SERVICE_LOCAL_BACKUP_SCHEMA,
    )
    hass.services.async_register(
        GeneralParams.DOMAIN,
        ServicesParams.SERVICE_GET_NETCAMERA_RATES,
        async_get_netcamera_rates,
        schema=ServicesParams.SERVICE_GET_NETCAMERA_RATES_SCHEMA,
        supports_response=SupportsResponse.ONLY,
    )
    hass.services.async_register(
        GeneralParams.DOMAIN,
        ServicesParams.SERVICE_UPDATE_TASK,
        async_update_task,
        schema=ServicesParams.SERVICE_UPDATE_TASK_SCHEMA,
        supports_response=SupportsResponse.ONLY,
    )
    hass.services.async_register(
        GeneralParams.DOMAIN,
        ServicesParams.SERVICE_DELETE_TASK,
        async_delete_task,
        schema=ServicesParams.SERVICE_DELETE_TASK_SCHEMA,
        supports_response=SupportsResponse.ONLY,
    )


async def async_unload_services(hass: HomeAssistant) -> None:
    """Unload services for the SAVIIA integration."""
    hass.services.async_remove(GeneralParams.DOMAIN, ServicesParams.SERVICE_SYNC_FILES)
    hass.services.async_remove(
        GeneralParams.DOMAIN, ServicesParams.SERVICE_LOCAL_BACKUP
    )
    hass.services.async_remove(
        GeneralParams.DOMAIN, ServicesParams.SERVICE_GET_NETCAMERA_RATES
    )
    hass.services.async_remove(GeneralParams.DOMAIN, ServicesParams.SERVICE_UPDATE_TASK)
    hass.services.async_remove(GeneralParams.DOMAIN, ServicesParams.SERVICE_DELETE_TASK)
