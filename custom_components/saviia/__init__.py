"""SAVIIA Integration."""

from pathlib import Path

from homeassistant.components.frontend import async_register_built_in_panel
from homeassistant.components.http import StaticPathConfig
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from saviialib import SaviiaAPI, SaviiaAPIConfig

from custom_components.saviia.const import GeneralParams

from .coordinator import (
    LocalBackupCoordinator,
    NetcameraRatesCoordinator,
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

CONFIG_SCHEMA = GeneralParams.CONFIG_SCHEMA

logclient = LogClient(
    LogClientArgs(client_name="logging", service_name="init", class_name="init")
)


async def async_setup(hass: HomeAssistant, config: dict) -> bool:  # noqa: ARG001
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
            latitude=config_entry.data.get("latitude"),
            longitude=config_entry.data.get("longitude"),
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
    netcamera_rates_coordinator = NetcameraRatesCoordinator(*coordinator_parameters)

    try:
        await thies_coordinator.async_config_entry_first_refresh()
        await backup_coordinator.async_config_entry_first_refresh()
        await netcamera_rates_coordinator.async_config_entry_first_refresh()

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
    hass.data[GeneralParams.DOMAIN][config_entry.entry_id][
        netcamera_rates_coordinator.name
    ] = netcamera_rates_coordinator
    logclient.debug(
        DebugArgs(
            status=LogStatus.SUCCESSFUL,
            metadata={"msg": "Coordinators setup successful"},
        )
    )

    await hass.config_entries.async_forward_entry_setups(
        config_entry, GeneralParams.PLATFORMS
    )
    # Panel registration
    if not hass.data[GeneralParams.DOMAIN].get("services_registered"):
        await async_setup_services(hass)
        hass.data[GeneralParams.DOMAIN]["services_registered"] = True
        logclient.debug(
            DebugArgs(
                status=LogStatus.SUCCESSFUL,
                metadata={"msg": "Services setup successful"},
            )
        )
        # Panel setup
        await hass.http.async_register_static_paths(
            [
                StaticPathConfig(
                    url_path="/frontend/saviia-get-tasks",
                    path=str(Path(__file__).parent / "frontend"),
                    cache_headers=False,
                )
            ]
        )
        try:
            if await _panel_exists(hass, "saviia-get-tasks"):
                logclient.debug(
                    DebugArgs(
                        status=LogStatus.SUCCESSFUL,
                        metadata={
                            "msg": "SAVIIA Get Tasks Panel already exists, skipping registration"
                        },
                    )
                )
                return True
            async_register_built_in_panel(
                hass,
                component_name="custom",
                sidebar_title="SAVIIA Get Tasks",
                sidebar_icon="mdi:format-list-checks",
                frontend_url_path="saviia-get-tasks",
                require_admin=False,
                config={
                    "_panel_custom": {
                        "name": "saviia-get-tasks.panel",
                        "module_url": "/saviia/frontend/saviia-get-tasks.panel.js",
                        "embed_iframe": False,
                    }
                },
            )
            logclient.debug(
                DebugArgs(
                    status=LogStatus.SUCCESSFUL,
                    metadata={"msg": "Frontend registered at /saviia-all-tasks"},
                )
            )
        except Exception as e:  # noqa: BLE001
            logclient.error(
                ErrorArgs(
                    status=LogStatus.ERROR,
                    metadata={"msg": f"Error registering frontend: {e!s}"},
                )
            )

    # Setup of variables needed for services
    hass.data[GeneralParams.DOMAIN]["discord_webhook_url"] = config_entry.data.get(
        "discord_webhook_url"
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


async def _panel_exists(hass: HomeAssistant, panel_name: str) -> bool:
    try:
        return hasattr(hass.data, "frontend_panels") and panel_name in hass.data.get(
            "frontend_panels", {}
        )
    except Exception as e:  # noqa: BLE001
        logclient.debug(
            DebugArgs(
                status=LogStatus.SUCCESSFUL,
                metadata={"msg": f"Error checking pannel existence: {e!s}"},
            )
        )
        return False
