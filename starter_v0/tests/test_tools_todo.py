"""TODO CP3 (student): Tool Unit Test Challenge.

Each test below is a stub. Replace `pytest.skip(...)` with a real test.
Patterns to copy are in test_tools_examples.py. Fixtures are in conftest.py.

Rules:
- Offline only: mock HTTP with `fake_http`, set fake keys with `monkeypatch.setenv`.
- One behaviour per test. Name the test after the behaviour, not the function.
- Done = `pytest tests/ -v` shows 0 skipped, 0 failed.
"""
from __future__ import annotations

import pytest

from conftest import FakeResponse  # noqa: F401  (you will need it)
from tools import TOOL_FUNCTIONS  # noqa: F401

TODO = "TODO CP3 (student): implement this test"


# ---------------- clarify ----------------

def test_clarify_choice_returns_options_and_awaits_user() -> None:
    # Call clarify with response_type="choice" and 2 options.
    # Assert: options are returned unchanged, awaiting_user is True.
    pytest.skip(TODO)


# ---------------- format ----------------

def test_format_sections_groups_items_by_section() -> None:
    # Items with section "A", "B", "A" -> markdown has exactly one "## A" and one "## B".
    pytest.skip(TODO)


def test_format_thread_numbers_items() -> None:
    # template="thread" -> lines start with "1/", "2/", ...
    pytest.skip(TODO)


def test_format_empty_items_does_not_crash() -> None:
    # items=None and items=[] -> item_count == 0, no exception.
    pytest.skip(TODO)


# ---------------- send (guardrail) ----------------

def test_send_confirmed_posts_to_telegram(monkeypatch, fake_http) -> None:
    # Set TELEGRAM_BOT_TOKEN / TELEGRAM_CHAT_ID, mock HTTP.
    # Assert: exactly one POST, URL contains the token, json has chat_id + text, status == "sent".
    pytest.skip(TODO)


def test_send_confirmed_without_env_returns_error_and_no_request(fake_http) -> None:
    pytest.skip(TODO)


# ---------------- lookup ----------------

def test_lookup_without_timeframe_omits_time_range(monkeypatch, fake_http) -> None:
    # timeframe=None -> request body has no "time_range" key.
    pytest.skip(TODO)


# ---------------- fetch ----------------

def test_fetch_maps_firecrawl_response(monkeypatch, fake_http) -> None:
    # Mock {"data": {"markdown": "...", "metadata": {"title": "T", "sourceURL": "https://..."}}}
    # Assert title/url/source/summary in result["items"][0].
    pytest.skip(TODO)


def test_fetch_truncates_markdown_to_4000_chars(monkeypatch, fake_http) -> None:
    pytest.skip(TODO)


# ---------------- timeline / social_search ----------------

def test_timeline_respects_limit_and_skips_items_without_id(monkeypatch, fake_http) -> None:
    # Mock {"timeline": [...]} with 1 item missing tweet_id and 6 valid items, limit=3.
    # Assert 3 items, and each url looks like https://x.com/<handle>/status/<id>.
    pytest.skip(TODO)


def test_social_search_passes_search_type(monkeypatch, fake_http) -> None:
    # Assert the request params carry the query and search_type ("Top" / "Latest").
    pytest.skip(TODO)


# ---------------- policy (local knowledge + trust boundary) ----------------

def test_policy_empty_query_returns_no_results() -> None:
    pytest.skip(TODO)


def test_policy_area_filter_only_returns_that_area() -> None:
    # policy_area="data_privacy" -> every result has policy_area == "data_privacy".
    pytest.skip(TODO)


def test_policy_instruction_like_lines_go_to_untrusted_text() -> None:
    # One policy file contains a quoted line that tries to give the assistant orders.
    # Query that section (source_citation) and assert: that line is in untrusted_text, NOT in facts.
    pytest.skip(TODO)


# ---------------- YOUR NEW TOOL(S) ----------------
# Write at least 3 tests per tool your team adds:
#   1. happy path (mocked if it calls an API)
#   2. bad / missing input from the model (empty string, wrong type, out-of-enum value)
#   3. failure path (missing key, HTTP error, timeout) -> returns error dict, does not raise

# hn_search: Hacker News search via the public Algolia API (team VietnamAirlines).

hn_search = TOOL_FUNCTIONS["hn_search"]

HN_HITS = {"hits": [
    {"objectID": "101", "title": "LLM agents in prod", "url": "https://www.example.com/agents",
     "author": "alice", "points": 300, "num_comments": 42, "created_at": "2026-11-01T10:00:00Z"},
    {"objectID": "102", "title": "Ask HN: How do you eval agents?", "url": None,
     "author": "bob", "points": 50, "num_comments": 10, "created_at": "2026-11-02T10:00:00Z"},
    {"title": "hit without objectID is skipped"},
]}


def test_hn_search_sends_expected_request_and_maps_results(fake_http) -> None:
    calls = fake_http(FakeResponse(HN_HITS))

    result = hn_search(query="LLM agents", limit=3)

    assert len(calls) == 1
    assert calls[0]["method"] == "GET"
    assert calls[0]["url"] == "https://hn.algolia.com/api/v1/search"
    assert calls[0]["params"] == {"query": "LLM agents", "tags": "story", "hitsPerPage": 3}
    assert result["sort"] == "relevance"
    assert result["items"][0] == {
        "title": "LLM agents in prod", "url": "https://www.example.com/agents", "source": "example.com",
        "discussion_url": "https://news.ycombinator.com/item?id=101",
        "author": "alice", "points": 300, "num_comments": 42, "date": "2026-11-01T10:00:00Z",
    }
    assert len(result["items"]) == 2  # the hit without objectID is dropped


def test_hn_search_story_without_url_falls_back_to_discussion_link(fake_http) -> None:
    fake_http(FakeResponse(HN_HITS))

    ask_hn = hn_search(query="eval")["items"][1]

    assert ask_hn["url"] == "https://news.ycombinator.com/item?id=102"
    assert ask_hn["source"] == "news.ycombinator.com"


def test_hn_search_sort_date_uses_search_by_date_and_coerces_string_limit(fake_http) -> None:
    calls = fake_http(FakeResponse({"hits": []}))

    result = hn_search(query="Rust", sort="date", limit="5")

    assert calls[0]["url"] == "https://hn.algolia.com/api/v1/search_by_date"
    assert calls[0]["params"]["hitsPerPage"] == 5
    assert result["items"] == []


def test_hn_search_clamps_out_of_range_limit(fake_http) -> None:
    calls = fake_http(FakeResponse({"hits": []}))

    hn_search(query="AI", limit=0)
    hn_search(query="AI", limit=999)

    assert calls[0]["params"]["hitsPerPage"] == 1
    assert calls[1]["params"]["hitsPerPage"] == 20


@pytest.mark.parametrize("bad_args", [
    {"query": ""},
    {"query": "   "},
    {"query": None},
    {"query": "AI", "sort": "popular"},
    {"query": "AI", "limit": "nhiều"},
])
def test_hn_search_bad_input_from_model_returns_error_without_request(fake_http, bad_args) -> None:
    calls = fake_http(FakeResponse(HN_HITS))

    result = hn_search(**bad_args)

    assert result["tool"] == "hn_search"
    assert result["error"] == "ValueError"
    assert calls == []


def test_hn_search_http_error_returns_error_dict(fake_http) -> None:
    fake_http(FakeResponse(status_code=503))

    result = hn_search(query="AI")

    assert result == {"tool": "hn_search", "error": "HTTPError", "message": "HTTP 503"}


def test_hn_search_timeout_returns_error_dict(fake_http) -> None:
    import requests

    fake_http(requests.Timeout("read timed out"))

    result = hn_search(query="AI")

    assert result["error"] == "Timeout"
    assert "timed out" in result["message"]
