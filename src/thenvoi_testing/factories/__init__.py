"""Mock data factories for unit tests.

This module provides factory functions to create mock SDK response objects
for testing without a real API server.

Usage:
    from thenvoi_testing.factories import factory

    agent = factory.agent_me(id="agent-123", name="TestBot")
    room = factory.chat_room(id="room-456")
    response = factory.response(agent)
"""

from __future__ import annotations

from thenvoi_testing.factories.base import (
    make_pydantic_mock,
    make_timestamp,
    make_uuid,
)
from thenvoi_testing.factories.models import MockDataFactory, factory

__all__ = [
    "MockDataFactory",
    "factory",
    "make_pydantic_mock",
    "make_timestamp",
    "make_uuid",
]
