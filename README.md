# gh-copilot-pydantic-ai

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![PyPI version](https://badge.fury.io/py/gh-pydantic-ai.svg)](https://badge.fury.io/py/gh-pydantic-ai)
[![Python Version](https://img.shields.io/pypi/pyversions/gh-pydantic-ai.svg)](https://pypi.org/project/gh-pydantic-ai)

GitHub Copilot Provider for Pydantic AI.

Inspired by [ericc-ch/copilot-api/](https://github.com/ericc-ch/copilot-api/).

## Installation

Install the package using pipx or your favorite package manager:

```bash
pip install gh-pydantic-ai
# or with uv
uv tool install gh-pydantic-ai
```

## CLI Usage

### Authentication

First, you need to authenticate with your GitHub account.

```bash
gh-clai-internal auth
```

### Query

After authentication, you can use the `gh-clai` command to interact with GitHub Copilot:

```bash
gh-clai "What is the capital of France?"
```

## Library Usage

This library also provides `GHCopilotModel` for integration with Pydantic AI.

```python
from gh_pydantic_ai import GHCopilotModel
from pydantic_ai import Agent

agent = Agent(
    model=GHCopilotModel()
)

result = agent.run_sync("What is the capital of France?")
print(result)
```

## Commands

- `gh-clai`: Main command to interact with GitHub Copilot, works same as `clai` command from `pydantic-ai`.
- `gh-clai-internal`: Internal commands for authentication and other utilities.
  - `auth`: Authenticate with GitHub.
  - `models`: List available models.
  - `usage`: Show usage information.

