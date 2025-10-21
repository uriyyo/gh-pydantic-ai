from openai import AsyncOpenAI
from openai.types import chat
from pydantic_ai import ModelResponse, ModelSettings
from pydantic_ai.models.openai import OpenAIChatModel
from pydantic_ai.profiles import ModelProfileSpec
from pydantic_ai.providers import Provider

from .consts import DEFAULT_MODEL
from .provider import GHCopilotProvider
from .types import GHCopilotModelName


class GHCopilotModel(OpenAIChatModel):
    def __init__(
        self,
        model_name: GHCopilotModelName | None,
        *,
        provider: Provider[AsyncOpenAI] | None = None,
        profile: ModelProfileSpec | None = None,
        settings: ModelSettings | None = None,
    ) -> None:
        super().__init__(
            model_name=model_name or DEFAULT_MODEL,
            provider=provider or GHCopilotProvider(),
            profile=profile,
            settings=settings,
        )

    def _process_response(self, response: chat.ChatCompletion | str) -> ModelResponse:
        if isinstance(response, chat.ChatCompletion):
            response.object = response.object or "chat.completion"

        return super()._process_response(response)


__all__ = [
    "GHCopilotModel",
]
