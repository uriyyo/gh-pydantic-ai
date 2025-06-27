# gh-copilot-pydantic-ai

GitHub Copilot integration with Pydantic AI.

Inspired by [ericc-ch/copilot-api/](https://github.com/ericc-ch/copilot-api/).

# Usage

1. Install the package:
```bash
uvx tool install gh-pydantic-ai
```

2. Authenticate with GitHub:
```bash
gh-clai-internal auth
```

3. Use the tool in your terminal:
```bash
gh-clai "What is the capital of France?"
```

# pydantic-ai

Library also provides Provider and Model classes to use together with Pydantic AI.

```python
from gh_pydantic_ai import GHCopilotModel
from pydantic_ai import Agent

agent = Agent(
    model=GHCopilotModel(
        model_name="gpt-4.1",
    ),
)
```
