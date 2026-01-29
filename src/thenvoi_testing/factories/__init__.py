"""Mock data factories for unit tests.

This module provides factory functions to create mock SDK response objects
for testing without a real API server.

Usage:
    from thenvoi_testing.factories import factory

    agent = factory.agent_me(id="agent-123", name="TestBot")
    room = factory.chat_room(id="room-456")
    response = factory.response(agent)

Event factories (require thenvoi-testing-python[rest]):
    from thenvoi_testing.factories.events import (
        make_message_event,
        make_room_added_event,
    )

    event = make_message_event(room_id="room-1", content="Hello!")
"""

from __future__ import annotations

from thenvoi_testing.factories.base import (
    make_pydantic_mock,
    make_timestamp,
    make_uuid,
)
from thenvoi_testing.factories.models import MockDataFactory, factory

# Event factories and types are imported lazily since they require the rest extra.
# Import them directly from thenvoi_testing.factories.events when needed.

__all__ = [
    "MockDataFactory",
    "factory",
    "make_pydantic_mock",
    "make_timestamp",
    "make_uuid",
]
