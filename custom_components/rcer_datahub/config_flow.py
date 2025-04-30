"""Config flow for RCER Data Hub integration."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

import voluptuous as vol
from homeassistant import config_entries
from homeassistant.data_entry_flow import FlowResult
from rcer_iot_client_pkg import EpiiUpdateThiesConfig

from .const import DOMAIN, LOGGER

if TYPE_CHECKING:
    from homeassistant.data_entry_flow import FlowResult


class ConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Config flow for RCER Data Hub."""

    async def async_step_user(
        self, user_input: dict[str, Any] | None = None
    ) -> FlowResult:
        """Handle the initial step."""
        errors = {}
        if user_input is not None:
            try:
                EpiiUpdateThiesConfig(
                    ftp_host=user_input["ftp_host"],
                    ftp_port=user_input["ftp_port"],
                    ftp_user=user_input["ftp_user"],
                    ftp_password=user_input["ftp_password"],
                    sharepoint_client_id=user_input["sharepoint_client_id"],
                    sharepoint_client_secret=user_input["sharepoint_client_secret"],
                    sharepoint_tenant_id=user_input["sharepoint_tenant_id"],
                    sharepoint_tenant_name=user_input["sharepoint_tenant_name"],
                    sharepoint_site_name=user_input["sharepoint_site_name"],
                )
                return self.async_create_entry(title="RCER Data Hub", data=user_input)
            except ValueError:
                errors["base"] = "invalid_input"
            except Exception as e:
                LOGGER.exception(f"Unexpected exception: {e}")
                errors["base"] = "unknown"
                raise
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
