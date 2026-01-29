"""Shared Python testing utilities for Thenvoi repositories.

This package provides:
- factories: Mock data factories for creating test objects
- factories.events: Event factory helpers (make_message_event, etc.)
- fixtures: Pytest fixtures (mock_api_client, sample_room_message, etc.)
- fakes: Fake implementations (FakeAgentTools, FakePhoenixServer)
- markers: Pytest skip markers (requires_api, requires_multi_agent, etc.)
- pagination: Helpers for paginated API responses in integration tests
- streaming: WebSocket payload types (MessageCreatedPayload, etc.)

Usage:
    # In your conftest.py (fixtures auto-registered via pytest plugin)
    pytest_plugins = ["thenvoi_testing.fixtures"]

    # In your tests
    from thenvoi_testing.factories import factory
    from thenvoi_testing.factories.events import make_message_event
    from thenvoi_testing.fakes import FakeAgentTools
    from thenvoi_testing.markers import requires_api
    from thenvoi_testing.pagination import fetch_all_pages, find_item_in_pages
    from thenvoi_testing.streaming import MessageCreatedPayload
"""

from __future__ import annotations

from thenvoi_testing.pagination import (
    fetch_all_pages,
    find_item_in_pages,
    item_exists_in_pages,
)

__version__ = "0.1.0"

__all__ = [
    "fetch_all_pages",
    "find_item_in_pages",
    "item_exists_in_pages",
]
