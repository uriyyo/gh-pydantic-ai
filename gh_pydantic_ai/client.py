from typing import TYPE_CHECKING, Any

from httpx import AsyncClient, Auth

from .auth import GHCopilotAuth


class GHCopilotClient(AsyncClient):
    if not TYPE_CHECKING:

        def __init__(self, **kwargs: Any) -> None:
            kwargs.setdefault("base_url", "https://api.githubcopilot.com")
            super().__init__(**kwargs)

    def _build_auth(self, auth: Any | None) -> Auth | None:
        if auth is None:
            return GHCopilotAuth()

        return super()._build_auth(auth)


__all__ = [
    "GHCopilotClient",
]
