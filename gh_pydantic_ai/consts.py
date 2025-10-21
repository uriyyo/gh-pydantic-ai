from .types import GHCopilotModelName

DEFAULT_MODEL = "gpt-5-mini"  # gpt-5-mini because it free and without usage limit

GITHUB_BASE_URL = "https://github.com"
GITHUB_CLIENT_ID = "Iv1.b507a08c87ecfe98"
GITHUB_APP_SCOPES = ["read:user"]

VSCODE_VERSION = "1.105.1"
COPILOT_VERSION = "0.32.3"
EDITOR_PLUGIN_VERSION = f"copilot-chat/${COPILOT_VERSION}"
USER_AGENT = f"GitHubCopilotChat/${COPILOT_VERSION}"
API_VERSION = "2025-04-01"

RESPONSES_API_MODELS: set[GHCopilotModelName] = {
    "gpt-5-codex",
}

__all__ = [
    "API_VERSION",
    "COPILOT_VERSION",
    "DEFAULT_MODEL",
    "EDITOR_PLUGIN_VERSION",
    "GITHUB_APP_SCOPES",
    "GITHUB_BASE_URL",
    "GITHUB_CLIENT_ID",
    "RESPONSES_API_MODELS",
    "USER_AGENT",
    "VSCODE_VERSION",
]
