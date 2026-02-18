"""Constants variables."""

import logging

import homeassistant.helpers.config_validation as cv
import voluptuous as vol
from homeassistant.const import CONF_NAME, Platform


class GeneralParams:
    """General variables."""

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


class ServicesParams:
    """Services parameters."""

    SERVICE_SYNC_FILES = "sync_files"
    SERVICE_SYNC_FILES_SCHEMA = vol.Schema({})

    SERVICE_LOCAL_BACKUP = "sync_local_backup"
    SERVICE_LOCAL_BACKUP_SCHEMA = vol.Schema({})

    SERVICE_GET_NETCAMERA_RATES = "get_netcamera_rates"
    SERVICE_GET_NETCAMERA_RATES_SCHEMA = vol.Schema(
        {
            vol.Required("latitude"): cv.latitude,
            vol.Required("longitude"): cv.longitude,
        }
    )
    SERVICE_UPDATE_TASK = "update_task"
    SERVICE_UPDATE_TASK_SCHEMA = vol.Schema(
        {
            vol.Required("task"): dict,
            vol.Required("completed"): bool,
        }
    )
    SERVICE_DELETE_TASK = "delete_task"
    SERVICE_DELETE_TASK_SCHEMA = vol.Schema(
        {
            vol.Required("task_id"): cv.string,
        }
    )
    SERVICE_CREATE_TASK = "create_task"
    SERVICE_CREATE_TASK_SCHEMA = vol.Schema(
        {
            vol.Required("task"): dict,
            vol.Optional("images"): list,
        }
    )

    SERVICE_GET_TASKS = "get_tasks"
    SERVICE_GET_TASKS_SCHEMA = vol.Schema(
        {
            vol.Optional("params"): dict,
        }
    )


class ConfigDefaultsParams:
    """Config flow default parameters."""

    # - THIES Data Logger Synchronization
    DEFAULT_SHAREPOINT_THIES_AVG_FOLDER = (
        "Shared%20Documents/General/Test_Raspberry/THIES/AVG"
    )
    DEFAULT_SHAREPOINT_THIES_EXT_FOLDER = (
        "Shared%20Documents/General/Test_Raspberry/THIES/EXT"
    )

    DEFAULT_FTP_PATH_AVG = "ftp/thies/BINFILES/ARCH_AV1"
    DEFAULT_FTP_PATH_EXT = "ftp/thies/BINFILES/ARCH_EX1"

    # - Local Backup
    DEFAULT_SHAREPOINT_BASE_URL = "/sites/uc365_CentrosyEstacionesRegionalesUC/Shared%20Documents/General/Test_Raspberry"
    DEFAULT_LOCAL_BACKUP_PATH = "/media/backup_local"
