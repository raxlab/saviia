"""Config flow for SAVIIA integration."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

import voluptuous as vol
from homeassistant import config_entries
from homeassistant.data_entry_flow import FlowResult
from homeassistant.const import (
    CONF_HOST,
    CONF_PORT,
    CONF_USERNAME,
    CONF_PASSWORD,
    CONF_API_KEY,
    CONF_CLIENT_ID,
    CONF_CLIENT_SECRET,
)

from .const import (
    DOMAIN,
    LOGGER,
)

if TYPE_CHECKING:
    from homeassistant.data_entry_flow import FlowResult


class SaviiaConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Config flow for Thies Data Logger."""

    VERSION = 1

    def _get_schema(self) -> vol.Schema:
        return vol.Schema(
            {
                # FTP
                vol.Required(CONF_HOST, default="localhost"): str,
                vol.Required(CONF_PORT, default=21): int,
                vol.Required(CONF_USERNAME): str,
                vol.Required(CONF_PASSWORD): str,
                # SharePoint / Microsoft
                vol.Required(CONF_CLIENT_ID): str,
                vol.Required(CONF_CLIENT_SECRET): str,
                vol.Required("tenant_id"): str,
                vol.Required("tenant_name"): str,
                vol.Required("site_name"): str,
                # THIES
                vol.Required("thies_ftp_server_avg_path"): str,
                vol.Required(
                    "thies_ftp_server_ext_path",
                    default=DEFAULT_FTP_PATH_EXT,
                ): str,
                # Backups
                vol.Required("sharepoint_avg_backup_folder_name"): str,
                vol.Required("sharepoint_ext_backup_folder_name"): str,
                vol.Required("local_backup_source_path"): str,
                vol.Required("sharepoint_backup_base_url"): str,
                # Notifications (optional)
                vol.Optional(CONF_API_KEY): str,
                vol.Optional("notification_channel_id"): str,
            }
        )

    async def async_step_user(
        self, user_input: dict[str, Any] | None = None
    ) -> FlowResult:
        """Handle the initial step."""
        errors = {}
        if user_input is not None:
            try:
                # Validate FTP port
                ftp_port = user_input.get("ftp_port")
                if not isinstance(ftp_port, int):
                    errors["ftp_port"] = "invalid_port"
                    return self.async_show_form(
                        step_id="user", data=self._get_schema(), errors=errors
                    )
                return self.async_create_entry(
                    title="SAVIIA Credentials", data=user_input
                )
            except ValueError as e:
                LOGGER.error(f"Value error during config flow: {e}")
                errors["base"] = "invalid_input"
            except vol.Invalid as e:
                LOGGER.error(f"Schema validation error: {e}")
                errors["base"] = "invalid_schema"
            except OSError as e:
                LOGGER.error(f"OS error during config flow: {e}")
                errors["base"] = "os_error"
            except RuntimeError as e:
                LOGGER.error(f"Runtime error during config flow: {e}")
                errors["base"] = "runtime_error"

        return self.async_show_form(
            step_id="user", data_schema=self._get_schema(), errors=errors
        )
