from __future__ import annotations

import asyncio
from typing import Any

import aiohttp


class ApiError(Exception):
    """Base API error."""


class AuthError(ApiError):
    """Authentication failed."""


class BaseApiClient:
    def __init__(
        self,
        base_url: str,
        timeout: int = 30,
    ) -> None:
        self._base_url = base_url.rstrip("/")
        self._timeout = aiohttp.ClientTimeout(total=timeout)
        self._session: aiohttp.ClientSession | None = None

    async def _get_session(self) -> aiohttp.ClientSession:
        if self._session is None or self._session.closed:
            self._session = aiohttp.ClientSession(timeout=self._timeout)
        return self._session

    async def _request(
        self,
        method: str,
        path: str,
        *,
        headers: dict[str, str] | None = None,
        json: dict[str, Any] | None = None,
        params: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        session = await self._get_session()
        url = f"{self._base_url}{path}"

        try:
            async with session.request(
                method=method,
                url=url,
                headers=headers,
                json=json,
                params=params,
            ) as response:
                if response.status == 401:
                    raise AuthError("Unauthorized")

                if response.status >= 400:
                    text = await response.text()
                    raise ApiError(
                        f"API error {response.status}: {text}"
                    )

                return await response.json()

        except asyncio.TimeoutError as exc:
            raise ApiError("Request timeout") from exc

        except aiohttp.ClientError as exc:
            raise ApiError("HTTP client error") from exc
