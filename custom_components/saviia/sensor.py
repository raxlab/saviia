from typing import Any

from homeassistant.components.sensor import (
    SensorEntity,
)
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import GeneralParams
from .coordinator import SyncThiesDataCoordinator


async def async_setup_entry(
    hass: HomeAssistant,
    config_entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up SAVIIA sensor based on a config entry."""
    thies_coordinator = hass.data[GeneralParams.DOMAIN][config_entry.entry_id][
        "thies_coordinator"
    ]
    backup_coordinator = hass.data[GeneralParams.DOMAIN][config_entry.entry_id][
        "local_backup_coordinator"
    ]

    sensors = [
        SaviiaNewFilesSensor(thies_coordinator, config_entry),
        SaviiaFailedFilesSensor(thies_coordinator, config_entry),
        SaviiaFileSyncStatusSensor(thies_coordinator, config_entry),
        SaviiaBackupStatusSensor(backup_coordinator, config_entry),
    ]
    async_add_entities(sensors, update_before_add=True)


class SaviiaBaseSensor(CoordinatorEntity, SensorEntity):
    """Sensor to display the list of uploaded files to SharePoint folder."""

    def __init__(
        self,
        coordinator: SyncThiesDataCoordinator,
        config_entry: ConfigEntry,
        attribute: str,
        name_suffix: str,
        icon: str | None = None,
    ) -> None:
        super().__init__(coordinator)
        self._attr_unique_id = f"{config_entry.entry_id}_{attribute}"
        self._attr_name = f"{config_entry.title} - {name_suffix}"
        self._attribute = attribute
        self._attr_icon = icon or "mdi:file"
        self.coordinator = coordinator

    @property
    def data(self) -> dict[str, Any]:
        coordinator_response = {
            "thies_coordinator": "synced_files",
            "local_backup_coordinator": "exported_files",
        }
        if coordinator_response.get(self.coordinator.name):
            return (
                self.coordinator.data.get(
                    coordinator_response[self.coordinator.name], {}
                )
                or {}
            )
        error_message = "Invalid coordinator name."
        raise KeyError(error_message)

    @property
    def metadata(self) -> dict[str, Any]:
        return self.data.get("metadata", {}).get("data", {})

    @property
    def extra_state_attributes(self) -> dict[str, Any] | None:
        return {
            "last_update": self.coordinator.last_update,
            "error": self.data.get("metadata", {}).get("error", {}),
        }


class SaviiaFileSyncStatusSensor(SaviiaBaseSensor):
    """Sensor for overall sync status message."""

    def __init__(self, coordinator, config_entry):
        super().__init__(
            coordinator,
            config_entry,
            attribute="sync_status",
            name_suffix="File Sync Status",
            icon="mdi:file-cloud-upload",
        )

    @property
    def native_value(self) -> str | None:
        message = self.data.get("message", "No sync message")
        server_status = self.data.get("status")
        return f"[{server_status}] {message}"

    @property
    def extra_state_attributes(self) -> dict[str, Any]:
        base = super().extra_state_attributes or {}
        server_status = self.data.get("status")
        return {**base, "status": server_status}


class SaviiaNewFilesSensor(SaviiaBaseSensor):
    """Sensor for number of new uploaded files."""

    def __init__(self, coordinator, config_entry):
        super().__init__(
            coordinator,
            config_entry,
            attribute="new_files",
            name_suffix="New Uploaded Files",
            icon="mdi:file-plus",
        )

    @property
    def native_value(self) -> int:
        return len(self.metadata.get("new_files", []))

    @property
    def extra_state_attributes(self) -> dict[str, Any]:
        base = super().extra_state_attributes or {}
        processed_files = self.metadata.get("processed_files", {})
        return {
            **base,
            "new_files": self.metadata.get("new_files", []),
            "new_files_attributes": processed_files,
        }


class SaviiaFailedFilesSensor(SaviiaBaseSensor):
    """Sensor for number of failed file uploads."""

    def __init__(self, coordinator, config_entry):
        super().__init__(
            coordinator,
            config_entry,
            attribute="failed_files",
            name_suffix="Failed Uploads",
            icon="mdi:file-alert",
        )

    @property
    def native_value(self) -> int:
        return len(self.metadata.get("failed_files", []))

    @property
    def extra_state_attributes(self) -> dict[str, Any]:
        base = super().extra_state_attributes or {}
        return {**base, "failed_files": self.metadata.get("failed_files", [])}


class SaviiaBackupStatusSensor(SaviiaBaseSensor):
    """Sensor for backup status."""

    def __init__(self, coordinator, config_entry):
        super().__init__(
            coordinator,
            config_entry,
            attribute="backup_status",
            name_suffix="Backup Status",
            icon="mdi:backup-restore",
        )

    @property
    def native_value(self) -> str | None:
        message = self.data.get("message", "No sync message")
        server_status = self.data.get("status")
        return f"[{server_status}] {message}"

    @property
    def extra_state_attributes(self) -> dict[str, Any]:
        base = super().extra_state_attributes or {}
        return {**base, "new_files": self.metadata.get("new_files", 0)}
