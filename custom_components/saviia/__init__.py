"""SAVIIA Integration."""

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from saviialib import SaviiaAPI, SaviiaAPIConfig

from custom_components.saviia.const import (
    CONFIG_SCHEMA,
    DOMAIN,
    LOGGER,
    PLATFORMS,
)

from .coordinator import (
    LocalBackupCoordinator,
    SyncThiesDataCoordinator,
    TasksCoordinator,
)
from .services import async_setup_services, async_unload_services


async def async_setup(hass: HomeAssistant, config: dict) -> bool:
    """Set up the SAVIIA component."""
    config = CONFIG_SCHEMA(config)
    if not hass.config_entries.async_entries(DOMAIN):
        hass.async_create_task(
            hass.config_entries.flow.async_init(DOMAIN, context={"source": "user"})
        )
    return True


async def async_setup_entry(hass: HomeAssistant, config_entry: ConfigEntry) -> bool:
    """Set up coordinator from a config entry."""
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
            logger=LOGGER,
            notification_client_api_key=config_entry.data.get(
                "notification_client_api_key", ""
            ),
        )
    )
    hass.data.setdefault(DOMAIN, {})
    hass.data[DOMAIN].setdefault(config_entry.entry_id, {})
    hass.data[DOMAIN][config_entry.entry_id]["api"] = api
    LOGGER.debug("[init] async_setup_entry_started")
    coordinator_parameters = (
        hass,
        config_entry,
        api,
    )
    thies_coordinator = SyncThiesDataCoordinator(*coordinator_parameters)
    backup_coordinator = LocalBackupCoordinator(*coordinator_parameters)
    tasks_coordinator = TasksCoordinator(*coordinator_parameters)

    try:
        await thies_coordinator.async_config_entry_first_refresh()
        await backup_coordinator.async_config_entry_first_refresh()
        await tasks_coordinator.async_config_entry_first_refresh()
    except ValueError as ve:
        LOGGER.error(f"[init] ValueError during coordinator refresh: {ve}")
        return False
    except ConnectionError as ce:
        LOGGER.error(f"[init] ConnectionError during coordinator refresh: {ce}")
        return False
    except TimeoutError as te:
        LOGGER.error(f"[init] TimeoutError during coordinator refresh: {te}")
        return False
    except RuntimeError as re:
        LOGGER.error(f"[init] RuntimeError during coordinator refresh: {re}")
        return False
    hass.data[DOMAIN][config_entry.entry_id][thies_coordinator.name] = thies_coordinator
    hass.data[DOMAIN][config_entry.entry_id][backup_coordinator.name] = (
        backup_coordinator
    )
    hass.data[DOMAIN][config_entry.entry_id][tasks_coordinator.name] = tasks_coordinator

    LOGGER.debug(f"[init] coordinator saved: {hass.data[DOMAIN]}")

    await hass.config_entries.async_forward_entry_setups(config_entry, PLATFORMS)
    if not hass.data[DOMAIN].get("services_registered"):
        await async_setup_services(hass)
        hass.data[DOMAIN]["services_registered"] = True
    LOGGER.debug("[init] async_setup_entry_successful")
    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload a config entry."""
    LOGGER.debug("[init] async_unload_entry_started")
    unload_ok = await hass.config_entries.async_unload_platforms(entry, PLATFORMS)
    if unload_ok:
        hass.data[DOMAIN].pop(entry.entry_id)

    if not hass.data[DOMAIN]:
        await async_unload_services(hass)
    LOGGER.debug("[init] async_unload_entry_successful")
    return unload_ok
