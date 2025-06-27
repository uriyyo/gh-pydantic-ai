from pydantic_ai import Agent
from pydantic_ai._cli import cli_system_prompt

from gh_pydantic_ai.agent import get_agent


def __getattr__(model: str) -> Agent:
    agent = get_agent(model)
    agent.system_prompt(cli_system_prompt)

    return agent


__all__: list[str] = []
