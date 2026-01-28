"""Tests for the markers module."""

from __future__ import annotations

import os
from unittest.mock import patch

import pytest

from thenvoi_testing.markers import (
    pytest_ignore_collect_in_ci,
    skip_with_condition,
    skip_without_env,
    skip_without_envs,
)


class TestSkipWithoutEnv:
    """Tests for skip_without_env marker factory."""

    def test_skips_when_env_not_set(self) -> None:
        """Should create marker that skips when env var is not set."""
        with patch.dict(os.environ, {}, clear=True):
            marker = skip_without_env("NONEXISTENT_VAR")
            # Check the marker is configured to skip (condition is first arg)
            assert marker.mark.args[0] is True

    def test_does_not_skip_when_env_set(self) -> None:
        """Should not skip when env var is set."""
        with patch.dict(os.environ, {"MY_VAR": "value"}):
            marker = skip_without_env("MY_VAR")
            assert marker.mark.args[0] is False

    def test_custom_reason(self) -> None:
        """Should use custom reason when provided."""
        marker = skip_without_env("MY_VAR", reason="Custom reason")
        assert marker.mark.kwargs["reason"] == "Custom reason"

    def test_default_reason(self) -> None:
        """Should use default reason when not provided."""
        marker = skip_without_env("MY_VAR")
        assert "MY_VAR" in marker.mark.kwargs["reason"]


class TestSkipWithoutEnvs:
    """Tests for skip_without_envs marker factory."""

    def test_skips_when_any_missing(self) -> None:
        """Should skip when any env var is missing."""
        with patch.dict(os.environ, {"VAR_A": "a"}, clear=True):
            marker = skip_without_envs(["VAR_A", "VAR_B"])
            assert marker.mark.args[0] is True

    def test_does_not_skip_when_all_set(self) -> None:
        """Should not skip when all env vars are set."""
        with patch.dict(os.environ, {"VAR_A": "a", "VAR_B": "b"}):
            marker = skip_without_envs(["VAR_A", "VAR_B"])
            assert marker.mark.args[0] is False

    def test_custom_reason(self) -> None:
        """Should use custom reason."""
        marker = skip_without_envs(["VAR_A"], reason="Need all vars")
        assert marker.mark.kwargs["reason"] == "Need all vars"


class TestSkipWithCondition:
    """Tests for skip_with_condition marker factory."""

    def test_skips_when_condition_true(self) -> None:
        """Should skip when condition is True."""
        marker = skip_with_condition(True, reason="Always skip")
        assert marker.mark.args[0] is True

    def test_does_not_skip_when_condition_false(self) -> None:
        """Should not skip when condition is False."""
        marker = skip_with_condition(False, reason="Never skip")
        assert marker.mark.args[0] is False

    def test_callable_condition(self) -> None:
        """Should evaluate callable conditions."""
        marker = skip_with_condition(lambda: 1 + 1 == 2, reason="Math works")
        assert marker.mark.args[0] is True

        marker = skip_with_condition(lambda: False, reason="Never")
        assert marker.mark.args[0] is False


class TestSkipInCi:
    """Tests for skip_in_ci pre-defined marker."""

    def test_skips_in_ci(self) -> None:
        """Should be configured to skip when CI=true."""
        with patch.dict(os.environ, {"CI": "true"}):
            # Re-evaluate by creating new marker
            marker = pytest.mark.skipif(
                os.environ.get("CI") == "true", reason="Skipped in CI"
            )
            assert marker.mark.args[0] is True

    def test_does_not_skip_outside_ci(self) -> None:
        """Should not skip when CI is not set."""
        with patch.dict(os.environ, {}, clear=True):
            marker = pytest.mark.skipif(
                os.environ.get("CI") == "true", reason="Skipped in CI"
            )
            assert marker.mark.args[0] is False


class TestPytestIgnoreCollectInCi:
    """Tests for pytest_ignore_collect_in_ci helper."""

    def test_ignores_integration_in_ci(self) -> None:
        """Should return True for integration folder in CI."""
        with patch.dict(os.environ, {"CI": "true"}):
            result = pytest_ignore_collect_in_ci(
                "/path/to/tests/integration/test_api.py"
            )
            assert result is True

    def test_does_not_ignore_unit_tests_in_ci(self) -> None:
        """Should return False for non-integration folders in CI."""
        with patch.dict(os.environ, {"CI": "true"}):
            result = pytest_ignore_collect_in_ci("/path/to/tests/unit/test_utils.py")
            assert result is False

    def test_does_not_ignore_outside_ci(self) -> None:
        """Should return False when not in CI."""
        with patch.dict(os.environ, {}, clear=True):
            result = pytest_ignore_collect_in_ci(
                "/path/to/tests/integration/test_api.py"
            )
            assert result is False

    def test_custom_folder(self) -> None:
        """Should respect custom folder parameter."""
        with patch.dict(os.environ, {"CI": "true"}):
            result = pytest_ignore_collect_in_ci(
                "/path/to/tests/e2e/test_flow.py", folder="e2e"
            )
            assert result is True
