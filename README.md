# thenvoi-testing-python

Shared Python testing utilities for Thenvoi repositories. Provides fixtures, factories, and fakes for testing adapters, WebSocket clients, and API integrations.

## Installation

Install from GitHub using uv:

```bash
# Core package
uv add "thenvoi-testing-python @ git+https://github.com/thenvoi/thenvoi-testing-python.git"

# With WebSocket testing support
uv add "thenvoi-testing-python[websocket] @ git+https://github.com/thenvoi/thenvoi-testing-python.git"

# With REST client testing support
uv add "thenvoi-testing-python[rest] @ git+https://github.com/thenvoi/thenvoi-testing-python.git"

# Full installation
uv add "thenvoi-testing-python[full] @ git+https://github.com/thenvoi/thenvoi-testing-python.git"
```

## Quick Start

The package automatically registers pytest fixtures when installed. Just use them in your tests:

```python
# Tests automatically have access to fixtures
async def test_adapter_sends_message(fake_agent_tools):
    adapter = MyAdapter()
    await adapter.process(message, fake_agent_tools)

    assert len(fake_agent_tools.messages_sent) == 1
    assert fake_agent_tools.messages_sent[0]["content"] == "Hello!"

def test_with_factory(factory):
    agent = factory.agent_me(id="test-123", name="TestBot")
    response = factory.response(agent)
    assert response.data.id == "test-123"
```

## Components

### Factories

Mock data factories for creating test objects that behave like Pydantic models:

```python
from thenvoi_testing.factories import factory

# Create mock objects with OpenAPI example defaults
agent = factory.agent_me()
agent = factory.agent_me(id="custom-id", name="CustomBot")

# Create response wrappers
response = factory.response(agent)
list_response = factory.list_response([room1, room2])

# Available factory methods:
# - agent_me()        - AgentMe object
# - peer()            - Peer object
# - chat_room()       - ChatRoom object
# - chat_participant() - ChatParticipant object
# - chat_message()    - ChatMessage object
# - chat_event()      - ChatEvent object
# - user_profile()    - UserProfile object
# - owned_agent()     - OwnedAgent object
# - registered_agent() - RegisteredAgent (with credentials)
# - deleted_agent()   - DeletedAgent object
```

### Fakes

Fake implementations for testing without mocking frameworks:

```python
from thenvoi_testing.fakes import FakeAgentTools

# FakeAgentTools tracks all tool calls
tools = FakeAgentTools()
await tools.send_message("Hello!")
await tools.send_event("Processing", "thought")
await tools.add_participant("Alice")

# Assert on tracked calls
assert len(tools.messages_sent) == 1
assert tools.messages_sent[0]["content"] == "Hello!"
assert len(tools.events_sent) == 1
assert len(tools.participants_added) == 1
```

For WebSocket testing (requires `websocket` extra):

```python
from thenvoi_testing.fakes import FakePhoenixServer

@pytest_asyncio.fixture
async def phoenix_server():
    server = FakePhoenixServer()
    await server.start()
    try:
        yield server
    finally:
        await server.stop()

async def test_websocket(phoenix_server):
    async with PHXChannelsClient(phoenix_server.url) as client:
        await client.subscribe_to_topic("test-topic", callback)
        await phoenix_server.simulate_server_event(
            "test-topic", "new_message", {"text": "hello"}
        )
```

### Markers

Skip markers for conditional test execution:

```python
from thenvoi_testing.markers import (
    skip_without_env,
    skip_without_envs,
    skip_with_condition,
    skip_in_ci,
    pytest_ignore_collect_in_ci,
)

# Skip if environment variable not set
requires_api = skip_without_env("THENVOI_API_KEY")

@requires_api
def test_api_call():
    ...

# Skip if any of multiple env vars not set
requires_multi_agent = skip_without_envs(
    ["THENVOI_API_KEY", "THENVOI_API_KEY_2"],
    reason="Both API keys required"
)

# Skip in CI environment
@skip_in_ci
def test_local_only():
    ...

# In conftest.py - skip integration folder in CI
def pytest_ignore_collect(collection_path):
    return pytest_ignore_collect_in_ci(str(collection_path), "integration")
```

### Settings

Base settings class for integration tests using Pydantic Settings:

```python
from pathlib import Path
from thenvoi_testing.settings import ThenvoiTestSettings

class TestSettings(ThenvoiTestSettings):
    _env_file_path = Path(__file__).parent / ".env.test"

settings = TestSettings()

# Check if credentials are available
if settings.has_api_key:
    client = create_client(settings.thenvoi_api_key)

if settings.has_multi_agent:
    # Both agents available for multi-agent tests
    pass
```

Example `.env.test`:
```
THENVOI_API_KEY=your-agent-api-key
TEST_AGENT_ID=your-agent-uuid
THENVOI_API_KEY_2=second-agent-key
TEST_AGENT_ID_2=second-agent-uuid
THENVOI_API_KEY_USER=user-api-key
THENVOI_BASE_URL=https://api.thenvoi.com
THENVOI_WS_URL=wss://api.thenvoi.com/api/v1/socket/websocket
```

## Pytest Plugin

The package registers as a pytest plugin automatically. Available fixtures:

| Fixture | Description |
|---------|-------------|
| `fake_agent_tools` | Fresh `FakeAgentTools` instance |
| `mock_websocket` | AsyncMock WebSocket client |
| `factory` | `MockDataFactory` instance |

## Development

```bash
# Clone the repository
git clone git@github.com:thenvoi/thenvoi-testing-python.git
cd thenvoi-testing-python

# Install with dev dependencies
uv sync --extra dev

# Run tests
uv run pytest tests/ -v

# Run linting
uv run ruff check .
uv run ruff format .
```

## Branching & Releases

This repository uses a **main-only** branch strategy:

- **Branch**: `main` (no `dev` branch)
- **Versioning**: Git tags (e.g., `v0.1.0`, `v0.2.0`)
- **Workflow**: Feature branch → PR → squash merge to `main` → tag release

To pin to a specific version:

```bash
uv add "thenvoi-testing-python @ git+https://github.com/thenvoi/thenvoi-testing-python.git@v0.1.0"
```

## License

MIT
