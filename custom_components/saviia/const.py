"""Constants variables."""

import logging

import homeassistant.helpers.config_validation as cv
import voluptuous as vol
from dotenv import load_dotenv
from homeassistant.const import CONF_NAME, Platform

load_dotenv()

# General variables
DOMAIN = "saviia"
CONFIG_SCHEMA = vol.Schema(
    {
        DOMAIN: vol.Schema(
            {
                vol.Optional(CONF_NAME, default="SAVIIA"): cv.string,
            }
        )
    },
    extra=vol.ALLOW_EXTRA,
)
LOGGER = logging.getLogger(__package__)
PLATFORMS = [Platform.SENSOR]

# Remote extraction cycle
UPDATE_INTERVAL_HOURS = 1
UPDATE_INTERVAL_MINUTES = 0

# Services parameters

SERVICE_SYNC_FILES = "sync_files"
SERVICE_SYNC_FILES_SCHEMA = vol.Schema({})
