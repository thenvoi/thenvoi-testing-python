"""Tests for the fixtures module (pytest plugin)."""

from __future__ import annotations

import pytest

from thenvoi_testing.fakes import FakeAgentTools
from thenvoi_testing.factories import MockDataFactory


class TestFakeAgentToolsFixture:
    """Tests for the fake_agent_tools fixture."""

    def test_fixture_returns_fake_agent_tools(self, fake_agent_tools) -> None:
        """fake_agent_tools fixture should return FakeAgentTools instance."""
        assert isinstance(fake_agent_tools, FakeAgentTools)

    @pytest.mark.asyncio
    async def test_fixture_is_fresh_instance(self, fake_agent_tools) -> None:
        """Each test should get a fresh FakeAgentTools instance."""
        # Send a message
        await fake_agent_tools.send_message("Test message")
        assert len(fake_agent_tools.messages_sent) == 1

    @pytest.mark.asyncio
    async def test_fixture_isolation(self, fake_agent_tools) -> None:
        """New test should have empty tracking lists."""
        # This runs after the previous test - should be fresh
        assert len(fake_agent_tools.messages_sent) == 0


class TestMockWebsocketFixture:
    """Tests for the mock_websocket fixture."""

    @pytest.mark.asyncio
    async def test_fixture_is_async_context_manager(self, mock_websocket) -> None:
        """mock_websocket should work as async context manager."""
        async with mock_websocket as ws:
            assert ws is mock_websocket

    @pytest.mark.asyncio
    async def test_fixture_has_channel_methods(self, mock_websocket) -> None:
        """mock_websocket should have channel operation methods."""
        await mock_websocket.join_chat_room_channel("room-123")
        await mock_websocket.leave_chat_room_channel("room-123")
        await mock_websocket.join_agent_rooms_channel()

        mock_websocket.join_chat_room_channel.assert_called_once_with("room-123")
        mock_websocket.leave_chat_room_channel.assert_called_once_with("room-123")
        mock_websocket.join_agent_rooms_channel.assert_called_once()


class TestFactoryFixture:
    """Tests for the factory fixture."""

    def test_fixture_returns_mock_data_factory(self, factory) -> None:
        """factory fixture should return MockDataFactory instance."""
        assert isinstance(factory, MockDataFactory)

    def test_fixture_can_create_mocks(self, factory) -> None:
        """factory fixture should be able to create mock objects."""
        agent = factory.agent_me(id="test-123", name="TestBot")
        assert agent.id == "test-123"
        assert agent.name == "TestBot"

    def test_fixture_can_create_responses(self, factory) -> None:
        """factory fixture should be able to create response wrappers."""
        agent = factory.agent_me()
        response = factory.response(agent)
        assert response.data == agent
