from __future__ import annotations

from typing import Any

import requests

from tools._shared import TIMEOUT, domain, err

API_BASE = "https://hn.algolia.com/api/v1"
SORT_ENDPOINTS = {"relevance": "search", "date": "search_by_date"}
MAX_LIMIT = 20


def _coerce_limit(limit: Any) -> int:
    """Models sometimes send "5", 0, or negative numbers; clamp to 1..MAX_LIMIT."""
    try:
        value = int(limit)
    except (TypeError, ValueError):
        raise ValueError(f"limit must be an integer, got {limit!r}") from None
    return max(1, min(value, MAX_LIMIT))


def hn_search(query: str = "", sort: str = "relevance", limit: int = 5) -> dict[str, Any]:
    """Search Hacker News stories via the public Algolia API (no API key needed)."""
    try:
        query = (query or "").strip() if isinstance(query, str) else ""
        if not query:
            raise ValueError("query must be a non-empty string")
        sort = (sort or "relevance").strip().lower() if isinstance(sort, str) else ""
        if sort not in SORT_ENDPOINTS:
            raise ValueError(f"sort must be one of {sorted(SORT_ENDPOINTS)}, got {sort!r}")
        hits_per_page = _coerce_limit(limit)

        response = requests.get(
            f"{API_BASE}/{SORT_ENDPOINTS[sort]}",
            params={"query": query, "tags": "story", "hitsPerPage": hits_per_page},
            timeout=TIMEOUT,
        )
        response.raise_for_status()
        hits = response.json().get("hits", [])

        items = []
        for hit in hits:
            story_id = hit.get("objectID")
            if not story_id:
                continue
            discussion_url = f"https://news.ycombinator.com/item?id={story_id}"
            url = hit.get("url") or discussion_url
            items.append({
                "title": hit.get("title"),
                "url": url,
                "source": domain(url) or "news.ycombinator.com",
                "discussion_url": discussion_url,
                "author": hit.get("author"),
                "points": hit.get("points"),
                "num_comments": hit.get("num_comments"),
                "date": hit.get("created_at"),
            })
        return {"tool": "hn_search", "query": query, "sort": sort, "items": items[:hits_per_page]}
    except Exception as exc:
        return err("hn_search", exc)
