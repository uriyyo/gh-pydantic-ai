import asyncio
import sys

import click
import rich
from pydantic_ai import _cli
from rich.pretty import Pretty
from rich.table import Table
from rich.text import Text

from gh_pydantic_ai.auth import get_usage, is_authenticated, try_get_access_token
from gh_pydantic_ai.client import GHCopilotClient


@click.group(invoke_without_command=True)
@click.option(
    "-q",
    "--prompt",
    required=False,
)
@click.option(
    "--model",
    default="gpt-4.1",
    help="The model to use for GitHub Copilot.",
    envvar="GH_COPILOT_MODEL",
)
@click.pass_context
def cli(
    ctx: click.Context,
    prompt: str | None,
    model: str,
) -> None:
    if ctx.invoked_subcommand is not None:
        return

    new_argv = []

    if prompt:
        new_argv.append(prompt)

    new_argv.extend(
        [
            "--agent",
            f"gh_pydantic_ai.agent:{model}",
        ],
    )

    sys.argv[1:] = new_argv
    _cli.cli(prog_name="gh")


@cli.group()
def internal() -> None:
    pass


async def _available_models() -> list[str]:
    async with GHCopilotClient(
        base_url="https://api.githubcopilot.com",
    ) as client:
        response = await client.get(
            "/models",
        )

        response.raise_for_status()
        return [model["id"] for model in response.json().get("data", [])]


@internal.command()
def models() -> None:
    if not is_authenticated():
        rich.print("You need to authenticate with GitHub Copilot first.")
        return

    _models = asyncio.run(_available_models())
    if not _models:
        rich.print("No models available.")
        return

    rich.print("Available models:")

    for model in _models:
        rich.print(f"- {model}")


@internal.command()
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


@internal.command()
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
