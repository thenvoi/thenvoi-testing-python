"""Tests for the fixtures module (pytest plugin)."""

from __future__ import annotations

from unittest.mock import AsyncMock, MagicMock

import pytest

from thenvoi_testing.factories import MockDataFactory
from thenvoi_testing.fakes import FakeAgentTools
from thenvoi_testing.streaming import MessageCreatedPayload


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


class TestMockAgentApiFixture:
    """Tests for the mock_agent_api fixture."""

    def test_fixture_returns_magic_mock(self, mock_agent_api) -> None:
        """mock_agent_api fixture should return a MagicMock."""
        assert isinstance(mock_agent_api, MagicMock)

    def test_has_preconfigured_methods(self, mock_agent_api) -> None:
        """mock_agent_api should have pre-configured method return values."""
        # get_agent_me should return a response with agent data
        response = mock_agent_api.get_agent_me.return_value
        assert response.data.id == "agent-123"
        assert response.data.name == "TestBot"

    def test_list_agent_chats_returns_rooms(self, mock_agent_api) -> None:
        """list_agent_chats should return list of chat rooms."""
        response = mock_agent_api.list_agent_chats.return_value
        assert len(response.data) == 2
        assert response.data[0].id == "room-1"
        assert response.data[1].id == "room-2"

    def test_can_override_return_values(self, mock_agent_api, factory) -> None:
        """Tests should be able to override default return values."""
        mock_agent_api.get_agent_me.return_value = factory.response(
            factory.agent_me(id="custom-agent", name="CustomBot")
        )
        response = mock_agent_api.get_agent_me.return_value
        assert response.data.id == "custom-agent"
        assert response.data.name == "CustomBot"


class TestMockHumanApiFixture:
    """Tests for the mock_human_api fixture."""

    def test_fixture_returns_magic_mock(self, mock_human_api) -> None:
        """mock_human_api fixture should return a MagicMock."""
        assert isinstance(mock_human_api, MagicMock)

    def test_has_profile_method(self, mock_human_api) -> None:
        """mock_human_api should have get_my_profile configured."""
        response = mock_human_api.get_my_profile.return_value
        assert response.data.name == "Test User"

    def test_has_agents_methods(self, mock_human_api) -> None:
        """mock_human_api should have agent-related methods configured."""
        # list_my_agents
        response = mock_human_api.list_my_agents.return_value
        assert len(response.data) == 1

        # register_my_agent
        response = mock_human_api.register_my_agent.return_value
        assert response.data.credentials.api_key is not None

    def test_has_chat_methods(self, mock_human_api) -> None:
        """mock_human_api should have chat-related methods configured."""
        response = mock_human_api.list_my_chats.return_value
        assert len(response.data) == 1
        assert response.data[0].id == "room-1"


class TestMockApiClientFixture:
    """Tests for the mock_api_client fixture."""

    def test_fixture_returns_async_mock(self, mock_api_client) -> None:
        """mock_api_client fixture should return an AsyncMock."""
        assert isinstance(mock_api_client, AsyncMock)

    def test_has_agent_api_attached(self, mock_api_client, mock_agent_api) -> None:
        """mock_api_client should have agent_api attached."""
        assert mock_api_client.agent_api is mock_agent_api

    def test_has_human_api_attached(self, mock_api_client, mock_human_api) -> None:
        """mock_api_client should have human_api attached."""
        assert mock_api_client.human_api is mock_human_api

    def test_can_access_api_methods_through_client(self, mock_api_client) -> None:
        """Should be able to access API methods through the client."""
        response = mock_api_client.agent_api.get_agent_me.return_value
        assert response.data.id == "agent-123"


class TestSampleRoomMessageFixture:
    """Tests for the sample_room_message fixture."""

    def test_returns_message_created_payload(self, sample_room_message) -> None:
        """sample_room_message should return MessageCreatedPayload."""
        assert isinstance(sample_room_message, MessageCreatedPayload)

    def test_has_user_sender_type(self, sample_room_message) -> None:
        """sample_room_message should be from a User."""
        assert sample_room_message.sender_type == "User"
        assert sample_room_message.sender_id == "user-456"

    def test_mentions_testbot(self, sample_room_message) -> None:
        """sample_room_message should mention TestBot."""
        assert "@TestBot" in sample_room_message.content
        assert len(sample_room_message.metadata.mentions) == 1
        assert sample_room_message.metadata.mentions[0].username == "TestBot"


class TestSampleAgentMessageFixture:
    """Tests for the sample_agent_message fixture."""

    def test_returns_message_created_payload(self, sample_agent_message) -> None:
        """sample_agent_message should return MessageCreatedPayload."""
        assert isinstance(sample_agent_message, MessageCreatedPayload)

    def test_has_agent_sender_type(self, sample_agent_message) -> None:
        """sample_agent_message should be from an Agent."""
        assert sample_agent_message.sender_type == "Agent"
        assert sample_agent_message.sender_id == "agent-123"

    def test_same_room_as_user_message(
        self, sample_room_message, sample_agent_message
    ) -> None:
        """Both messages should be in the same room."""
        assert sample_room_message.chat_room_id == sample_agent_message.chat_room_id
