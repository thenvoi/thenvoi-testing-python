"""Tests for the settings module."""

from __future__ import annotations

import os
from unittest.mock import patch

from thenvoi_testing.settings import BaseTestSettings, ThenvoiTestSettings


class TestBaseTestSettings:
    """Tests for BaseTestSettings base class."""

    def test_loads_from_environment(self) -> None:
        """Should load settings from environment variables."""

        class TestSettings(BaseTestSettings):
            my_value: str = "default"

        with patch.dict(os.environ, {"MY_VALUE": "from-env"}):
            settings = TestSettings()
            assert settings.my_value == "from-env"

    def test_uses_defaults_when_env_not_set(self) -> None:
        """Should use defaults when env vars not set."""

        class TestSettings(BaseTestSettings):
            my_value: str = "default"

        with patch.dict(os.environ, {}, clear=True):
            settings = TestSettings()
            assert settings.my_value == "default"

    def test_case_insensitive(self) -> None:
        """Should load env vars case-insensitively."""

        class TestSettings(BaseTestSettings):
            my_api_key: str = ""

        with patch.dict(os.environ, {"MY_API_KEY": "secret"}):
            settings = TestSettings()
            assert settings.my_api_key == "secret"


class TestThenvoiTestSettings:
    """Tests for ThenvoiTestSettings class."""

    def test_default_values(self) -> None:
        """Should have sensible defaults."""
        with patch.dict(os.environ, {}, clear=True):
            settings = ThenvoiTestSettings()
            assert settings.thenvoi_api_key == ""
            assert settings.thenvoi_base_url == "http://localhost:4000"
            assert "localhost:4000" in settings.thenvoi_ws_url

    def test_has_api_key_property(self) -> None:
        """has_api_key should return True when key is set."""
        with patch.dict(os.environ, {"THENVOI_API_KEY": "test-key"}):
            settings = ThenvoiTestSettings()
            assert settings.has_api_key is True

        with patch.dict(os.environ, {}, clear=True):
            settings = ThenvoiTestSettings()
            assert settings.has_api_key is False

    def test_has_multi_agent_property(self) -> None:
        """has_multi_agent should require both keys."""
        with patch.dict(
            os.environ,
            {"THENVOI_API_KEY": "key1", "THENVOI_API_KEY_2": "key2"},
        ):
            settings = ThenvoiTestSettings()
            assert settings.has_multi_agent is True

        with patch.dict(os.environ, {"THENVOI_API_KEY": "key1"}):
            settings = ThenvoiTestSettings()
            assert settings.has_multi_agent is False

    def test_has_user_api_property(self) -> None:
        """has_user_api should check user API key."""
        with patch.dict(os.environ, {"THENVOI_API_KEY_USER": "user-key"}):
            settings = ThenvoiTestSettings()
            assert settings.has_user_api is True

        with patch.dict(os.environ, {}, clear=True):
            settings = ThenvoiTestSettings()
            assert settings.has_user_api is False

    def test_override_from_env(self) -> None:
        """Should load all settings from environment."""
        with patch.dict(
            os.environ,
            {
                "THENVOI_API_KEY": "api-key-1",
                "TEST_AGENT_ID": "agent-123",
                "THENVOI_BASE_URL": "https://api.thenvoi.com",
            },
        ):
            settings = ThenvoiTestSettings()
            assert settings.thenvoi_api_key == "api-key-1"
            assert settings.test_agent_id == "agent-123"
            assert settings.thenvoi_base_url == "https://api.thenvoi.com"
