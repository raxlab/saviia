from homeassistant.core import HomeAssistant
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator
from rcer_iot_client_pkg import EpiiAPI

from custom_components.rcer_datahub.helpers.datetime_utils import datetime_to_str, today

from .const import EPII_API_CONFIG


class RCERDatahubUpdateCoordinator(DataUpdateCoordinator):
    """Class to manage remote extraction workflow at EPII."""

    def __init__(
        self, hass: HomeAssistant, api: EpiiAPI, logger, name, update_interval
    ) -> None:
        """Set up the coordinator."""
        self.api = api
        self.last_update = None
        self.data: dict[str, dict] = {}
        super().__init(
            hass,
            logger,
            name,
            update_interval,
            always_update=True,
        )

    async def _async_update_data(self) -> dict:
        """Upload data from RCER API and get response."""
        try:
            self.logger.debug("[coordinator] async_update_data_started")
            synced_files = await self.api.update_thies_data(EPII_API_CONFIG)
            self.data = synced_files
            self.last_update = datetime_to_str(today())
            self.logger.debug(
                "[coordinator] async_update_data_successful", extra=synced_files
            )
            return synced_files
        except Exception as e:
            self.logger.error(
                "[coordinator] async_update_data_error", extra={"error": e.__str__()}
            )
            raise
