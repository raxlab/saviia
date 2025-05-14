"""Constants variables."""

import logging

import homeassistant.helpers.config_validation as cv
import voluptuous as vol
from dotenv import load_dotenv
from homeassistant.const import CONF_NAME, Platform

load_dotenv()

# General variables
DOMAIN = "saviia"
MANUFACTURER = "raxlab"
CONFIG_SCHEMA = vol.Schema(
    {
        DOMAIN: vol.Schema(
            {
                vol.Optional(CONF_NAME, default=DOMAIN): cv.string,
            }
        )
    },
    extra=vol.ALLOW_EXTRA,
)
LOGGER = logging.getLogger(__package__)
PLATFORMS = [Platform.SENSOR]

# Sharepoint coordinator parameters
LOCAL_BACKUP_PATH = "/media/backup_local"
DESTINATION_FOLDERS = {"0_Camaras_Trampa": "Camaras_Trampa"}

# Services parameters

SERVICE_SYNC_FILES = "sync_files"
SERVICE_SYNC_FILES_SCHEMA = vol.Schema({})

SERVICE_LOCAL_BACKUP = "sync_local_backup"
SERVICE_LOCAL_BACKUP_SCHEMA = vol.Schema({})
