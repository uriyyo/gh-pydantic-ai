import asyncio
import sys
from typing import Any, cast, get_args

import click
import rich
from pydantic_ai import _cli
from rich.pretty import Pretty
from rich.table import Table
from rich.text import Text

from gh_pydantic_ai.auth import get_usage, is_authenticated, try_get_access_token
from gh_pydantic_ai.client import GHCopilotClient
from gh_pydantic_ai.types import GHCopilotModelName


@click.command()
@click.argument(
    "prompt",
    nargs=-1,
    type=click.STRING,
)
@click.option(
    "--model",
    default="gpt-4.1",
    help="The model to use for GitHub Copilot.",
    envvar="GH_COPILOT_MODEL",
    type=click.Choice([*get_args(GHCopilotModelName.__value__)]),
)
def cli(
    prompt: str | None,
    model: str,
) -> None:
    if not is_authenticated():
        rich.print(
            Text(
                "You need to authenticate with GitHub Copilot first. Run `gh-clai-internal auth` to authenticate.",
                style="yellow",
            ),
        )
        return

    new_argv = []

    if prompt:
        new_argv.append(prompt)

    new_argv.extend(
        [
            "--agent",
            f"gh_pydantic_ai.agent_cli:{model}",
        ],
    )

    sys.argv[1:] = new_argv
    _cli.cli(prog_name="gh")


@click.group()
def internal_cli() -> None:
    pass


async def _available_models() -> list[dict[str, Any]]:
    async with GHCopilotClient(
        base_url="https://api.githubcopilot.com",
    ) as client:
        response = await client.get(
            "/models",
        )

        response.raise_for_status()
        return cast(list[dict[str, Any]], response.json()["data"])


@internal_cli.command()
@click.option("--raw", is_flag=True, help="Display raw model data.")
def models(
    *,
    raw: bool,
) -> None:
    if not is_authenticated():
        rich.print("You need to authenticate with GitHub Copilot first.")
        return

    _models_raw = asyncio.run(_available_models())

    if not _models_raw:
        rich.print("No models available.")
        return

    if raw:
        rich.print(_models_raw)
        return

    _models = [model["id"] for model in _models_raw]

    rich.print("Available models:")

    for model in _models:
        rich.print(f"- {model}")


@internal_cli.command()
def auth() -> None:
    if is_authenticated():
        rich.print(
            Text(
                "You are already authenticated with GitHub Copilot.",
                style="green",
            ),
        )
        return

    rich.print(
        Text(
            "You need to authenticate with GitHub Copilot.",
            style="yellow",
        ),
    )
    asyncio.run(try_get_access_token(device_login_fallback=True))


@internal_cli.command()
def usage() -> None:
    if not is_authenticated():
        rich.print("You need to authenticate with GitHub Copilot first.")
        return

    result = asyncio.run(get_usage())

    table = Table(
        "Quota ID",
        "Remaining",
        "Percent Remaining",
        "Quota Remaining",
        "Unlimited",
        title="GitHub Copilot Usage",
    )

    for value in result["quota_snapshots"].values():
        table.add_row(
            value["quota_id"],
            Pretty(value["remaining"]),
            Pretty(value["percent_remaining"]),
            Pretty(value["quota_remaining"]),
            Pretty(value["unlimited"]),
        )

    rich.print(table)


if __name__ == "__main__":
    cli()
