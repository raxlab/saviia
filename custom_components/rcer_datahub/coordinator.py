from datetime import timedelta, timezone

from homeassistant.helpers.update_coordinator import DataUpdateCoordinator

from .const import LOGGER, UPDATE_INTERVAL_HOURS, UPDATE_INTERVAL_MINUTES


class RCERDataHubCoordinator(DataUpdateCoordinator):
    """Class to manage remote extraction workflow from EPII"""

    def __init__(self, hass, ftp_client, http_client):
        self.ftp_client = ftp_client
        self.http_client = http_client
        super().__init(
            hass,
            LOGGER,
            name="rcer_datahub",
            update_interval=timedelta(
                hours=UPDATE_INTERVAL_HOURS, minutes=UPDATE_INTERVAL_MINUTES
            ),
        )

    # async def _async_update_data(self).
        