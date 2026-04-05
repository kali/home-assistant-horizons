from __future__ import annotations

from datetime import datetime, timezone

from homeassistant.components.sensor import SensorEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback

class HorizonsTestSensor(SensorEntity):
    _attr_name = "Horizons Test"
    _attr_unique_id = "horizons_test"
    _attr_icon = "mdi:weather-sunset"

    @property
    def native_value(self):
        return datetime.now(timezone.utc).isoformat()

async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    async_add_entities([HorizonsTestSensor()])
