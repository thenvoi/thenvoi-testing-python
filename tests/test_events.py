"""Tests for the event factories and streaming types."""

from __future__ import annotations

from thenvoi_testing.factories.events import (
    MessageEvent,
    ParticipantAddedEvent,
    ParticipantRemovedEvent,
    RoomAddedEvent,
    RoomRemovedEvent,
    make_message_event,
    make_participant_added_event,
    make_participant_removed_event,
    make_room_added_event,
    make_room_removed_event,
)
from thenvoi_testing.streaming import (
    Mention,
    MessageCreatedPayload,
    MessageMetadata,
    ParticipantAddedPayload,
    ParticipantRemovedPayload,
    RoomAddedPayload,
    RoomOwner,
    RoomRemovedPayload,
)


class TestStreamingTypes:
    """Tests for the streaming payload types."""

    def test_message_metadata_creation(self) -> None:
        """MessageMetadata should be created with mentions."""
        metadata = MessageMetadata(
            mentions=[Mention(id="agent-1", username="Bot")],
            status="sent",
        )
        assert len(metadata.mentions) == 1
        assert metadata.mentions[0].id == "agent-1"
        assert metadata.status == "sent"

    def test_message_created_payload(self) -> None:
        """MessageCreatedPayload should be created with all fields."""
        payload = MessageCreatedPayload(
            id="msg-123",
            content="Hello world",
            message_type="text",
            metadata=MessageMetadata(mentions=[], status="sent"),
            sender_id="user-456",
            sender_type="User",
            chat_room_id="room-789",
            inserted_at="2024-01-01T00:00:00Z",
            updated_at="2024-01-01T00:00:00Z",
        )
        assert payload.id == "msg-123"
        assert payload.content == "Hello world"
        assert payload.sender_type == "User"

    def test_room_added_payload(self) -> None:
        """RoomAddedPayload should be created with owner."""
        owner = RoomOwner(id="user-1", name="Test User", type="User")
        payload = RoomAddedPayload(
            id="room-123",
            owner=owner,
            status="active",
            type="direct",
            title="Test Room",
            created_at="2024-01-01T00:00:00Z",
            participant_role="member",
        )
        assert payload.id == "room-123"
        assert payload.owner.name == "Test User"

    def test_room_removed_payload(self) -> None:
        """RoomRemovedPayload should be created correctly."""
        payload = RoomRemovedPayload(
            id="room-123",
            status="removed",
            type="direct",
            title="Test Room",
            removed_at="2024-01-01T00:00:00Z",
        )
        assert payload.id == "room-123"
        assert payload.status == "removed"

    def test_participant_added_payload(self) -> None:
        """ParticipantAddedPayload should be created correctly."""
        payload = ParticipantAddedPayload(id="user-123", name="Test User", type="User")
        assert payload.id == "user-123"
        assert payload.name == "Test User"

    def test_participant_removed_payload(self) -> None:
        """ParticipantRemovedPayload should be created correctly."""
        payload = ParticipantRemovedPayload(id="user-123")
        assert payload.id == "user-123"


class TestMakeMessageEvent:
    """Tests for make_message_event factory."""

    def test_creates_message_event(self) -> None:
        """make_message_event should return a MessageEvent."""
        event = make_message_event()
        assert isinstance(event, MessageEvent)

    def test_default_values(self) -> None:
        """make_message_event should use sensible defaults."""
        event = make_message_event()
        assert event.payload is not None
        assert event.room_id == "room-123"
        assert event.payload.id == "msg-123"
        assert event.payload.sender_type == "User"

    def test_custom_values(self) -> None:
        """make_message_event should accept custom values."""
        event = make_message_event(
            room_id="custom-room",
            msg_id="custom-msg",
            content="Custom content",
            sender_id="custom-sender",
            sender_type="Agent",
        )
        assert event.payload is not None
        assert event.room_id == "custom-room"
        assert event.payload.id == "custom-msg"
        assert event.payload.content == "Custom content"
        assert event.payload.sender_id == "custom-sender"
        assert event.payload.sender_type == "Agent"

    def test_custom_metadata(self) -> None:
        """make_message_event should accept custom metadata."""
        custom_metadata = MessageMetadata(
            mentions=[Mention(id="bot-1", username="TestBot")],
            status="delivered",
        )
        event = make_message_event(metadata=custom_metadata)
        assert event.payload is not None
        assert len(event.payload.metadata.mentions) == 1
        assert event.payload.metadata.status == "delivered"


class TestMakeRoomAddedEvent:
    """Tests for make_room_added_event factory."""

    def test_creates_room_added_event(self) -> None:
        """make_room_added_event should return a RoomAddedEvent."""
        event = make_room_added_event()
        assert isinstance(event, RoomAddedEvent)

    def test_default_values(self) -> None:
        """make_room_added_event should use sensible defaults."""
        event = make_room_added_event()
        assert event.payload is not None
        assert event.room_id == "room-123"
        assert event.payload.title == "Test Room"
        assert event.payload.status == "active"

    def test_custom_values(self) -> None:
        """make_room_added_event should accept custom values."""
        event = make_room_added_event(
            room_id="custom-room",
            title="Custom Room",
            status="pending",
            type="group",
        )
        assert event.payload is not None
        assert event.room_id == "custom-room"
        assert event.payload.title == "Custom Room"
        assert event.payload.status == "pending"
        assert event.payload.type == "group"

    def test_custom_owner(self) -> None:
        """make_room_added_event should accept custom owner."""
        custom_owner = RoomOwner(id="agent-1", name="Bot", type="Agent")
        event = make_room_added_event(owner=custom_owner)
        assert event.payload is not None
        assert event.payload.owner.id == "agent-1"
        assert event.payload.owner.type == "Agent"


class TestMakeRoomRemovedEvent:
    """Tests for make_room_removed_event factory."""

    def test_creates_room_removed_event(self) -> None:
        """make_room_removed_event should return a RoomRemovedEvent."""
        event = make_room_removed_event()
        assert isinstance(event, RoomRemovedEvent)

    def test_default_values(self) -> None:
        """make_room_removed_event should use sensible defaults."""
        event = make_room_removed_event()
        assert event.payload is not None
        assert event.room_id == "room-123"
        assert event.payload.status == "removed"

    def test_custom_values(self) -> None:
        """make_room_removed_event should accept custom values."""
        event = make_room_removed_event(
            room_id="custom-room",
            title="Custom Room",
            status="archived",
        )
        assert event.payload is not None
        assert event.room_id == "custom-room"
        assert event.payload.title == "Custom Room"
        assert event.payload.status == "archived"


class TestMakeParticipantAddedEvent:
    """Tests for make_participant_added_event factory."""

    def test_creates_participant_added_event(self) -> None:
        """make_participant_added_event should return a ParticipantAddedEvent."""
        event = make_participant_added_event()
        assert isinstance(event, ParticipantAddedEvent)

    def test_default_values(self) -> None:
        """make_participant_added_event should use sensible defaults."""
        event = make_participant_added_event()
        assert event.payload is not None
        assert event.room_id == "room-123"
        assert event.payload.name == "Test User"
        assert event.payload.type == "User"

    def test_custom_values(self) -> None:
        """make_participant_added_event should accept custom values."""
        event = make_participant_added_event(
            room_id="custom-room",
            participant_id="agent-123",
            name="Bot",
            type="Agent",
        )
        assert event.payload is not None
        assert event.room_id == "custom-room"
        assert event.payload.id == "agent-123"
        assert event.payload.name == "Bot"
        assert event.payload.type == "Agent"


class TestMakeParticipantRemovedEvent:
    """Tests for make_participant_removed_event factory."""

    def test_creates_participant_removed_event(self) -> None:
        """make_participant_removed_event should return a ParticipantRemovedEvent."""
        event = make_participant_removed_event()
        assert isinstance(event, ParticipantRemovedEvent)

    def test_default_values(self) -> None:
        """make_participant_removed_event should use sensible defaults."""
        event = make_participant_removed_event()
        assert event.payload is not None
        assert event.room_id == "room-123"
        assert event.payload.id == "user-456"

    def test_custom_values(self) -> None:
        """make_participant_removed_event should accept custom values."""
        event = make_participant_removed_event(
            room_id="custom-room",
            participant_id="agent-123",
        )
        assert event.payload is not None
        assert event.room_id == "custom-room"
        assert event.payload.id == "agent-123"
