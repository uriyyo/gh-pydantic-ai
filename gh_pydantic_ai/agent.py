from pydantic_ai import Agent

from .model import resolve_gh_model
from .types import GHCopilotModelName


def get_agent(model: GHCopilotModelName) -> Agent:
    return Agent(
        model=resolve_gh_model(model),
    )


__all__ = [
    "get_agent",
]
