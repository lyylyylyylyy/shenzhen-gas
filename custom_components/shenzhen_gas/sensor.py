"""Support for Shenzhen Gas sensors."""
from __future__ import annotations

from homeassistant.components.sensor import SensorEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from .const import DOMAIN

async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up Shenzhen Gas sensor based on a config entry."""
    # TODO: Implement sensor setup
    pass

class ShenzhenGasSensor(SensorEntity):
    """Representation of a Shenzhen Gas sensor."""

    # TODO: Implement sensor class
    pass
