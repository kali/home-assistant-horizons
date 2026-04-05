from __future__ import annotations

import logging

import voluptuous as vol
from aiohttp import ClientSession

from homeassistant import config_entries
from homeassistant.helpers.aiohttp_client import async_get_clientsession

from .const import (
    CONF_LATITUDE,
    CONF_LONGITUDE,
    CONF_PROFILE_POINTS,
    CONF_PROFILE_RESOLUTION_DEG,
    CONF_PROFILE_SOURCE,
    DOMAIN,
    PROFILE_SOURCE_PVGIS,
    PVGIS_PROFILE_RESOLUTION_DEG,
)
from .pvgis import PvgisConnectionError, PvgisResponseError, async_fetch_horizon_profile

_LOGGER = logging.getLogger(__name__)


class HorizonsConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    VERSION = 1

    async def async_step_user(self, user_input=None):
        errors: dict[str, str] = {}

        if user_input is not None:
            latitude = user_input[CONF_LATITUDE]
            longitude = user_input[CONF_LONGITUDE]

            await self.async_set_unique_id(f"{round(latitude, 6)},{round(longitude, 6)}")
            self._abort_if_unique_id_configured()

            session: ClientSession = async_get_clientsession(self.hass)

            try:
                profile_points = await async_fetch_horizon_profile(
                    session=session,
                    latitude=latitude,
                    longitude=longitude,
                )
            except PvgisConnectionError:
                errors["base"] = "cannot_connect"
            except PvgisResponseError:
                errors["base"] = "invalid_response"
            except Exception:
                _LOGGER.exception("Unexpected error while fetching PVGIS horizon profile")
                errors["base"] = "unknown"
            else:
                return self.async_create_entry(
                    title=f"Horizons ({latitude:.4f}, {longitude:.4f})",
                    data={
                        CONF_LATITUDE: latitude,
                        CONF_LONGITUDE: longitude,
                        CONF_PROFILE_SOURCE: PROFILE_SOURCE_PVGIS,
                        CONF_PROFILE_RESOLUTION_DEG: PVGIS_PROFILE_RESOLUTION_DEG,
                        CONF_PROFILE_POINTS: profile_points,
                    },
                )

        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema(
                {
                    vol.Required(CONF_LATITUDE, default=self.hass.config.latitude): float,
                    vol.Required(CONF_LONGITUDE, default=self.hass.config.longitude): float,
                }
            ),
            errors=errors,
        )
