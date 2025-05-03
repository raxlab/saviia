from datetime import timedelta

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator
from saviialib import EpiiAPI, EpiiUpdateThiesConfig

from custom_components.saviia.helpers.datetime_utils import datetime_to_str, today

from .const import (
    LOGGER,
    MANUFACTURER,
    UPDATE_INTERVAL_DAYS,
    UPDATE_INTERVAL_HOURS,
    UPDATE_INTERVAL_MINUTES,
)


class SyncThiesDataCoordinator(DataUpdateCoordinator):
    """Class to manage remote extraction workflow at EPII."""

    def __init__(
        self,
        hass: HomeAssistant,
        config_entry: ConfigEntry,
        api: EpiiAPI,
    ) -> None:
        """Set up the coordinator."""
        super().__init__(
            hass,
            LOGGER,
            name=MANUFACTURER,
            config_entry=config_entry,
            update_interval=timedelta(
                days=UPDATE_INTERVAL_DAYS,
                hours=UPDATE_INTERVAL_HOURS,
                minutes=UPDATE_INTERVAL_MINUTES,
            ),
            always_update=True,
        )
        self.api = api
        self.config_entry = config_entry
        self.update_thies_config = EpiiUpdateThiesConfig(
            ftp_port=config_entry.data["ftp_port"],
            ftp_host=config_entry.data["ftp_host"],
            ftp_user=config_entry.data["ftp_user"],
            ftp_password=config_entry.data["ftp_password"],
            sharepoint_client_id=config_entry.data["sharepoint_client_id"],
            sharepoint_client_secret=config_entry.data["sharepoint_client_secret"],
            sharepoint_tenant_id=config_entry.data["sharepoint_tenant_id"],
            sharepoint_tenant_name=config_entry.data["sharepoint_tenant_name"],
            sharepoint_site_name=config_entry.data["sharepoint_site_name"],
        )
        self.last_update: str | None = None
        self.data: dict[str, dict] = {}

    async def _async_update_data(self) -> dict:
        """Upload data using the Epii API from SAVIIA library and get uploaded files."""
        self.logger.debug("[coordinator] async_update_data_started")
        try:
            synced_files = await self.api.update_thies_data(self.update_thies_config)
            self.data = synced_files
            self.last_update = datetime_to_str(today())
            self.logger.debug(
                "[coordinator] async_update_data_successful %s",
                synced_files,
            )
            return {"synced_files": synced_files}
        except Exception as e:
            self.logger.error(
                "[coordinator] async_update_data_error",
                extra={"error": e.__str__()},
            )
            raise
