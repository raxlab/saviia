"""Config flow for SAVIIA integration."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

import voluptuous as vol
from homeassistant import config_entries
from homeassistant.data_entry_flow import FlowResult

from .const import (
    DEFAULT_FTP_PATH_EXT,
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
                vol.Required(
                    "ftp_host",
                    default="localhost",
                ): str,
                vol.Required("ftp_port", default=21): int,
                vol.Required(
                    "ftp_user",
                ): str,
                vol.Required(
                    "ftp_password",
                ): str,
                vol.Required(
                    "sharepoint_client_id",
                ): str,
                vol.Required(
                    "sharepoint_client_secret",
                ): str,
                vol.Required(
                    "sharepoint_tenant_id",
                ): str,
                vol.Required(
                    "sharepoint_tenant_name",
                ): str,
                vol.Required(
                    "sharepoint_site_name",
                ): str,  # THIES Data Logger Parameters
                vol.Required("thies_ftp_server_avg_path"): str,
                vol.Required(
                    "thies_ftp_server_ext_path", default=DEFAULT_FTP_PATH_EXT
                ): str,
                vol.Required("sharepoint_avg_backup_folder_name"): str,
                vol.Required(
                    "sharepoint_ext_backup_folder_name"
                ): str,  # Local Backup Parameters
                vol.Required("local_backup_source_path"): str,
                vol.Required("sharepoint_backup_base_url"): str,
                vol.Optional(
                    "notification_client_api_key",
                    description="Optional API key for Discord Bot client",
                ): str,
                vol.Optional(
                    "notification_channel_id",
                    description="Optional Channel ID for notifications of new tasks created using the Discord Bot",
                ): str,
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
