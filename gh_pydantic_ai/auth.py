import asyncio
import time
import webbrowser
from collections.abc import AsyncGenerator, Generator
from contextlib import suppress
from dataclasses import dataclass
from pathlib import Path
from typing import cast

import pyperclip
import rich
from httpx import AsyncClient, Auth, Request, Response

from .consts import GITHUB_APP_SCOPES, GITHUB_CLIENT_ID
from .headers import copilot_headers, github_headers, standard_headers
from .types import DataStrAny

CONFIG_ROOT = Path.home() / ".config" / "gh-copilot-pydantic-ai"
TOKEN_FILE = CONFIG_ROOT / "access_token.txt"


async def get_device_code(client: AsyncClient) -> DataStrAny:
    response = await client.post(
        "/login/device/code",
        json={
            "client_id": GITHUB_CLIENT_ID,
            "scope": " ".join(GITHUB_APP_SCOPES),
        },
    )
    response.raise_for_status()

    return cast(DataStrAny, response.json())


async def wait_for_login(
    client: AsyncClient,
    device_code: str,
    interval: float,
) -> str:
    while True:
        response = await client.post(
            "/login/oauth/access_token",
            json={
                "client_id": GITHUB_CLIENT_ID,
                "device_code": device_code,
                "grant_type": "urn:ietf:params:oauth:grant-type:device_code",
            },
        )

        match response.json():
            case {"access_token": str(access_token)}:
                return access_token
            case _:
                rich.print("Not logged in yet, waiting for user to authenticate...")
                await asyncio.sleep(interval)


async def try_get_access_token(
    *,
    device_login_fallback: bool = False,
) -> str:
    CONFIG_ROOT.mkdir(parents=True, exist_ok=True)

    if TOKEN_FILE.exists():
        return TOKEN_FILE.read_text()

    if not device_login_fallback:
        raise ValueError("Login failed and no access token found.")

    async with AsyncClient(
        base_url="https://github.com",
        headers=standard_headers(),
    ) as client:
        device_code_info = await get_device_code(client)

        rich.print(
            f"Please open {device_code_info['verification_uri']} and enter the code: {device_code_info['user_code']}",
        )

        with suppress(Exception):
            pyperclip.copy(device_code_info["user_code"])
        with suppress(Exception):
            webbrowser.open_new_tab(device_code_info["verification_uri"])

        async with asyncio.timeout(device_code_info["expires_in"]):
            access_token = await wait_for_login(
                client,
                device_code_info["device_code"],
                interval=device_code_info["interval"],
            )

    TOKEN_FILE.write_text(access_token)
    return access_token


async def get_copilot_token() -> DataStrAny:
    async with AsyncClient(
        base_url="https://api.github.com/",
    ) as client:
        response = await client.get(
            "copilot_internal/v2/token",
            headers={
                **github_headers(),
                "Authorization": f"Bearer {await try_get_access_token()}",
            },
        )

        response.raise_for_status()
        return cast(DataStrAny, response.json())


async def get_usage() -> DataStrAny:
    async with AsyncClient(
        base_url="https://api.github.com/",
    ) as client:
        response = await client.get(
            "/copilot_internal/user",
            headers={
                **github_headers(),
                "Authorization": f"Bearer {await try_get_access_token()}",
            },
        )

        response.raise_for_status()
        return cast(DataStrAny, response.json())


def is_authenticated() -> bool:
    return bool(TOKEN_FILE.exists() and TOKEN_FILE.read_text().strip())


@dataclass
class GHCopilotAuth(Auth):
    _token: str | None = None
    _expires_at: float | None = None

    @property
    def is_expired(self) -> bool:
        if not self._token or not self._expires_at:
            return True

        return self._expires_at <= (time.time() + 60)  # 60 seconds buffer

    async def async_auth_flow(self, request: Request) -> AsyncGenerator[Request, Response]:
        if not self._token:
            data = await get_copilot_token()

            self._token = data["token"]
            self._expires_at = data["expires_at"]

        request.headers.update(copilot_headers())
        request.headers["Authorization"] = f"Bearer {self._token}"

        yield request

    def sync_auth_flow(self, request: Request) -> Generator[Request, Response]:
        raise NotImplementedError


__all__ = [
    "GHCopilotAuth",
    "get_usage",
    "is_authenticated",
    "try_get_access_token",
]
