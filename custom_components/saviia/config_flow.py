"""Config flow for SAVIIA integration."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

import voluptuous as vol
from homeassistant import config_entries
from homeassistant.data_entry_flow import FlowResult

from .const import DOMAIN, LOGGER

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
                    description="Hostname or IP address of the FTP server.",
                    default="localhost",
                ): str,
                vol.Required(
                    "ftp_port", description="Port number of the FTP server.", default=21
                ): int,
                vol.Required(
                    "ftp_user",
                    description="Username for the FTP server.",
                ): str,
                vol.Required(
                    "ftp_password",
                    description="Password for the FTP server.",
                ): str,
                vol.Required(
                    "sharepoint_client_id",
                    description="Client ID for SharePoint authentication.",
                ): str,
                vol.Required(
                    "sharepoint_client_secret",
                    description="Client secret for SharePoint authentication.",
                ): str,
                vol.Required(
                    "sharepoint_tenant_id",
                    description="Tenant ID for SharePoint authentication.",
                ): str,
                vol.Required(
                    "sharepoint_tenant_name",
                    description="Tenant name for SharePoint.",
                ): str,
                vol.Required(
                    "sharepoint_site_name",
                    description="Site name in SharePoint.",
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
                ftp_host = user_input.get("ftp_host")
                return self.async_create_entry(title="SAVIIA Credentials", data=user_input)
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
