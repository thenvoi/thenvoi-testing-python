"""Pytest configuration for thenvoi-testing-python tests.

Note: The fixtures from thenvoi_testing.fixtures are automatically
registered via the pytest plugin entry point in pyproject.toml.
"""

from __future__ import annotations

import pytest


# Mark all tests as asyncio by default
def pytest_configure(config: pytest.Config) -> None:
    """Configure pytest markers."""
    config.addinivalue_line("markers", "asyncio: mark test as asyncio")
