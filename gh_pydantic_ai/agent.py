from pydantic_ai import Agent
from pydantic_ai.models.openai import OpenAIModel

from .provider import GitHubCopilotProvider


def get_agent(model: str) -> Agent:
    return Agent(
        model=OpenAIModel(
            model_name=model,
            provider=GitHubCopilotProvider(),
        ),
    )


__all__ = [
    "get_agent",
]
