# Thenvoi Testing Python

Shared Python testing utilities for Thenvoi repositories. Provides fixtures, factories, and fakes for testing adapters, WebSocket clients, and API integrations.

## Code Structure

```
src/thenvoi_testing/
├── factories/      # Mock data factories (MockDataFactory, events)
├── fakes/          # Fake implementations (FakeAgentTools, FakePhoenixServer)
├── fixtures/       # Pytest plugin with auto-registered fixtures
├── streaming/      # WebSocket payload types (MessageCreatedPayload, etc.)
├── markers.py      # Skip marker utilities (skip_without_env, skip_in_ci)
├── pagination.py   # Pagination helpers for integration tests
└── settings.py     # Pydantic BaseSettings for integration tests
```

## Testing Structure

```
tests/
├── test_events.py      # Event factory tests
├── test_factories.py   # MockDataFactory tests
├── test_fakes.py       # FakeAgentTools tests
├── test_fixtures.py    # Pytest plugin tests
├── test_markers.py     # Skip marker tests
├── test_pagination.py  # Pagination helper tests
├── test_settings.py    # Settings tests
└── conftest.py         # Test configuration
```

## Commands

```bash
# Install dependencies
uv sync --extra dev

# Run tests
uv run pytest tests/ -v

# Run single test
uv run pytest tests/ -k "test_name"

# Run with coverage
uv run pytest tests/ --cov=src/thenvoi_testing

# Linting and formatting
uv run ruff check .
uv run ruff format .
```

## Installation (for consumers)

```bash
# From PyPI
uv add thenvoi-testing-python

# With specific extras
uv add "thenvoi-testing-python[websocket]"

# Pin to version
uv add "thenvoi-testing-python==0.1.1"
```

## Branching & Releases

- **Branch**: `main` only (no `dev` branch)
- **Versioning**: Managed by release-please via conventional commits
- **Publishing**: Automated PyPI publish via trusted publisher (OIDC)
- **Workflow**: Feature branch → PR (conventional commit title) → squash merge to `main` → release-please PR → merge → PyPI publish
