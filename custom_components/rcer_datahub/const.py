"""Constants variables."""

import logging
import os

import homeassistant.helpers.config_validation as cv
import voluptuous as vol
from dotenv import load_dotenv
from homeassistant.const import CONF_NAME, Platform
from rcer_iot_client_pkg import EpiiUpdateThiesConfig

load_dotenv()

# General variables
DOMAIN = "rcer_datahub"
CONFIG_SCHEMA = vol.Schema(
    {
        DOMAIN: vol.Schema(
            {
                vol.Optional(CONF_NAME, default="RCER Datahub"): cv.string,
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

# EPII API Configuration
EPII_API_CONFIG = EpiiUpdateThiesConfig(
    ftp_host=os.getenv("FTP_HOST"),
    ftp_port=int(os.getenv("FTP_PORT")),
    ftp_user=os.getenv("FTP_USER"),
    ftp_password=os.getenv("FTP_PASSWORD"),
    sharepoint_client_id=os.getenv("CLIENT_ID"),
    sharepoint_client_secret=os.getenv("CLIENT_SECRET"),
    sharepoint_tenant_id=os.getenv("TENANT_ID"),
    sharepoint_tenant_name=os.getenv("TENANT_NAME"),
    sharepoint_site_name=os.getenv("SITE_NAME"),
)

# Services parameters

SERVICE_SYNC_FILES = "sync_files"
SERVICE_SYNC_FILES_SCHEMA = vol.Schema({})
