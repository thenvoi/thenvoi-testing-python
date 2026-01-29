"""Tests for the fakes module."""

from __future__ import annotations

import pytest

from thenvoi_testing.fakes import FakeAgentTools


class TestFakeAgentTools:
    """Tests for FakeAgentTools fake implementation."""

    @pytest.fixture
    def tools(self) -> FakeAgentTools:
        """Create a fresh FakeAgentTools instance."""
        return FakeAgentTools()

    @pytest.mark.asyncio
    async def test_send_message_tracks_messages(self, tools: FakeAgentTools) -> None:
        """send_message() should track all sent messages."""
        result = await tools.send_message("Hello, world!")

        assert len(tools.messages_sent) == 1
        assert tools.messages_sent[0]["content"] == "Hello, world!"
        assert result["id"] == "msg-0"

    @pytest.mark.asyncio
    async def test_send_message_with_mentions(self, tools: FakeAgentTools) -> None:
        """send_message() should track mentions."""
        mentions = [{"id": "user-1", "name": "Alice"}]
        await tools.send_message("Hey @Alice", mentions=mentions)

        assert tools.messages_sent[0]["mentions"] == mentions

    @pytest.mark.asyncio
    async def test_send_event_tracks_events(self, tools: FakeAgentTools) -> None:
        """send_event() should track all sent events."""
        result = await tools.send_event(
            content="Processing...", message_type="thought", metadata={"step": 1}
        )

        assert len(tools.events_sent) == 1
        assert tools.events_sent[0]["content"] == "Processing..."
        assert tools.events_sent[0]["message_type"] == "thought"
        assert tools.events_sent[0]["metadata"]["step"] == 1
        assert result["id"] == "evt-0"

    @pytest.mark.asyncio
    async def test_add_participant_tracks_additions(
        self, tools: FakeAgentTools
    ) -> None:
        """add_participant() should track added participants."""
        result = await tools.add_participant("Alice", role="admin")

        assert len(tools.participants_added) == 1
        assert tools.participants_added[0]["name"] == "Alice"
        assert tools.participants_added[0]["role"] == "admin"
        assert result["id"] == "p-Alice"

    @pytest.mark.asyncio
    async def test_remove_participant_tracks_removals(
        self, tools: FakeAgentTools
    ) -> None:
        """remove_participant() should track removed participants."""
        result = await tools.remove_participant("Bob")

        assert len(tools.participants_removed) == 1
        assert tools.participants_removed[0]["name"] == "Bob"
        assert result["id"] == "p-Bob"

    @pytest.mark.asyncio
    async def test_get_participants_returns_empty_list(
        self, tools: FakeAgentTools
    ) -> None:
        """get_participants() should return empty list by default."""
        result = await tools.get_participants()
        assert result == []

    @pytest.mark.asyncio
    async def test_lookup_peers_returns_empty_result(
        self, tools: FakeAgentTools
    ) -> None:
        """lookup_peers() should return empty result with pagination."""
        result = await tools.lookup_peers(page=2, page_size=25)

        assert result["peers"] == []
        assert result["metadata"]["page"] == 2
        assert result["metadata"]["page_size"] == 25
        assert result["metadata"]["total"] == 0

    @pytest.mark.asyncio
    async def test_create_chatroom_returns_uuid(self, tools: FakeAgentTools) -> None:
        """create_chatroom() should return a room ID."""
        room_id = await tools.create_chatroom()
        assert room_id.startswith("room-")

    @pytest.mark.asyncio
    async def test_create_chatroom_with_task_id(self, tools: FakeAgentTools) -> None:
        """create_chatroom() should accept optional task_id."""
        room_id = await tools.create_chatroom(task_id="task-123")
        assert room_id.startswith("room-")

    def test_get_tool_schemas_returns_empty_list(self, tools: FakeAgentTools) -> None:
        """get_tool_schemas() should return empty list by default."""
        assert tools.get_tool_schemas("openai") == []

    def test_get_anthropic_tool_schemas_returns_empty(
        self, tools: FakeAgentTools
    ) -> None:
        """get_anthropic_tool_schemas() should return empty list."""
        assert tools.get_anthropic_tool_schemas() == []

    def test_get_openai_tool_schemas_returns_empty(self, tools: FakeAgentTools) -> None:
        """get_openai_tool_schemas() should return empty list."""
        assert tools.get_openai_tool_schemas() == []

    @pytest.mark.asyncio
    async def test_execute_tool_call_tracks_calls(self, tools: FakeAgentTools) -> None:
        """execute_tool_call() should track all tool calls."""
        result = await tools.execute_tool_call(
            "get_weather", {"location": "New York", "unit": "celsius"}
        )

        assert len(tools.tool_calls) == 1
        assert tools.tool_calls[0]["tool_name"] == "get_weather"
        assert tools.tool_calls[0]["arguments"]["location"] == "New York"
        assert result == {"status": "ok"}

    @pytest.mark.asyncio
    async def test_multiple_operations_tracked_separately(
        self, tools: FakeAgentTools
    ) -> None:
        """All operations should be tracked in their respective lists."""
        await tools.send_message("Hello")
        await tools.send_message("World")
        await tools.send_event("Processing", "thought")
        await tools.add_participant("Alice")
        await tools.execute_tool_call("test_tool", {})

        assert len(tools.messages_sent) == 2
        assert len(tools.events_sent) == 1
        assert len(tools.participants_added) == 1
        assert len(tools.tool_calls) == 1
