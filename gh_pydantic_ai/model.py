from openai import AsyncOpenAI
from pydantic_ai.models.openai import OpenAIChatModel, OpenAISystemPromptRole
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
        system_prompt_role: OpenAISystemPromptRole | None = None,
    ) -> None:
        super().__init__(
            model_name=model_name or DEFAULT_MODEL,
            provider=provider or GHCopilotProvider(),
            profile=profile,
            system_prompt_role=system_prompt_role,
        )


__all__ = [
    "GHCopilotModel",
]
