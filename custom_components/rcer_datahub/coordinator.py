from dotenv import load_dotenv
from homeassistant.core import HomeAssistant
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator

from custom_components.rcer_datahub.api.rcer_datahub_api import RCERDatahubAPI
from custom_components.rcer_datahub.helpers.datetime_utils import datetime_to_str, today

load_dotenv()


class RCERDatahubUpdateCoordinator(DataUpdateCoordinator):
    """Class to manage remote extraction workflow at EPII."""

    def __init__(
        self, hass: HomeAssistant, api: RCERDatahubAPI, logger, name, update_interval
    ) -> None:
        self.api = api
        self.last_update = None
        super().__init(
            hass=hass,
            logger=logger,
            name=name,
            update_interval=update_interval,
            always_update=True,
        )

    async def _async_update_data(self) -> dict:
        """Upload data from RCER API and get response."""
        self.logger.debug("[coordinator] async_update_date_started")
        synced_files = await self.api.syncronize_thies_data_to_cloud()
        self.last_update = datetime_to_str(today())
        self.logger.debug("[coordinator] async_update_date_successful", extra=synced_files)
        return synced_files
