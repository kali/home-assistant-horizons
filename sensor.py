from __future__ import annotations

from homeassistant.components.sensor import SensorEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from .const import CONF_PROFILE_POINTS


class HorizonsProfilePointCountSensor(SensorEntity):
    def __init__(self, entry: ConfigEntry) -> None:
        self._entry = entry
        self._attr_unique_id = f"{entry.entry_id}_profile_points"
        self._attr_name = "Horizons Profile Points"
        self._attr_icon = "mdi:terrain"

    @property
    def native_value(self) -> int:
        return len(self._entry.data.get(CONF_PROFILE_POINTS, []))


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    async_add_entities([HorizonsProfilePointCountSensor(entry)])
