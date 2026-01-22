"""SAVIIA Integration."""

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from saviialib import SaviiaAPI, SaviiaAPIConfig

from custom_components.saviia.const import GeneralParams

from .coordinator import (
    LocalBackupCoordinator,
    SyncThiesDataCoordinator,
)
from .libs.log_client import (
    DebugArgs,
    ErrorArgs,
    LogClient,
    LogClientArgs,
    LogStatus,
)
from .services import async_setup_services, async_unload_services

logclient = LogClient(
    LogClientArgs(client_name="logging", service_name="init", class_name="init")
)


async def async_setup(hass: HomeAssistant, config: dict) -> bool:
    """Set up the SAVIIA component."""
    logclient.method_name = "async_setup"
    logclient.debug(DebugArgs(status=LogStatus.STARTED))
    if not hass.config_entries.async_entries(GeneralParams.DOMAIN):
        hass.async_create_task(
            hass.config_entries.flow.async_init(
                GeneralParams.DOMAIN, context={"source": "user"}
            )
        )
    logclient.debug(
        DebugArgs(
            status=LogStatus.SUCCESSFUL,
            metadata={"msg": "SAVIIA component setup successful"},
        )
    )
    return True


async def async_setup_entry(hass: HomeAssistant, config_entry: ConfigEntry) -> bool:
    """Set up coordinator from a config entry."""
    logclient.method_name = "async_setup_entry"
    logclient.debug(DebugArgs(status=LogStatus.STARTED))
    api = SaviiaAPI(
        SaviiaAPIConfig(
            ftp_port=config_entry.data["ftp_port"],
            ftp_host=config_entry.data["ftp_host"],
            ftp_user=config_entry.data["ftp_user"],
            ftp_password=config_entry.data["ftp_password"],
            sharepoint_client_id=config_entry.data["sharepoint_client_id"],
            sharepoint_client_secret=config_entry.data["sharepoint_client_secret"],
            sharepoint_tenant_id=config_entry.data["sharepoint_tenant_id"],
            sharepoint_tenant_name=config_entry.data["sharepoint_tenant_name"],
            sharepoint_site_name=config_entry.data["sharepoint_site_name"],
            logger=GeneralParams.LOGGER,
            notification_client_api_key=config_entry.data.get(
                "notification_client_api_key", ""
            ),
        )
    )
    hass.data.setdefault(GeneralParams.DOMAIN, {})
    hass.data[GeneralParams.DOMAIN].setdefault(config_entry.entry_id, {})
    hass.data[GeneralParams.DOMAIN][config_entry.entry_id]["api"] = api
    coordinator_parameters = (
        hass,
        config_entry,
        api,
    )
    thies_coordinator = SyncThiesDataCoordinator(*coordinator_parameters)
    backup_coordinator = LocalBackupCoordinator(*coordinator_parameters)

    try:
        await thies_coordinator.async_config_entry_first_refresh()
        await backup_coordinator.async_config_entry_first_refresh()

    except ValueError as ve:
        logclient.error(
            ErrorArgs(
                status=LogStatus.ERROR,
                metadata={"msg": f"ValueError during coordinator refresh: {ve}"},
            )
        )
        return False
    except ConnectionError as ce:
        logclient.error(
            ErrorArgs(
                status=LogStatus.ERROR,
                metadata={"msg": f"ConnectionError during coordinator refresh: {ce}"},
            )
        )
        return False
    except TimeoutError as te:
        logclient.error(
            ErrorArgs(
                status=LogStatus.ERROR,
                metadata={"msg": f"TimeoutError during coordinator refresh: {te}"},
            )
        )
        return False
    except RuntimeError as re:
        logclient.error(
            ErrorArgs(
                status=LogStatus.ERROR,
                metadata={"msg": f"RuntimeError during coordinator refresh: {re}"},
            )
        )
        return False
    hass.data[GeneralParams.DOMAIN][config_entry.entry_id][thies_coordinator.name] = (
        thies_coordinator
    )
    hass.data[GeneralParams.DOMAIN][config_entry.entry_id][backup_coordinator.name] = (
        backup_coordinator
    )
    logclient.debug(
        DebugArgs(
            status=LogStatus.SUCCESSFUL,
            metadata={"msg": "Coordinators setup successful"},
        )
    )

    await hass.config_entries.async_forward_entry_setups(
        config_entry, GeneralParams.PLATFORMS
    )
    if not hass.data[GeneralParams.DOMAIN].get("services_registered"):
        await async_setup_services(hass)
        hass.data[GeneralParams.DOMAIN]["services_registered"] = True
        logclient.debug(
            DebugArgs(
                status=LogStatus.SUCCESSFUL,
                metadata={"msg": "Services setup successful"},
            )
        )

    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload a config entry."""
    logclient.method_name = "async_unload_entry"
    logclient.debug(DebugArgs(status=LogStatus.STARTED))
    unload_ok = await hass.config_entries.async_unload_platforms(
        entry, GeneralParams.PLATFORMS
    )
    if unload_ok:
        hass.data[GeneralParams.DOMAIN].pop(entry.entry_id)

    if not hass.data[GeneralParams.DOMAIN]:
        await async_unload_services(hass)
    logclient.debug(
        DebugArgs(
            status=LogStatus.SUCCESSFUL,
            metadata={"msg": "Config entry unload successful"},
        )
    )
    return unload_ok
