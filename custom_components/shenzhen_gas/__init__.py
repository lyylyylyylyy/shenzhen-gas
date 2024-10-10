"""The Shenzhen Gas integration."""
from __future__ import annotations

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant

from .const import DOMAIN

PLATFORMS: list[str] = ["sensor"]

async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up Shenzhen Gas from a config entry."""
    hass.data.setdefault(DOMAIN, {})
    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)
    return True

async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload a config entry."""
    unload_ok = await hass.config_entries.async_unload_platforms(entry, PLATFORMS)
    if unload_ok:
        hass.data[DOMAIN].pop(entry.entry_id)
    return unload_ok

from homeassistant.components.http import HomeAssistantView
from aiohttp import web
import random

class RefreshCaptchaView(HomeAssistantView):
    url = "/shenzhen_gas/refresh_captcha"
    name = "shenzhen_gas:refresh_captcha"
    requires_auth = False

    async def get(self, request):
        """Handle refresh captcha request."""
        new_captcha_url = f"https://service.szgas.com.cn/login/kaptcha-image.jspx?{random.randint(1, 1000)}"
        return web.Response(status=302, headers={"Location": new_captcha_url})

async def async_setup(hass, config):
    """Set up the Shenzhen Gas component."""
    hass.http.register_view(RefreshCaptchaView())
    return True
