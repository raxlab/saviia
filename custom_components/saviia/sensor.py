from homeassistant.components.sensor import (
    SensorEntity,
)
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import DOMAIN
from .coordinator import SyncThiesDataCoordinator
from typing import Any

async def async_setup_entry(
    hass: HomeAssistant,
    config_entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up SAVIIA sensor based on a config entry."""
    coordinator = hass.data[DOMAIN][config_entry.entry_id]
    sensors = [
        SaviiaNewFilesSensor(coordinator, config_entry),
        SaviiaFailedFilesSensor(coordinator, config_entry),
        SaviiaFileSyncStatusSensor(coordinator, config_entry),
        SaviiaOverwrittenFilesSensor(coordinator, config_entry),
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
        return self.data.get("metadata", {}) or {}

    @property
    def native_value(self) -> str | None:
        data = self.coordinator.data or {}
        return data.get("synced_files", {}).get("message", "No data yet.")

    @property
    def extra_state_attributes(self) -> dict[str, Any] | None:
        return {
            "last_updated": self.coordinator.last_updated,
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
        return {**base, "new_files": self.metadata.get("new_files", [])}


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


class SaviiaOverwrittenFilesSensor(SaviiaBaseSensor):
    """Sensor for number of overwritten files during sync."""

    def __init__(self, coordinator, config_entry):
        super().__init__(
            coordinator,
            config_entry,
            attribute="overwritten_files",
            name_suffix="Overwritten Files",
            icon="mdi:file-rotate-left",
        )

    @property
    def native_value(self) -> int:
        return len(self.metadata.get("overwritten_files", []))

    @property
    def extra_state_attributes(self) -> dict[str, Any]:
        base = super().extra_state_attributes or {}
        return {**base, "overwritten_files": self.metadata.get("overwritten_files", [])}
