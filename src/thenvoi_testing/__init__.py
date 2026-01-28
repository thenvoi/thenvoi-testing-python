"""Shared Python testing utilities for Thenvoi repositories.

This package provides:
- factories: Mock data factories for creating test objects
- fixtures: Pytest fixtures for unit and integration tests
- fakes: Fake implementations (FakeAgentTools, FakePhoenixServer)
- markers: Pytest skip markers (requires_api, requires_multi_agent, etc.)
- helpers: Utility functions for common test patterns

Usage:
    # In your conftest.py
    pytest_plugins = ["thenvoi_testing.fixtures"]

    # In your tests
    from thenvoi_testing.factories import factory
    from thenvoi_testing.fakes import FakeAgentTools
    from thenvoi_testing.markers import requires_api
"""

from __future__ import annotations

__version__ = "0.1.0"
