---
name: hn_search
track: bonus
kind: live_api
provider: Hacker News Algolia API
requires_env: []
inputs: [query, sort, limit]
outputs: [items]
side_effect: false
---
# hn_search

Tool mới của nhóm VietnamAirlines. Tìm bài (story) trên Hacker News qua API công khai
`https://hn.algolia.com/api/v1`, không cần API key.

- `query`: từ khóa chủ đề, ví dụ `LLM agents`, `Rust`. Không được rỗng.
- `sort`: `relevance` (mặc định, endpoint `/search`) hoặc `date` (mới nhất, endpoint `/search_by_date`).
- `limit`: số bài, ép về khoảng 1–20; chấp nhận cả số dạng chuỗi như `"5"`.

Mỗi item trả về gồm `title`, `url` (link gốc; nếu là bài Ask HN không có link thì dùng link thảo luận),
`source`, `discussion_url`, `author`, `points`, `num_comments`, `date`.

Khi nào agent nên gọi: user hỏi cộng đồng dev/tech, Hacker News hoặc HN đang bàn gì về một chủ đề.
Không dùng cho tin tức web chung (dùng `lookup`) hay bài đăng Twitter/X (dùng `social_search` / `timeline`).

Lỗi (query rỗng, `sort` ngoài enum, `limit` không phải số, HTTP lỗi, timeout) đều trả về error dict
`{"tool", "error", "message"}`, không raise.
