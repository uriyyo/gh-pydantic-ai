from datetime import UTC, datetime

from openai import AsyncOpenAI
from openai.types import chat
from pydantic_ai.messages import ModelResponse
from pydantic_ai.models.openai import OpenAIModel, OpenAISystemPromptRole
from pydantic_ai.profiles import ModelProfileSpec
from pydantic_ai.providers import Provider

from .provider import GHCopilotProvider
from .types import GHCopilotModelName


class GHCopilotModel(OpenAIModel):
    def __init__(
        self,
        model_name: GHCopilotModelName | None,
        *,
        provider: Provider[AsyncOpenAI] | None = None,
        profile: ModelProfileSpec | None = None,
        system_prompt_role: OpenAISystemPromptRole | None = None,
    ) -> None:
        super().__init__(
            model_name=model_name or "gpt-4.1",  # gpt-4.1 because it free and without usage limit
            provider=provider or GHCopilotProvider(),
            profile=profile,
            system_prompt_role=system_prompt_role,
        )

    def _process_response(self, response: chat.ChatCompletion | str) -> ModelResponse:
        # todo: verify that we need it
        if isinstance(response, chat.ChatCompletion):
            response.object = response.object or "chat.completion"
            response.created = response.created or int(datetime.now(UTC).timestamp())

        return super()._process_response(response)


__all__ = [
    "GHCopilotModel",
]
