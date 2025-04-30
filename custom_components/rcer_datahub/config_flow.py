"""Config flow for RCER Data Hub integration."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

import voluptuous as vol
from homeassistant import config_entries
from homeassistant.data_entry_flow import FlowResult

from .const import DOMAIN

if TYPE_CHECKING:
    from homeassistant.data_entry_flow import FlowResult


class SyncThiesDataConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Config flow for Thies Data Logger."""

    VERSION = 1

    async def async_step_user(
        self, user_input: dict[str, Any] | None = None
    ) -> FlowResult:
        """Handle the initial step."""
        errors = {}
        if user_input is not None:
            try:
                return self.async_create_entry(title="RCER Data Hub", data=user_input)
            except ValueError:
                errors["base"] = "invalid_input"
        data_schema = vol.Schema(
            {
                vol.Required("ftp_host"): str,
                vol.Required("ftp_port"): int,
                vol.Required("ftp_user"): str,
                vol.Required("ftp_password"): str,
                vol.Required("sharepoint_client_id"): str,
                vol.Required("sharepoint_client_secret"): str,
                vol.Required("sharepoint_tenant_id"): str,
                vol.Required("sharepoint_tenant_name"): str,
                vol.Required("sharepoint_site_name"): str,
            }
        )

        return self.async_show_form(
            step_id="user", data_schema=data_schema, errors=errors
        )
