from homeassistant.config_entries import ConfigEntry  # type: ignore
from homeassistant.core import HomeAssistant  # type: ignore
from homeassistant.helpers.update_coordinator import (  # type: ignore
    DataUpdateCoordinator,  # type: ignore
)
from saviialib import EpiiAPI  # type: ignore

from custom_components.saviia.helpers.datetime_utils import datetime_to_str, today

from .const import LOGGER, MANUFACTURER


class SaviiaBaseCoordinator(DataUpdateCoordinator):
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
            update_interval=None,
        )
        self.api = api
        self.config_entry = config_entry
        self.last_update: str | None = None
        self.data: dict[str, dict] = {}


class SyncThiesDataCoordinator(SaviiaBaseCoordinator):
    """Class to manage remote extraction workflow at EPII."""

    def __init__(self, hass, config_entry, api):
        super().__init__(hass, config_entry, api)
        self.name = "thies_coordinator"
        self.sharepoint_folders_path = [
            config_entry.data["sharepoint_avg_backup_folder_name"],
            config_entry.data["sharepoint_ext_backup_folder_name"],
        ]
        self.ftp_server_folders_path = [
            config_entry.data["thies_ftp_server_avg_path"],
            config_entry.data["thies_ftp_server_ext_path"],
        ]

    async def _async_update_data(self) -> dict:
        """Upload data using the Epii API from SAVIIA library and get uploaded files."""
        self.logger.info("[%s] async_update_data_started", self.name)
        try:
            synced_files = await self.api.update_thies_data(
                sharepoint_folders_path=self.sharepoint_folders_path,
                ftp_server_folders_path=self.ftp_server_folders_path,
            )
            self.data = synced_files
            self.last_update = datetime_to_str(today())
            self.logger.info(
                "[%s] async_update_data_successful %s", self.name, synced_files
            )
            return {"synced_files": synced_files}
        except Exception as e:
            self.logger.info(
                "[%s] async_update_data_error: %s",
                self.name,
                e.__str__(),
            )
            raise


class LocalBackupCoordinator(SaviiaBaseCoordinator):
    """Class to manage Local Backup at EPII."""

    def __init__(self, hass, config_entry, api):
        super().__init__(hass, config_entry, api)
        self.name = "local_backup_coordinator"
        self.local_backup_source_path = config_entry.data["local_backup_source_path"]
        self.sharepoint_backup_base_url = config_entry.data["sharepoint_backup_base_url"]

    async def _async_update_data(self) -> dict:
        """Execute the local backup, extracting files from the source path requested."""
        self.logger.info("[%s] async_local_backup_started", self.name)
        try:
            exported_files = await self.api.upload_backup_to_sharepoint(
                local_backup_source_path=self.local_backup_source_path,
                sharepoint_destination_path=self.sharepoint_backup_base_url,
            )
            self.data = exported_files
            self.last_update = datetime_to_str(today())
            self.logger.info(
                "[%s] async_update_data_successful: %s", self.name, exported_files
            )
            return {"exported_files": exported_files}
        except Exception as e:
            self.logger.info(
                "[%s] async_update_data_error",
                e.__str__(),
            )
            raise
