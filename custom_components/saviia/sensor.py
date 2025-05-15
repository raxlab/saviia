from typing import Any

from homeassistant.components.sensor import (
    SensorEntity,
)
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import DOMAIN
from .coordinator import SyncThiesDataCoordinator


async def async_setup_entry(
    hass: HomeAssistant,
    config_entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up SAVIIA sensor based on a config entry."""
    thies_coordinator = hass.data[DOMAIN][config_entry.entry_id]["thies_coordinator"]
    backup_coordinator = hass.data[DOMAIN][config_entry.entry_id]["local_backup_coordinator"]
    sensors = [
        SaviiaNewFilesSensor(thies_coordinator, config_entry),
        SaviiaFailedFilesSensor(thies_coordinator, config_entry),
        SaviiaFileSyncStatusSensor(thies_coordinator, config_entry),
        SaviiaBackupStatusSensor(backup_coordinator, config_entry)
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

    @property
    def data(self) -> dict[str, Any]:
        return self.coordinator.data.get("synced_files", {}) or {}

    @property
    def metadata(self) -> dict[str, Any]:
        return self.data.get("metadata", {}).get("data", {})

    @property
    def extra_state_attributes(self) -> dict[str, Any] | None:
        return {
            "last_update": self.coordinator.last_update,
            "error": self.metadata.get("error"),
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
        new_files_attributes = []
        if processed_files:
            new_files_attributes = [
                f"{name} [{info['processed_date']}|{info['file_size']} B]"
                for name, info in processed_files.items()
            ]
        return {
            **base,
            "new_files": self.metadata.get("new_files", []),
            "new_files_attributes": new_files_attributes,
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
        return {**base, "new_files": len(self.metadata.get("new_files", []))}

