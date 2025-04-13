import os
from datetime import timedelta

from dotenv import load_dotenv
from homeassistant.core import HomeAssistant
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator

from ...libs.http_client import HTTPClient, HttpClientInitArgs
from .const import LOGGER, UPDATE_INTERVAL_HOURS, UPDATE_INTERVAL_MINUTES

load_dotenv()


class RCERDataHubCoordinator(DataUpdateCoordinator):
    """Class to manage remote extraction workflow from EPII"""

    def __init__(self, hass: HomeAssistant):
        super().__init(
            hass,
            LOGGER,
            name="rcer_datahub",
            update_interval=timedelta(
                hours=UPDATE_INTERVAL_HOURS, minutes=UPDATE_INTERVAL_MINUTES
            ),
        )
        self.http_client = HTTPClient(
            HttpClientInitArgs(
                client_name="request_client",
                access_token=os.getenv("MICROSOFT_GRAPH_ACCESS_TOKEN"),
                base_url="https://graph.microsoft.com/v1.0/"
            )
        )

    async def _async_setup(self) -> None:
        """Do Initialization logic"""

    async def _async_update_data(self):
        """Do usual update"""
