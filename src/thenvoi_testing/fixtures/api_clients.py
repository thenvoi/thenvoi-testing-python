"""Shared API client mock fixtures.

Provides pre-configured mock fixtures for testing code that uses
the Thenvoi REST API client.

Fixtures:
- mock_agent_api: MagicMock of the agent_api namespace
- mock_human_api: MagicMock of the human_api namespace
- mock_api_client: AsyncMock with both APIs attached
"""

from __future__ import annotations

from unittest.mock import AsyncMock, MagicMock

import pytest

from thenvoi_testing.factories import factory


@pytest.fixture
def mock_agent_api() -> MagicMock:
    """Create a mocked agent_api with pre-configured return values.

    This is an explicit MagicMock - it will NOT auto-create any attributes.
    Tests must set up return values for methods they want to call.

    Pre-configured methods:
    - get_agent_me() - Returns factory.agent_me()
    - list_agent_chats() - Returns two chat rooms
    - list_agent_chat_participants() - Returns one participant
    - create_agent_chat_event() - Returns factory.chat_event()
    - create_agent_chat_message() - Returns factory.chat_message()

    Example:
        def test_agent_api(mock_agent_api):
            # Override default return value if needed
            mock_agent_api.get_agent_me.return_value = factory.response(
                factory.agent_me(id="custom-id")
            )

            # Call your code
            result = await some_function(mock_agent_api)

            # Verify the correct method was called
            mock_agent_api.get_agent_me.assert_called_once()
    """
    agent_api = MagicMock()

    # Pre-configure common methods with default responses
    agent_api.get_agent_me.return_value = factory.response(
        factory.agent_me(id="agent-123", name="TestBot", description="Test agent")
    )

    agent_api.list_agent_chats.return_value = factory.list_response(
        [
            factory.chat_room(id="room-1"),
            factory.chat_room(id="room-2"),
        ]
    )

    agent_api.list_agent_chat_participants.return_value = factory.list_response(
        [
            factory.chat_participant(id="agent-123", name="TestBot", type="Agent"),
        ]
    )

    agent_api.create_agent_chat_event.return_value = factory.response(
        factory.chat_event()
    )

    agent_api.create_agent_chat_message.return_value = factory.response(
        factory.chat_message()
    )

    return agent_api


@pytest.fixture
def mock_human_api() -> MagicMock:
    """Create a mocked human_api with pre-configured return values.

    This is an explicit MagicMock for the User API (human_api namespace).

    Pre-configured methods:
    - get_my_profile() - Returns factory.user_profile()
    - list_my_agents() - Returns one owned agent
    - register_my_agent() - Returns factory.registered_agent()
    - delete_my_agent() - Returns factory.deleted_agent()
    - list_my_chats() - Returns one chat room
    - create_my_chat_room() - Returns factory.chat_room()
    - get_my_chat_room() - Returns factory.chat_room()
    - list_my_chat_participants() - Returns one participant
    - list_my_peers() - Returns one peer

    Example:
        def test_user_api(mock_human_api):
            # Override return value
            mock_human_api.list_my_agents.return_value = factory.list_response([
                factory.owned_agent(id="agent-1"),
                factory.owned_agent(id="agent-2"),
            ])

            # Call your code
            result = await some_function(mock_human_api)

            # Verify
            mock_human_api.list_my_agents.assert_called_once()
    """
    human_api = MagicMock()

    # Profile
    human_api.get_my_profile.return_value = factory.response(factory.user_profile())

    # Agents
    human_api.list_my_agents.return_value = factory.list_response(
        [factory.owned_agent()]
    )
    human_api.register_my_agent.return_value = factory.response(
        factory.registered_agent()
    )
    human_api.delete_my_agent.return_value = factory.response(factory.deleted_agent())

    # Chats
    human_api.list_my_chats.return_value = factory.list_response(
        [factory.chat_room(id="room-1")]
    )
    human_api.create_my_chat_room.return_value = factory.response(factory.chat_room())
    human_api.get_my_chat_room.return_value = factory.response(factory.chat_room())
    human_api.list_my_chat_participants.return_value = factory.list_response(
        [factory.chat_participant()]
    )
    human_api.list_my_peers.return_value = factory.list_response([factory.peer()])

    return human_api


@pytest.fixture
def mock_api_client(mock_agent_api: MagicMock, mock_human_api: MagicMock) -> AsyncMock:
    """Create a mocked AsyncRestClient with both APIs attached.

    Combines mock_agent_api and mock_human_api into a single client mock.
    Use this when testing code that needs the full API client.

    Example:
        async def test_with_full_client(mock_api_client, mock_agent_api):
            # Set up specific return value via the sub-fixture
            mock_agent_api.get_agent_me.return_value = factory.response(
                factory.agent_me(name="CustomBot")
            )

            # Pass the client to your code
            await some_function(mock_api_client)

            # Verify via the sub-fixture
            mock_agent_api.get_agent_me.assert_called_once()

        async def test_user_operations(mock_api_client, mock_human_api):
            # Access human_api through the client or directly
            await user_operation(mock_api_client)
            mock_human_api.register_my_agent.assert_called_once()
    """
    client = AsyncMock()
    client.agent_api = mock_agent_api
    client.human_api = mock_human_api
    return client
