"""Tests for the pagination utilities."""

from __future__ import annotations

import json

from thenvoi_testing.pagination import (
    fetch_all_pages,
    find_item_in_pages,
    item_exists_in_pages,
)


class MockContext:
    """Mock context for testing pagination functions."""

    pass


def make_paginated_response(
    items: list[dict],
    page: int,
    total_pages: int,
) -> str:
    """Create a mock paginated API response."""
    return json.dumps(
        {
            "data": items,
            "metadata": {
                "page": page,
                "total_pages": total_pages,
                "page_size": len(items),
            },
        }
    )


class TestFetchAllPages:
    """Tests for fetch_all_pages function."""

    def test_single_page(self) -> None:
        """Should return all items from a single page."""
        items = [{"id": "1", "name": "Item 1"}, {"id": "2", "name": "Item 2"}]

        def list_func(ctx, page: int = 1, page_size: int = 50) -> str:
            return make_paginated_response(items, page=1, total_pages=1)

        ctx = MockContext()
        result = fetch_all_pages(ctx, list_func)

        assert len(result) == 2
        assert result[0]["id"] == "1"
        assert result[1]["id"] == "2"

    def test_multiple_pages(self) -> None:
        """Should fetch and combine items from multiple pages."""
        pages = {
            1: [{"id": "1"}, {"id": "2"}],
            2: [{"id": "3"}, {"id": "4"}],
            3: [{"id": "5"}],
        }

        def list_func(ctx, page: int = 1, page_size: int = 50) -> str:
            return make_paginated_response(pages[page], page=page, total_pages=3)

        ctx = MockContext()
        result = fetch_all_pages(ctx, list_func)

        assert len(result) == 5
        assert [item["id"] for item in result] == ["1", "2", "3", "4", "5"]

    def test_empty_results(self) -> None:
        """Should return empty list for no results."""

        def list_func(ctx, page: int = 1, page_size: int = 50) -> str:
            return make_paginated_response([], page=1, total_pages=1)

        ctx = MockContext()
        result = fetch_all_pages(ctx, list_func)

        assert result == []

    def test_passes_kwargs(self) -> None:
        """Should pass additional kwargs to list function."""
        received_kwargs: dict = {}

        def list_func(
            ctx, page: int = 1, page_size: int = 50, filter_by: str = ""
        ) -> str:
            received_kwargs["filter_by"] = filter_by
            return make_paginated_response([{"id": "1"}], page=1, total_pages=1)

        ctx = MockContext()
        fetch_all_pages(ctx, list_func, filter_by="active")

        assert received_kwargs["filter_by"] == "active"


class TestFindItemInPages:
    """Tests for find_item_in_pages function."""

    def test_finds_item_on_first_page(self) -> None:
        """Should find item on the first page."""
        items = [{"id": "1", "name": "First"}, {"id": "2", "name": "Target"}]

        def list_func(ctx, page: int = 1, page_size: int = 50) -> str:
            return make_paginated_response(items, page=1, total_pages=1)

        ctx = MockContext()
        result = find_item_in_pages(
            ctx, list_func, lambda item: item["name"] == "Target"
        )

        assert result is not None
        assert result["id"] == "2"

    def test_finds_item_on_later_page(self) -> None:
        """Should find item on a later page."""
        pages = {
            1: [{"id": "1", "name": "First"}],
            2: [{"id": "2", "name": "Target"}],
        }

        def list_func(ctx, page: int = 1, page_size: int = 50) -> str:
            return make_paginated_response(pages[page], page=page, total_pages=2)

        ctx = MockContext()
        result = find_item_in_pages(
            ctx, list_func, lambda item: item["name"] == "Target"
        )

        assert result is not None
        assert result["id"] == "2"

    def test_returns_none_when_not_found(self) -> None:
        """Should return None when item is not found."""
        items = [{"id": "1", "name": "First"}, {"id": "2", "name": "Second"}]

        def list_func(ctx, page: int = 1, page_size: int = 50) -> str:
            return make_paginated_response(items, page=1, total_pages=1)

        ctx = MockContext()
        result = find_item_in_pages(
            ctx, list_func, lambda item: item["name"] == "NonExistent"
        )

        assert result is None

    def test_stops_early_when_found(self) -> None:
        """Should stop fetching pages once item is found."""
        pages_fetched: list[int] = []

        def list_func(ctx, page: int = 1, page_size: int = 50) -> str:
            pages_fetched.append(page)
            if page == 1:
                return make_paginated_response(
                    [{"id": "target"}], page=1, total_pages=10
                )
            return make_paginated_response(
                [{"id": f"other-{page}"}], page=page, total_pages=10
            )

        ctx = MockContext()
        result = find_item_in_pages(ctx, list_func, lambda item: item["id"] == "target")

        assert result is not None
        assert pages_fetched == [1]  # Only first page was fetched


class TestItemExistsInPages:
    """Tests for item_exists_in_pages function."""

    def test_returns_true_when_item_exists(self) -> None:
        """Should return True when item with ID exists."""
        items = [{"id": "target-id", "name": "Target"}]

        def list_func(ctx, page: int = 1, page_size: int = 50) -> str:
            return make_paginated_response(items, page=1, total_pages=1)

        ctx = MockContext()
        result = item_exists_in_pages(ctx, list_func, "target-id")

        assert result is True

    def test_returns_false_when_item_not_found(self) -> None:
        """Should return False when item with ID does not exist."""
        items = [{"id": "other-id", "name": "Other"}]

        def list_func(ctx, page: int = 1, page_size: int = 50) -> str:
            return make_paginated_response(items, page=1, total_pages=1)

        ctx = MockContext()
        result = item_exists_in_pages(ctx, list_func, "nonexistent-id")

        assert result is False

    def test_searches_multiple_pages(self) -> None:
        """Should search across multiple pages."""
        pages = {
            1: [{"id": "1"}],
            2: [{"id": "target-id"}],
        }

        def list_func(ctx, page: int = 1, page_size: int = 50) -> str:
            return make_paginated_response(pages[page], page=page, total_pages=2)

        ctx = MockContext()
        result = item_exists_in_pages(ctx, list_func, "target-id")

        assert result is True
