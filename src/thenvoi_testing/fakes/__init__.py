"""Fake implementations for testing.

This module provides fake implementations that can be used
instead of mocking frameworks for cleaner, more maintainable tests.

Usage:
    from thenvoi_testing.fakes import FakeAgentTools, FakePhoenixServer

    async def test_adapter():
        tools = FakeAgentTools()
        await tools.send_message(content="Hello!")
        assert len(tools.messages_sent) == 1
"""

from __future__ import annotations

from thenvoi_testing.fakes.agent_tools import FakeAgentTools

__all__ = [
    "FakeAgentTools",
]

# FakePhoenixServer is conditionally imported to avoid websockets dependency
try:
    from thenvoi_testing.fakes.phoenix_server import FakePhoenixServer

    __all__.append("FakePhoenixServer")
except ImportError:
    pass  # websockets not installed
