import argparse
import asyncio
import os
import sys
from importlib.metadata import version as _metadata_version
from typing import Any, cast

import click
import rich
from pydantic_ai import _cli
from rich.console import Console
from rich.pretty import Pretty
from rich.table import Table
from rich.text import Text

from gh_pydantic_ai.auth import get_usage, is_authenticated, try_get_access_token
from gh_pydantic_ai.client import GHCopilotClient
from gh_pydantic_ai.consts import DEFAULT_MODEL


def cli() -> None:
    if not is_authenticated():
        rich.print(
            Text(
                "You need to authenticate with GitHub Copilot first. Run `gh-clai-internal auth` to authenticate.",
                style="yellow",
            ),
        )
        return

    parser = argparse.ArgumentParser(add_help=False)
    parser.add_argument("prompt", nargs="*")
    parser.add_argument("-m", "--model", default=None, type=str)
    parser.add_argument("-a", "--agent", default=None, type=str)
    parser.add_argument("-t", "--code-theme")
    parser.add_argument("--no-stream", action="store_true")
    parser.add_argument("-l", "--list-models", action="store_true")
    parser.add_argument("--version", action="store_true")

    args, _ = parser.parse_known_args()
    console = Console()

    if args.version:
        name_version = f"[green]gh - GH-Copilot Pydantic AI CLI v{_metadata_version('gh_pydantic_ai')}[/green]"
        console.print(name_version, highlight=False)
        return

    if args.list_models:
        _models = asyncio.run(_available_models())

        console.print("[green]Available models:[/green]")
        for model in _models:
            console.print(f"  {model['id']}", highlight=False)

        return

    model = args.model or os.getenv("GH_COPILOT_MODEL") or DEFAULT_MODEL

    new_args = []

    if not args.agent:
        new_args += [
            "--agent",
            f"gh_pydantic_ai.agent_cli:{model}",
        ]

    if args.code_theme:
        new_args += [
            "--code-theme",
            args.code_theme,
        ]

    if args.no_stream:
        new_args += [
            "--no-stream",
        ]

    if args.prompt:
        new_args += [" ".join(args.prompt)]

    sys.argv[1:] = new_args
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
        rich.print_json(data=_models_raw, indent=4)
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
