from pydantic_ai import Agent

from .model import GHCopilotModel
from .provider import GHCopilotProvider
from .types import GHCopilotModelName


def get_agent(model: GHCopilotModelName) -> Agent:
    return Agent(
        model=GHCopilotModel(
            model_name=model,
            provider=GHCopilotProvider(),
        ),
    )


__all__ = [
    "get_agent",
]
