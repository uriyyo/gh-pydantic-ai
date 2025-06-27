import uuid

from .consts import API_VERSION, EDITOR_PLUGIN_VERSION, USER_AGENT
from .types import Headers


def standard_headers() -> Headers:
    return {
        "accept": "application/json",
        "content-type": "application/json",
    }


def github_headers() -> Headers:
    return {
        **standard_headers(),
        "editor-version": "vscode/1.101.2",
        "editor-plugin-version": EDITOR_PLUGIN_VERSION,
        "user-agent": USER_AGENT,
        "x-github-api-version": API_VERSION,
        "x-vscode-user-agent-library-version": "electron-fetch",
    }


def copilot_headers() -> Headers:
    return {
        **standard_headers(),
        "copilot-integration-id": "vscode-chat",
        "editor-version": "vscode/1.101.2",
        "editor-plugin-version": EDITOR_PLUGIN_VERSION,
        "user-agent": USER_AGENT,
        "openai-intent": "conversation-panel",
        "x-github-api-version": API_VERSION,
        "x-request-id": str(uuid.uuid4()),
        "x-vscode-user-agent-library-version": "electron-fetch",
    }


__all__ = [
    "copilot_headers",
    "github_headers",
    "standard_headers",
]
