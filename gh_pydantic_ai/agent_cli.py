from typing import cast

from pydantic_ai import Agent
from pydantic_ai._cli import cli_system_prompt

from .agent import get_agent
from .types import GHCopilotModelName


def __getattr__(model: str) -> Agent:
    agent = get_agent(cast(GHCopilotModelName, model))
    agent.system_prompt(cli_system_prompt)

    return agent


__all__: list[str] = []
