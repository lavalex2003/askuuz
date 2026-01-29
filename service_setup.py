from __future__ import annotations

from homeassistant.core import HomeAssistant
from homeassistant.config_entries import ConfigEntry

from .const import DOMAIN


async def async_setup_service(
    hass: HomeAssistant,
    entry: ConfigEntry,
    coordinator_cls,
) -> bool:
    coordinator = coordinator_cls(
        hass,
        entry.entry_id,
        entry.data["username"],
        entry.data["password"],
        entry.data["account_id"],
        options=entry.data,
    )

    hass.data.setdefault(DOMAIN, {})
    hass.data[DOMAIN][entry.entry_id] = coordinator

    await coordinator.async_config_entry_first_refresh()
    return True


async def async_unload_service(
    hass: HomeAssistant,
    entry: ConfigEntry,
) -> bool:
    hass.data[DOMAIN].pop(entry.entry_id, None)
    return True
