from typing import Any, Literal

type Headers = dict[str, str]
type DataStrAny = dict[str, Any]

type GHCopilotModelName = Literal[
    "claude-3.5-sonnet",
    "claude-3.7-sonnet",
    "claude-3.7-sonnet-thought",
    "claude-haiku-4.5",
    "claude-sonnet-4",
    "claude-sonnet-4.5",
    "gemini-2.0-flash-001",
    "gemini-2.5-pro",
    "gpt-3.5-turbo",
    "gpt-3.5-turbo-0613",
    "gpt-4",
    "gpt-4-0125-preview",
    "gpt-4-0613",
    "gpt-4-o-preview",
    "gpt-4.1",
    "gpt-4.1-2025-04-14",
    "gpt-4o",
    "gpt-4o-2024-05-13",
    "gpt-4o-2024-08-06",
    "gpt-4o-2024-11-20",
    "gpt-4o-mini",
    "gpt-4o-mini-2024-07-18",
    "gpt-5",
    "gpt-5-codex",
    "gpt-5-mini",
    "grok-code-fast-1",
    "o3-mini",
    "o3-mini-2025-01-31",
    "o3-mini-paygo",
    "o4-mini",
    "o4-mini-2025-04-16",
    "oswe-vscode-prime",
]

__all__ = [
    "DataStrAny",
    "GHCopilotModelName",
    "Headers",
]
