
from homeassistant.components.sensor import (
    SensorEntity,
)
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import DOMAIN
from .coordinator import RCERDatahubUpdateCoordinator


async def async_setup_entry(
    hass: HomeAssistant,
    config_entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up RCER Data hub sensor based on a config entry."""
    coordinator = hass.data[DOMAIN][config_entry.entry_id]["coordinator"]
    sensors = [FileUploadSensor(coordinator)]
    async_add_entities(sensors, update_before_add=True)


class FileUploadSensor(CoordinatorEntity, SensorEntity):
    """Sensor to display the list of uploaded files to SharePoint folder."""

    _attr_name = "Uploaded Files"
    _attr_icon = "mdi:file-cloud-upload"

    def __init__(self, coordinator: RCERDatahubUpdateCoordinator) -> None:
        super().__init__(coordinator)

    @property
    def native_value(self) -> str | None:
        return (
            self.coordinator.data if self.coordinator.data else "No files uploaded yet."
        )
