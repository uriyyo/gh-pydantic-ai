from pydantic_ai import Agent
from pydantic_ai.models.openai import OpenAIModel

from gh_pydantic_ai.provider import GitHubCopilotProvider


def __getattr__(model: str) -> Agent:
    return Agent(
        model=OpenAIModel(
            model_name=model,
            provider=GitHubCopilotProvider(),
        ),
    )


__all__: list[str] = []
