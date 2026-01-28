"""Pytest fixtures for Thenvoi testing.

This module provides pytest fixtures that are automatically registered
when thenvoi-testing-python is installed (via pytest plugin entry point).

The fixtures provided are:
- fake_agent_tools: FakeAgentTools instance for testing adapters
- mock_websocket: AsyncMock WebSocket client for subscription tests
- factory: MockDataFactory instance for creating test data

Usage:
    # Just install the package and fixtures are available
    def test_my_adapter(fake_agent_tools):
        await adapter.on_message(msg, fake_agent_tools, ...)
        assert len(fake_agent_tools.messages_sent) == 1

    def test_data_factory(factory):
        agent = factory.agent_me(id="test-123")
        assert agent.id == "test-123"
"""

from __future__ import annotations

from unittest.mock import AsyncMock

import pytest

from thenvoi_testing.fakes import FakeAgentTools
from thenvoi_testing.factories import factory as _factory


@pytest.fixture
def fake_agent_tools() -> FakeAgentTools:
    """Provide a FakeAgentTools instance for adapter testing.

    Tracks all calls to send_message, send_event, add_participant, etc.
    allowing assertions on tool usage without mocking.

    Example:
        async def test_adapter_sends_message(fake_agent_tools):
            adapter = MyAdapter()
            await adapter.process(message, fake_agent_tools)

            assert len(fake_agent_tools.messages_sent) == 1
            assert fake_agent_tools.messages_sent[0]["content"] == "Hello!"
    """
    return FakeAgentTools()


@pytest.fixture
def mock_websocket() -> AsyncMock:
    """Provide a mock WebSocket client for subscription tests.

    The mock is configured as an async context manager with common
    channel operations pre-configured.

    Example:
        async def test_subscription(mock_websocket):
            async with mock_websocket:
                await mock_websocket.join_chat_room_channel("room-123")
            mock_websocket.join_chat_room_channel.assert_called_once()
    """
    ws = AsyncMock()

    # Make it work as async context manager
    ws.__aenter__ = AsyncMock(return_value=ws)
    ws.__aexit__ = AsyncMock(return_value=None)

    # Mock channel operations
    ws.join_chat_room_channel = AsyncMock()
    ws.leave_chat_room_channel = AsyncMock()
    ws.join_agent_rooms_channel = AsyncMock()

    return ws


@pytest.fixture
def factory():
    """Provide MockDataFactory for creating test objects.

    Example:
        def test_with_factory(factory):
            agent = factory.agent_me(id="test-agent", name="TestBot")
            message = factory.chat_message(content="Hello")
            response = factory.response(agent)
    """
    return _factory
