"""Tests for the factories module."""

from __future__ import annotations

from datetime import UTC

from thenvoi_testing.factories import (
    factory,
    make_pydantic_mock,
    make_timestamp,
    make_uuid,
)


class TestMakePydanticMock:
    """Tests for make_pydantic_mock helper."""

    def test_creates_mock_with_attributes(self) -> None:
        """Mock should have specified attributes."""
        mock = make_pydantic_mock(id="test-123", name="Test")
        assert mock.id == "test-123"
        assert mock.name == "Test"

    def test_model_dump_returns_dict(self) -> None:
        """model_dump() should return a dict of attributes."""
        mock = make_pydantic_mock(id="test-123", name="Test", value=42)
        result = mock.model_dump()

        assert result == {"id": "test-123", "name": "Test", "value": 42}

    def test_model_dump_with_none_values(self) -> None:
        """model_dump() should include None values."""
        mock = make_pydantic_mock(id="test-123", name=None, value="ok")
        result = mock.model_dump()

        assert result == {"id": "test-123", "name": None, "value": "ok"}

    def test_nested_mock_as_value(self) -> None:
        """Nested mocks are stored as-is (not serialized automatically)."""
        inner = make_pydantic_mock(inner_id="inner-1")
        outer = make_pydantic_mock(outer_id="outer-1", nested=inner)

        result = outer.model_dump()

        assert result["outer_id"] == "outer-1"
        # Nested mock is stored as the Mock object itself
        assert result["nested"] == inner


class TestHelpers:
    """Tests for helper functions."""

    def test_make_uuid_returns_uuid_string(self) -> None:
        """make_uuid() should return a valid UUID string."""
        uuid = make_uuid()
        assert isinstance(uuid, str)
        # UUID format: 8-4-4-4-12
        parts = uuid.split("-")
        assert len(parts) == 5
        assert len(parts[0]) == 8

    def test_make_timestamp_returns_datetime(self) -> None:
        """make_timestamp() should return a UTC datetime."""
        from datetime import datetime

        timestamp = make_timestamp()
        assert isinstance(timestamp, datetime)
        assert timestamp.tzinfo == UTC


class TestMockDataFactory:
    """Tests for MockDataFactory methods."""

    def test_agent_me_defaults(self) -> None:
        """agent_me() should return mock with OpenAPI example defaults."""
        agent = factory.agent_me()
        assert agent.id == "550e8400-e29b-41d4-a716-446655440000"
        assert agent.name == "Weather Assistant"

    def test_agent_me_override(self) -> None:
        """agent_me() should allow overriding defaults."""
        agent = factory.agent_me(id="custom-id", name="CustomBot")
        assert agent.id == "custom-id"
        assert agent.name == "CustomBot"

    def test_peer_defaults(self) -> None:
        """peer() should return mock with defaults."""
        peer = factory.peer()
        assert peer.type == "Agent"
        assert peer.is_global is True

    def test_chat_room_defaults(self) -> None:
        """chat_room() should return mock with defaults."""
        room = factory.chat_room()
        assert room.id == "daca00d0-eb6b-4db1-8201-c46015c93d04"
        assert room.title == "Q4 Sales Analysis Discussion"

    def test_chat_participant_defaults(self) -> None:
        """chat_participant() should return mock with defaults."""
        participant = factory.chat_participant()
        assert participant.name == "Data Analyst"
        assert participant.type == "Agent"

    def test_chat_message_defaults(self) -> None:
        """chat_message() should return mock with defaults."""
        message = factory.chat_message()
        assert message.message_type == "text"
        assert message.sender_type == "User"

    def test_chat_event_defaults(self) -> None:
        """chat_event() should return mock with defaults."""
        event = factory.chat_event()
        assert event.sender_type == "Agent"
        assert event.message_type == "thought"

    def test_response_wraps_data(self) -> None:
        """response() should wrap data and serialize correctly."""
        agent = factory.agent_me(id="test-123")
        response = factory.response(agent)

        assert response.data == agent
        result = response.model_dump()
        assert result["data"]["id"] == "test-123"

    def test_response_with_none(self) -> None:
        """response() should handle None data."""
        response = factory.response(None)
        result = response.model_dump()
        assert result["data"] is None

    def test_list_response_wraps_items(self) -> None:
        """list_response() should wrap list of items."""
        rooms = [factory.chat_room(id="room-1"), factory.chat_room(id="room-2")]
        response = factory.list_response(rooms)

        assert len(response.data) == 2
        assert response.meta["total"] == 2

        result = response.model_dump()
        assert len(result["data"]) == 2
        assert result["data"][0]["id"] == "room-1"

    def test_user_profile_defaults(self) -> None:
        """user_profile() should return mock with defaults."""
        profile = factory.user_profile()
        assert profile.name == "Test User"
        assert profile.email == "test@example.com"

    def test_owned_agent_defaults(self) -> None:
        """owned_agent() should return mock with defaults."""
        agent = factory.owned_agent()
        assert agent.is_external is True

    def test_registered_agent_has_credentials(self) -> None:
        """registered_agent() should include credentials."""
        reg = factory.registered_agent()
        assert hasattr(reg, "agent")
        assert hasattr(reg, "credentials")
        assert "thnv_" in reg.credentials.api_key

    def test_deleted_agent_defaults(self) -> None:
        """deleted_agent() should return mock with defaults."""
        deleted = factory.deleted_agent()
        assert deleted.executions_deleted == 0
