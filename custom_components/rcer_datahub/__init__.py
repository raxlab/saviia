"""RCER Data Hub Integration"""

import logging

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant, ServiceCall

from .const import DOMAIN
from .libs.ftp_client import FTPClient

_LOGGER = logging.getLogger(__name__)


async def async_setup(hass: HomeAssistant, entry: ConfigEntry):
    async def handle_ftp_list_files(call: ServiceCall):
        host = call.data.get("host")
        user = call.data.get("user")
        password = call.data.get("password")
        path = call.data.get("path", "/")

        try:
            ftp = FTPClient(host, user, password, path)
            files = ftp.list_files()
            _LOGGER.info(f"Files: {files}")
        except Exception as e:
            _LOGGER.error(f"FTP error: {e}")

    hass.services.async_register(DOMAIN, "ftp_list_files", handle_ftp_list_files)

    return True
