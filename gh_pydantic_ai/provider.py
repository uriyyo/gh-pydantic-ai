from openai import AsyncOpenAI
from pydantic_ai.providers import Provider

from .client import GHCopilotClient


class GHCopilotProvider(Provider[AsyncOpenAI]):
    @property
    def name(self) -> str:
        return "gh-copilot"

    @property
    def base_url(self) -> str:
        return "https://api.githubcopilot.com"

    @property
    def client(self) -> AsyncOpenAI:
        return self._client

    def __init__(self) -> None:
        self._client = AsyncOpenAI(
            api_key="",
            base_url=self.base_url,
            http_client=GHCopilotClient(),
        )


__all__ = [
    "GHCopilotProvider",
]
