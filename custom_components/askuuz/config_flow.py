from __future__ import annotations

import voluptuous as vol

from homeassistant import config_entries
from homeassistant.helpers.selector import SelectSelector, SelectSelectorConfig
from homeassistant.helpers import config_validation as cv
from homeassistant.helpers.aiohttp_client import async_get_clientsession

from .const import DOMAIN
from .api.electricity import ElectricityApiClient
from .api.water import WaterApiClient
from .api.tbo import TboApiClient
from .api.management import ManagementApiClient
from .api.base import AuthError, ApiError


class ASKUUZConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    VERSION = 1

    def __init__(self) -> None:
        self._service: str | None = None
        self._data: dict = {}

    async def _validate_credentials(self, username: str, password: str, service: str) -> bool:
        """Validate credentials by attempting to login."""
        try:
            session = async_get_clientsession(self.hass)
            
            # Create appropriate API client based on service type
            if service == "electricity":
                api = ElectricityApiClient(session=session)
                response = await api._request(
                    method="POST",
                    path="/user-login",
                    json={
                        "login": username,
                        "password": password,
                    },
                    headers={
                        "Accept": "application/json, text/plain, */*",
                        "Content-Type": "application/json",
                    },
                )
                # Check if token exists in response
                return "data" in response and "accessToken" in response.get("data", {})
            
            elif service == "water":
                api = WaterApiClient(session=session)
                token = await api.login(pid=username, pin=password)
                return token is not None and isinstance(token, str) and len(token) > 0
            
            elif service == "tbo":
                api = TboApiClient(session=session)
                token = await api.login(pid=username, pin=password)
                return token is not None and isinstance(token, str) and len(token) > 0
            
            elif service == "management":
                api = ManagementApiClient(session=session)
                result = await api.login(username, password)
                return "access_token" in result and "yandex_token" in result
        
        except AuthError:
            return False
        except ApiError:
            return False
        except Exception:
            return False

    async def async_step_user(self, user_input=None):
        errors = {}

        if user_input is None:
            return self.async_show_form(
                step_id="user",
                data_schema=vol.Schema(
                    {
                        vol.Required("service"): SelectSelector(
                            SelectSelectorConfig(
                                options=["electricity", "water", "tbo", "management"],
                                mode="dropdown",
                                translation_key="service",
                            )
                        )
                    }
                ),
                errors=errors,
            )

        self._service = user_input["service"]
        return await self.async_step_credentials()

    async def async_step_credentials(self, user_input=None):
        errors = {}

        if user_input is None:
            schema = {
                vol.Required("username"): str,
                vol.Required("password"): str,
                vol.Required("account_id"): str,
            }

            if self._service == "management":
                schema[vol.Optional("enable_gas", default=False)] = cv.boolean

            return self.async_show_form(
                step_id="credentials",
                data_schema=vol.Schema(schema),
                errors=errors,
            )

        # Basic validation
        if not user_input["username"] or not user_input["password"]:
            errors["base"] = "invalid_auth"
            schema = {
                vol.Required("username"): str,
                vol.Required("password"): str,
                vol.Required("account_id"): str,
            }

            if self._service == "management":
                schema[vol.Optional("enable_gas", default=False)] = cv.boolean

            return self.async_show_form(
                step_id="credentials",
                data_schema=vol.Schema(schema),
                errors=errors,
            )

        # Validate credentials by attempting to login
        if not await self._validate_credentials(
            user_input["username"],
            user_input["password"],
            self._service
        ):
            errors["base"] = "invalid_auth"
            schema = {
                vol.Required("username", description={"suggested_value": user_input["username"]}): str,
                vol.Required("password"): str,
                vol.Required("account_id", description={"suggested_value": user_input["account_id"]}): str,
            }

            if self._service == "management":
                schema[vol.Optional("enable_gas", default=user_input.get("enable_gas", False))] = cv.boolean

            return self.async_show_form(
                step_id="credentials",
                data_schema=vol.Schema(schema),
                errors=errors,
            )

        self._data = {
            "service": self._service,
            "username": user_input["username"],
            "password": user_input["password"],
            "account_id": user_input["account_id"],
        }

        # Check if configuration with same service, username, and account_id already exists
        for entry in self.hass.config_entries.async_entries(DOMAIN):
            if (
                entry.data.get("service") == self._service
                and entry.data.get("username") == user_input["username"]
                and entry.data.get("account_id") == user_input["account_id"]
            ):
                errors["base"] = "already_configured"
                schema = {
                    vol.Required("username", description={"suggested_value": user_input["username"]}): str,
                    vol.Required("password"): str,
                    vol.Required("account_id", description={"suggested_value": user_input["account_id"]}): str,
                }

                if self._service == "management":
                    schema[vol.Optional("enable_gas", default=user_input.get("enable_gas", False))] = cv.boolean

                return self.async_show_form(
                    step_id="credentials",
                    data_schema=vol.Schema(schema),
                    errors=errors,
                )

        if self._service != "management" or not user_input.get("enable_gas"):
            return self._create_entry(self._data)

        self._data["enable_gas"] = True
        return await self.async_step_gas()

    async def async_step_gas(self, user_input=None):
        errors = {}

        if user_input is None:
            return self.async_show_form(
                step_id="gas",
                data_schema=vol.Schema(
                    {
                        vol.Required("gas_account_id"): str,
                    }
                ),
                errors=errors,
            )

        if not user_input.get("gas_account_id"):
            errors["base"] = "invalid_gas_account"
            return self.async_show_form(
                step_id="gas",
                data_schema=vol.Schema(
                    {
                        vol.Required("gas_account_id"): str,
                    }
                ),
                errors=errors,
            )

        self._data["gas_account_id"] = user_input["gas_account_id"]
        return self._create_entry(self._data)

    def _create_entry(self, data: dict):
        return self.async_create_entry(
            title=f"ASKU {data['service'].capitalize()} {data['account_id']}",
            data=data,
        )
