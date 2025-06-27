from typing import Any, Literal

type Headers = dict[str, str]
type DataStrAny = dict[str, Any]

type GHCopilotModelName = Literal[
    "gpt-3.5-turbo",
    "gpt-3.5-turbo-0613",
    "gpt-4o-mini",
    "gpt-4o-mini-2024-07-18",
    "gpt-4",
    "gpt-4-0613",
    "gpt-4-0125-preview",
    "gpt-4.1",
    "gpt-4o",
    "gpt-4o-2024-11-20",
    "gpt-4o-2024-05-13",
    "gpt-4-o-preview",
    "gpt-4o-2024-08-06",
    "o1",
    "o1-2024-12-17",
    "o3-mini",
    "o3-mini-2025-01-31",
    "o3-mini-paygo",
    "gpt-4o-copilot",
    "text-embedding-ada-002",
    "text-embedding-3-small",
    "text-embedding-3-small-inference",
    "claude-3.5-sonnet",
    "claude-3.7-sonnet",
    "claude-3.7-sonnet-thought",
    "claude-sonnet-4",
    "gemini-2.0-flash-001",
    "gemini-2.5-pro-preview-06-05",
    "gemini-2.5-pro",
    "o4-mini",
    "o4-mini-2025-04-16",
    "gpt-4.1-2025-04-14",
]

__all__ = [
    "DataStrAny",
    "GHCopilotModelName",
    "Headers",
]
