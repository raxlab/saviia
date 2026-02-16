"""Provides services for SAVIIA integration."""

from __future__ import annotations

import base64
import json
from io import BytesIO
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from homeassistant.core import (
        HomeAssistant,
        ServiceCall,
        ServiceResponse,
    )


from http import HTTPStatus

import aiohttp
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

    for entry_id, entry_data in call.hass.data[GeneralParams.DOMAIN].items():
        if entry_id == "services_registered":
            continue
        api: SaviiaAPI = entry_data["api"]
        camera_services = api.get("netcamera")
        try:
            result = await camera_services.get_camera_rates()
            logclient.info(
                InfoArgs(
                    status=LogStatus.SUCCESSFUL,
                    metadata={
                        "msg": f"Camera rates retrieved: {result.get('metadata')}"
                    },
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
    return None


async def async_update_task(call: ServiceCall) -> ServiceResponse:
    """Update a Task in a Discord channel."""
    logclient.method_name = "async_update_task"
    logclient.debug(DebugArgs(status=LogStatus.STARTED))
    _ensure_domain_setup(call.hass)

    for entry_id, entry_data in call.hass.data[GeneralParams.DOMAIN].items():
        if entry_id == "services_registered":
            continue
        api: SaviiaAPI = entry_data["api"]
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
                    metadata={"msg": f"Error retrieving camera rates: {e}"},
                )
            )
            raise
    return None


async def async_delete_task(call: ServiceCall) -> ServiceResponse:
    """Delete a Task in a Discord channel."""
    logclient.method_name = "async_delete_task"
    logclient.debug(DebugArgs(status=LogStatus.STARTED))
    _ensure_domain_setup(call.hass)

    for entry_id, entry_data in call.hass.data[GeneralParams.DOMAIN].items():
        if entry_id == "services_registered":
            continue
        api: SaviiaAPI = entry_data["api"]
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
                    metadata={"msg": f"Error retrieving camera rates: {e}"},
                )
            )
            raise
    return None


async def async_create_task(call: ServiceCall) -> ServiceResponse:  # noqa: PLR0915
    """Create a new task and send to Discord webhook."""
    logclient.method_name = "async_create_task"
    logclient.debug(DebugArgs(status=LogStatus.STARTED))

    hass = call.hass
    _ensure_domain_setup(hass)

    # Get the Discord webhook URL from configuration
    discord_webhook_url = None
    for entry_id, entry_data in hass.data[GeneralParams.DOMAIN].items():
        if entry_id != "services_registered":
            continue
        config = entry_data.get("config")
        if not config:
            continue
        discord_webhook_url = config.get("discord_webhook_url")
        if discord_webhook_url:
            break
    if discord_webhook_url is None:
        logclient.error(
            ErrorArgs(
                status=LogStatus.ERROR,
                metadata={"msg": "Discord webhook URL not configured"},
            )
        )
        return {
            "success": False,
            "error": "Discord webhook URL not configured",
            "hass": hass.data[GeneralParams.DOMAIN].items(),
        }

    try:
        title = call.data.get("title", "")
        details = call.data.get("details", "Sin descripción")
        assignee = call.data.get("assignee", "No asignada")
        category = call.data.get("category", "Sin categoría")
        deadline = call.data.get("deadline", "")
        periodicity = call.data.get("periodicity", "Sin periodicidad")
        periodicity_num = call.data.get("periodicity_num", "?")
        priority = call.data.get("priority", "Baja")
        images = call.data.get("images", [])

        if periodicity != "Sin periodicidad" and periodicity_num == "?":
            logclient.error(
                ErrorArgs(
                    status=LogStatus.ERROR,
                    metadata={
                        "msg": "Invalid periodicity number for non-zero periodicity"
                    },
                )
            )
            return {
                "success": False,
                "error": "No definiste un número válido para la periodicidad.",
            }

        def _format_periodicity(periodicity: str, periodicity_num) -> str:
            """Format periodicity string."""
            if periodicity in {"", "Sin periodicidad"}:
                return "Sin periodicidad"
            if periodicity == "daily":
                return f"Cada {periodicity_num} día(s)"
            if periodicity == "weekly":
                return f"Cada {periodicity_num} semana(s)"
            if periodicity == "monthly":
                return f"Cada {periodicity_num} mes(es)"
            if periodicity == "yearly":
                return f"Cada {periodicity_num} año(s)"
            return "Sin periodicidad"

        periodicity_str = _format_periodicity(periodicity, periodicity_num)

        # Build task content
        content = f"## {title}\n"
        content += "* __Estado__: Pendiente\n"
        content += f"* __Fecha de realización__: {deadline}\n"
        content += f"* __Descripcion__: {details}\n"
        content += f"* __Periodicidad__: {periodicity_str}\n"
        content += f"* __Prioridad__: {priority}\n"
        content += f"* __Categoría__: {category}\n"
        content += f"* __Persona asignada__: {assignee}\n"
        form_data = aiohttp.FormData()
        embeds = []

        for index, img in enumerate(images):
            try:
                # Decode base64 image data
                img_data = img.get("data", "")
                img_name = img.get("name", f"image_{index}")
                img_type = img.get("type", "image/jpeg")
                image_bytes = base64.b64decode(img_data)
                form_data.add_field(
                    f"files[{index}]",
                    BytesIO(image_bytes),
                    filename=img_name,
                    content_type=img_type,
                )
                embeds.append(
                    {
                        "title": f"Imagen {index + 1}: {img_name}",
                        "image": {"url": f"attachment://{img_name}"},
                    }
                )
            except Exception as e:  # noqa: BLE001
                logclient.error(
                    ErrorArgs(
                        status=LogStatus.ERROR,
                        metadata={"msg": f"Error processing image {index}: {e!s}"},
                    )
                )
        payload_json = {"content": content, "embeds": embeds}
        form_data.add_field("payload_json", json.dumps(payload_json))
        async with aiohttp.ClientSession() as session:  # noqa: SIM117
            async with session.post(discord_webhook_url, data=form_data) as response:
                if response.status not in {204, 200}:
                    error_text = await response.text()
                    logclient.error(
                        ErrorArgs(
                            status=LogStatus.ERROR,
                            metadata={"msg": f"Discord webhook error: {error_text}"},
                        )
                    )
                    return {"success": False, "error": f"Discord error: {error_text}"}

                logclient.info(
                    InfoArgs(
                        status=LogStatus.SUCCESSFUL,
                        metadata={"msg": "Task created successfully on Discord"},
                    )
                )
                return {"success": True, "message": "Tarea creada con éxito ✅"}

    except Exception as e:  # noqa: BLE001
        logclient.error(
            ErrorArgs(
                status=LogStatus.ERROR,
                metadata={"msg": f"Error creating task: {e!s}"},
            )
        )
        return {"success": False, "error": str(e)}


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
    hass.services.async_register(
        GeneralParams.DOMAIN,
        ServicesParams.SERVICE_CREATE_TASK,
        async_create_task,
        schema=ServicesParams.SERVICE_CREATE_TASK_SCHEMA,
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
    hass.services.async_remove(GeneralParams.DOMAIN, ServicesParams.SERVICE_CREATE_TASK)
