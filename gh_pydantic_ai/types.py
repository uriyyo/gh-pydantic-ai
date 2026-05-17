from typing import Any, Literal

type Headers = dict[str, str]
type DataStrAny = dict[str, Any]

type GHCopilotModelName = Literal[
    # claude models
    "claude-opus-4.7",
    "claude-opus-4.5",
    "claude-sonnet-4.6",
    "claude-sonnet-4.5",
    "claude-haiku-4.5",
    # gemini models
    "gemini-3.1-pro-preview",
    "gemini-3-flash-preview",
    "gemini-2.5-pro",
    # gpt-5 models
    "gpt-5.5",
    "gpt-5.4",
    "gpt-5.4-mini",
    "gpt-5.3-codex",
    "gpt-5.2-codex",
    "gpt-5.2",
    "gpt-5-mini",
    # gpt-4o models
    "gpt-4o-2024-11-20",
    "gpt-4o-2024-08-06",
    "gpt-4o-2024-07-18",
    "gpt-4o-2024-05-13",
    "gpt-4-o-preview",
    "gpt-4o-mini-2024-07-18",
    "gpt-4o-mini",
    "gpt-4o",
    # gpt-4.1 models
    "gpt-4.1-2025-04-14",
    "gpt-4.1",
    # gpt-4 models
    "gpt-4-0613",
    "gpt-4-0125-preview",
    "gpt-4",
    # gpt-3.5 models
    "gpt-3.5-turbo-0613",
    "gpt-3.5-turbo",
    # other models
    "oswe-vscode-prime",
]

__all__ = [
    "DataStrAny",
    "GHCopilotModelName",
    "Headers",
]
