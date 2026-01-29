from __future__ import annotations

from typing import Any
import logging
import aiohttp

_LOGGER = logging.getLogger(__name__)


class ManagementApiClient:
    """API client for ASKU Management Company service.

    ❗ Правила:
    - НЕ хранит токены
    - НЕ делает retry
    - НЕ знает про Home Assistant
    - Только HTTP + возврат данных
    """

    BASE_URL = "https://back.my.kommunal.uz/api"

    def __init__(self, session: aiohttp.ClientSession) -> None:
        self._session = session

    # ------------------------------------------------------------------
    # AUTH
    # ------------------------------------------------------------------

    async def login(self, login: str, password: str) -> dict[str, Any]:
        """Login and return raw token data."""
        url = f"{self.BASE_URL}/login"
        payload = {
            "login": login,
            "parol": password,
        }

        async with self._session.post(url, json=payload) as resp:
            resp.raise_for_status()
            data = await resp.json()

        if not data.get("status"):
            raise RuntimeError("Login failed")

        token_data = data.get("data") or {}

        return {
            "access_token": token_data.get("access_token"),
            "yandex_token": token_data.get("yandex_"),
        }

    # ------------------------------------------------------------------
    # MANAGEMENT DATA
    # ------------------------------------------------------------------

    async def get_dashboard(
        self,
        token: str,
        yandex_token: str,
        year: int,
    ) -> dict[str, Any]:
        url = f"{self.BASE_URL}/dashboard"
        headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json",
            "Accept": "application/json",
        }
        payload = {
            "data": yandex_token,
            "year": year,
        }

        async with self._session.post(
            url,
            json=payload,
            headers=headers,
        ) as resp:
            # ⚠️ endpoint иногда отдаёт text/html
            data = await resp.json(content_type=None)

        if not data.get("status"):
            raise RuntimeError("Dashboard request failed")

        return data.get("data") or {}

    async def get_accruals(
        self,
        token: str,
        yandex_token: str,
        year: str,
    ) -> dict[str, Any]:
        """Get accruals for specified year."""
        url = f"{self.BASE_URL}/nachisleniya"
        headers = {
            "Authorization": f"Bearer {token}",
        }
        payload = {
            "data": yandex_token,
            "year": year,
        }

        async with self._session.post(
            url,
            json=payload,
            headers=headers,
        ) as resp:
            resp.raise_for_status()
            data = await resp.json()

        if not data.get("status"):
            raise RuntimeError("Accruals request failed")

        return data.get("data") or {}

    # ------------------------------------------------------------------
    # GAS
    # ------------------------------------------------------------------

    async def get_gas_data(
        self,
        token: str,
        yandex_token: str,
    ) -> dict[str, Any]:
        url = f"{self.BASE_URL}/gaz"
        headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json",
            "Accept": "application/json",
        }
        payload = {
            "data": yandex_token,
        }

        async with self._session.post(
            url,
            json=payload,
            headers=headers,
        ) as resp:
            data = await resp.json()

        if not data.get("status"):
            raise RuntimeError("Gas request failed")

        return data.get("data") or {}
