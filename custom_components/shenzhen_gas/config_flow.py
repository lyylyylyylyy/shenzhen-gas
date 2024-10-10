"""Config flow for Shenzhen Gas integration."""
from __future__ import annotations
import random
from typing import Any
import base64
from homeassistant.helpers.aiohttp_client import async_get_clientsession
import aiohttp

import voluptuous as vol

from homeassistant import config_entries
from homeassistant.core import HomeAssistant
from homeassistant.data_entry_flow import FlowResult
from homeassistant.exceptions import HomeAssistantError

from .const import DOMAIN

STEP_USER_DATA_SCHEMA = vol.Schema({
    vol.Required("username"): str,
    vol.Required("password"): str,
    vol.Required("captcha"): str,
})

async def validate_input(hass: HomeAssistant, data: dict[str, Any]) -> dict[str, Any]:
    """Validate the user input allows us to connect."""
    # TODO: Implement validation logic here
    return {"title": f"Shenzhen Gas Account {data['username']}"}

class ConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for Shenzhen Gas."""

    VERSION = 1

    def __init__(self):
        self.captcha_url = None

    async def async_step_user(self, user_input: dict[str, Any] | None = None) -> FlowResult:
        """Handle the initial step."""
        errors: dict[str, str] = {}
        if user_input is not None:
            if user_input.get("refresh_captcha", False):
                # 用户点击了刷新验证码
                return await self.async_step_user()
            try:
                info = await validate_input(self.hass, user_input)
            except CannotConnect:
                errors["base"] = "cannot_connect"
            except InvalidAuth:
                errors["base"] = "invalid_auth"
            except Exception:  # pylint: disable=broad-except
                errors["base"] = "unknown"
            else:
                return self.async_create_entry(title=info["title"], data=user_input)

        if not self.captcha_url:
            self.captcha_url = f"https://service.szgas.com.cn/login/kaptcha-image.jspx?{random.randint(1, 1000)}"

        session = async_get_clientsession(self.hass)
        try:
            async with session.get(self.captcha_url) as response:
                if response.status == 200:
                    captcha_image = await response.read()
                    captcha_base64 = base64.b64encode(captcha_image).decode('utf-8')
                    captcha_html = f'<img src="data:image/jpeg;base64,{captcha_base64}" alt="验证码" />'
                else:
                    captcha_html = "无法加载验证码"
        except aiohttp.ClientError:
            captcha_html = "无法加载验证码"

        return self.async_show_form(
            step_id="user", 
            data_schema=vol.Schema({
                vol.Required("username"): str,
                vol.Required("password"): str,
                vol.Required("captcha"): str,
                vol.Optional("refresh_captcha", default=False): bool,
            }),
            errors=errors,
            description_placeholders={
                "captcha_image": captcha_html,
            },
        )

class CannotConnect(HomeAssistantError):
    """Error to indicate we cannot connect."""

class InvalidAuth(HomeAssistantError):
    """Error to indicate there is invalid auth."""
