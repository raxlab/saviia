from datetime import timedelta

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.update_coordinator import (
    DataUpdateCoordinator,
)
from saviialib import SaviiaAPI

from custom_components.saviia.helpers.datetime_utils import datetime_to_str, today
from custom_components.saviia.libs.log_client import (
    DebugArgs,
    ErrorArgs,
    LogClient,
    LogClientArgs,
    LogStatus,
)

from .const import GeneralParams


class SaviiaBaseCoordinator(DataUpdateCoordinator):
    def __init__(
        self,
        hass: HomeAssistant,
        config_entry: ConfigEntry,
        api: SaviiaAPI,
    ) -> None:
        """Set up the coordinator."""
        super().__init__(
            hass,
            GeneralParams.LOGGER,
            name=GeneralParams.MANUFACTURER,
            config_entry=config_entry,
            update_interval=None,
        )
        self.api = api
        self.config_entry = config_entry
        self.last_update: str | None = None
        self.data: dict[str, dict] = {}


class SyncThiesDataCoordinator(SaviiaBaseCoordinator):
    """Class to manage remote extraction workflow for Thies Data Logger."""

    def __init__(self, hass, config_entry, api: SaviiaAPI):
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
        self.local_backup_path = config_entry.data["local_backup_source_path"]
        self.thies_service = api.get("thies")
        self.logclient = LogClient(
            LogClientArgs(
                client_name="logging",
                service_name="coordinators",
                class_name="sync_thies_data_coordinator",
            )
        )

    async def _async_update_data(self) -> dict:
        """Upload data using the SAVIIA library and get uploaded files."""
        self.logclient.method_name = "_async_update_data"
        self.logclient.debug(
            DebugArgs(
                status=LogStatus.STARTED, metadata={"msg": "Thies data sync started"}
            )
        )
        try:
            synced_files = await self.thies_service.update_thies_data(
                sharepoint_folders_path=self.sharepoint_folders_path,
                ftp_server_folders_path=self.ftp_server_folders_path,
                local_backup_source_path=self.local_backup_path,
            )
            self.data = synced_files
            self.last_update = datetime_to_str(today())
            self.logclient.debug(
                DebugArgs(
                    status=LogStatus.SUCCESSFUL,
                    metadata={
                        "msg": f"Thies data sync completed. Data: {synced_files}"
                    },
                )
            )
            return {"synced_files": synced_files}
        except Exception as e:
            self.logclient.error(
                ErrorArgs(
                    status=LogStatus.ERROR,
                    metadata={"msg": e.__str__()},
                )
            )
            raise


class LocalBackupCoordinator(SaviiaBaseCoordinator):
    """Class to manage the Local Backup."""

    def __init__(self, hass, config_entry, api):
        super().__init__(hass, config_entry, api)
        self.name = "local_backup_coordinator"
        self.local_backup_source_path = config_entry.data["local_backup_source_path"]
        self.sharepoint_backup_base_url = config_entry.data[
            "sharepoint_backup_base_url"
        ]
        self.backup_service = api.get("backup")
        self.logclient = LogClient(
            LogClientArgs(
                client_name="logging",
                service_name="coordinators",
                class_name="local_backup_coordinator",
            )
        )

    async def _async_update_data(self) -> dict:
        """Execute the local backup, extracting files from the source path requested."""
        self.logclient.method_name = "_async_update_data"
        self.logclient.debug(
            DebugArgs(
                status=LogStatus.STARTED, metadata={"msg": "Local backup started"}
            )
        )
        try:
            exported_files = await self.backup_service.upload_backup_to_sharepoint(
                local_backup_source_path=self.local_backup_source_path,
                sharepoint_destination_path=self.sharepoint_backup_base_url,
            )
            self.data = exported_files
            self.last_update = datetime_to_str(today())
            self.logclient.debug(
                DebugArgs(
                    status=LogStatus.SUCCESSFUL,
                    metadata={"msg": f"Local backup completed. Data: {exported_files}"},
                )
            )

            return {"exported_files": exported_files}
        except Exception as e:
            self.logclient.error(
                ErrorArgs(
                    status=LogStatus.ERROR,
                    metadata={"msg": e.__str__()},
                )
            )
            raise


class NetcameraRatesCoordinator(SaviiaBaseCoordinator):
    """Class to manage the Netcamera time rates fetching."""

    def __init__(self, hass, config_entry, api):
        super().__init__(hass, config_entry, api)
        self.name = "netcamera_rates_coordinator"
        self.latitude = config_entry.data["latitude"]
        self.longitude = config_entry.data["longitude"]
        self.update_interval = timedelta(minutes=10)
        self.camera_service = api.get("netcamera")
        self.logclient = LogClient(
            LogClientArgs(
                client_name="logging",
                service_name="coordinators",
                class_name="netcamera_rates_coordinator",
            )
        )

    async def _async_update_data(self) -> dict:
        """Fetch netcamera time rates based on latitude and longitude."""
        self.logclient.method_name = "_async_update_data"
        self.logclient.debug(
            DebugArgs(
                status=LogStatus.STARTED,
                metadata={"msg": "Netcamera rates fetching started"},
            )
        )
        try:
            netcamera_rates = await self.camera_service.get_camera_rates()
            self.data = netcamera_rates
            self.last_update = datetime_to_str(today())
            self.logclient.debug(
                DebugArgs(
                    status=LogStatus.SUCCESSFUL,
                    metadata={
                        "msg": f"Netcamera rates fetching completed. Data: {netcamera_rates}"
                    },
                )
            )
            return {"netcamera_rates": netcamera_rates}
        except Exception as e:
            self.logclient.error(
                ErrorArgs(
                    status=LogStatus.ERROR,
                    metadata={"msg": e.__str__()},
                )
            )
            raise
