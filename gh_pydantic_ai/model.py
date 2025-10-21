from warnings import deprecated

from openai import AsyncOpenAI
from openai.types import chat
from pydantic_ai import ModelResponse, ModelSettings
from pydantic_ai.models.openai import OpenAIChatModel, OpenAIResponsesModel
from pydantic_ai.profiles import ModelProfileSpec
from pydantic_ai.providers import Provider

from .consts import DEFAULT_MODEL, RESPONSES_API_MODELS
from .provider import GHCopilotProvider
from .types import GHCopilotModelName


class GHCopilotChatModel(OpenAIChatModel):
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


@deprecated(
    "GHCopilotModel is deprecated and will be removed in a future release. "
    "Please use GHCopilotChatModel or GHCopilotResponsesModel instead.",
)
class GHCopilotModel(GHCopilotChatModel):
    pass


class GHCopilotResponsesModel(OpenAIResponsesModel):
    def __init__(
        self,
        model_name: GHCopilotModelName,
        *,
        provider: Provider[AsyncOpenAI] | None = None,
        profile: ModelProfileSpec | None = None,
        settings: ModelSettings | None = None,
    ) -> None:
        super().__init__(
            model_name=model_name,
            provider=provider or GHCopilotProvider(),
            profile=profile,
            settings=settings,
        )


def resolve_gh_model(
    model_name: GHCopilotModelName | None,
    *,
    provider: Provider[AsyncOpenAI] | None = None,
    profile: ModelProfileSpec | None = None,
    settings: ModelSettings | None = None,
) -> GHCopilotChatModel | GHCopilotResponsesModel:
    model_name = model_name or DEFAULT_MODEL

    if model_name in RESPONSES_API_MODELS:
        return GHCopilotResponsesModel(
            model_name=model_name,
            provider=provider,
            profile=profile,
            settings=settings,
        )

    return GHCopilotChatModel(
        model_name=model_name,
        provider=provider,
        profile=profile,
        settings=settings,
    )


__all__ = [
    "GHCopilotChatModel",
    "GHCopilotModel",
    "GHCopilotResponsesModel",
    "resolve_gh_model",
]
