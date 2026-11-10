# Báo cáo cá nhân — Người 1: Tool Engineer & Unit Testing

> Căn cứ theo bảng phân công tại [PHAN_CONG_NHOM_3_NGUOI.md](../../PHAN_CONG_NHOM_3_NGUOI.md) và kết quả nghiệm thu tại [report/team/group_report.md](group_report.md).

---

## 1. Thông tin thành viên

- Họ tên: Nguyễn Thanh Tùng
- MSSV: 2A202603957
- Email: Thtung13102004@gmail.com

---

## 2. Phần việc phụ trách

* **Setup & Baseline (Phối hợp CP1):** Rà soát các API key phụ trợ, kiểm tra đảm bảo bộ test baseline ban đầu chạy pass.
* **Xây dựng Tool mới (CP3):**
   - Lựa chọn, thiết kế hoàn chỉnh tool mới `hn_search` (Hacker News Search).
   - Viết logic thực thi trong `tool.py`, thiết lập cơ chế phòng vệ: kiểm tra hợp lệ đầu vào, ép kiểu tham số, tuyệt đối không để exception làm sập runtime của Agent.
   - Viết tài liệu đặc tả `TOOL.md` đầy đủ frontmatter (`name`, `description`, `args`, `returns`).
   - Khai báo và đăng ký tool vào `starter_v0/tools/__init__.py` (`TOOL_FUNCTIONS`); bàn giao schema tham số cho Người 2 (để đưa vào `tools.yaml`) và Người 3 (để viết kịch bản eval).
* **Phát triển Unit Test cho Tool mới (CP3):**
   - Viết bộ unit test toàn diện cho tool mới trong `starter_v0/tests/test_tools_todo.py`, bao phủ từ happy path, bad input, boundary clamping đến các tình huống lỗi mạng/HTTP.
   - Đảm bảo toàn bộ test chạy offline qua `fake_http`, đạt 100% pass trên `pytest`.
4. **Đóng góp nội dung báo cáo:** Tổng hợp bằng chứng kỹ thuật về tool mới và kết quả unit test để đưa vào báo cáo nhóm tại `report/team/group_report.md`.

---

## 3. Đóng góp cụ thể

- **Hiện thực tool mới `hn_search`:**
  - Tích hợp Algolia API tìm kiếm tin tức, thảo luận lập trình trên Hacker News với 2 chế độ: liên quan (`sort="relevance"`) và theo thời gian (`sort="date"`).
  - Xây dựng các guardrail an toàn:
    - Input validation: Trả về dict lỗi `{"error": ...}` ngay lập tức khi `query` rỗng hoặc `sort` sai enum, tránh gửi request vô ích lên API.
    - Argument coercion & boundary clamping: Tự động ép kiểu chuỗi sang số nguyên khi model truyền `limit="5"`; tự động kẹp ngưỡng an toàn trong khoảng `[1, 20]` khi model truyền giá trị biên như `0` hoặc `999`.
    - Fallback cơ chế: Tự động trỏ về link bài thảo luận trên HN nếu story không có URL ngoài.
    - Error handling: Bắt trọn toàn bộ ngoại lệ HTTP (429, 500, 503, timeout) và trả về format `{"error": str(e), "items": []}`, đảm bảo agent không bao giờ bị dừng đột ngột.
  - Soạn thảo tài liệu chuẩn `TOOL.md` và đăng ký vào registry `starter_v0/tools/__init__.py`.

- **Xây dựng bộ Unit Test:**
  - Đóng góp 7 hàm test (tương đương 11 test cases khi tính `@pytest.mark.parametrize`), vượt xa yêu cầu tối thiểu (≥ 3 test/tool):
    1. *Happy path:* Kiểm tra query parameters gửi đi và ánh xạ chính xác các trường dữ liệu kết quả (`test_hn_search_happy_path`).
    2. *Discussion fallback:* Kiểm tra fallback link thảo luận khi thiếu `story_url` (`test_hn_search_fallback_to_story_url`).
    3. *Date sorting & String coercion:* Kiểm tra gọi endpoint `search_by_date` và tự ép kiểu `limit="5"` dạng string (`test_hn_search_sort_date_and_string_limit`).
    4. *Boundary clamping:* Kiểm tra ép `limit` về cận an toàn 1 khi nhận `0`, và về 20 khi nhận `999` (`test_hn_search_clamps_out_of_range_limit`).
    5. *Bad input:* Kiểm tra 5 trường hợp input xấu/lỗi cú pháp (chuỗi rỗng, kiểu không hợp lệ...) trả về error dict mà không gọi mạng (`test_hn_search_bad_inputs`).
    6. *HTTP Error handling:* Giả lập HTTP 503 từ server, đảm bảo tool trả về error dict mà không throw exception (`test_hn_search_http_error`).
    7. *Timeout handling:* Giả lập request timeout (`test_hn_search_timeout`).
  - Kiểm thử đạt: **78 passed, 14 skipped, 0 failed** trên toàn bộ suite test.

- **Bàn giao và tích hợp:**
  - Chuyển giao thông số `hn_search` cho Người 2 khai báo vào `artifacts/tools.yaml` (ở bản `v3-final`).
  - Phối hợp cùng Người 3 xác thực 4 eval cases gọi tool `hn_search` (G01, G02, G06, G07) trong `starter_v0/data/eval_group.json`, đạt tỷ lệ thành công 100%.

---

## 4. Bằng chứng

Toàn bộ kết quả thực thi và bằng chứng kỹ thuật của Người 1 đã được nghiệm thu và ghi nhận chi tiết tại file báo cáo nhóm [report/team/group_report.md](group_report.md):

- **File/Mục đối chiếu trong `group_report.md`:**
  1. **Mục A2 — Bảng danh sách Tool agent có:**
     - Xác nhận tool mới `hn_search` đã được tích hợp vào danh mục hoạt động của agent với ghi chú "Tool mới nhóm thêm: có" và mô tả: *Tìm bài trên Hacker News theo chủ đề (`sort` relevance/date, `limit`); API công khai, không cần key*.
  2. **Mục 3 — Giải pháp (Tool mới `hn_search`):**
     - Mô tả chi tiết kiến trúc, API endpoint, nguyên lý kiểm tra input, cơ chế ép kiểu `limit` và kẹp ngưỡng `1–20`, cùng định hướng tình huống Agent nên gọi.
  3. **Mục B5a — Bảng Required Evidence (Tool mới, unit test, UI):**
     - **Minh chứng Tool mới:** Trỏ trực tiếp tới `starter_v0/tools/hn_search/tool.py` và `starter_v0/tools/hn_search/TOOL.md`.
     - **Minh chứng Unit test:** Trỏ tới file `starter_v0/tests/test_tools_todo.py`. Kết quả `pytest` được xác thực: **78 passed, 14 skipped, 0 failed**.
     - **Minh chứng lỗi unit test bắt được nhưng eval không bắt được:** Phân tích thực tế về việc xử lý `limit="5"` (string), kẹp biên `limit=0` và chặn `query=""` trước khi gửi request.
  4. **Mục B3 — Team Eval Cases:**
     - Bằng chứng 4 case eval nhóm sử dụng tool `hn_search` (G01, G02, G06, G07) đều đạt **PASS** trong run `v3-final_B_group_openrouter_20261110T185319916584.json`.

- **AI/công cụ đã dùng và cách tự kiểm tra kết quả:**
  - *Công cụ đã dùng:* Python 3.11, Pytest, VS Code/Cursor. Sử dụng AI Assistant để hỗ trợ rà soát các trường hợp biên của API Algolia và cấu trúc mock `fake_http`.
  - *Cách tự kiểm tra kết quả:* 
    - Chạy unit test cô lập: `pytest starter_v0/tests/test_tools_todo.py -v` đảm bảo 100% test case của `hn_search` đều xanh lá và chạy hoàn toàn offline không gọi ra Internet.
    - Đối soát nội dung và số liệu kỹ thuật với file [group_report.md](group_report.md).

---

## 5. Tự đánh giá

- **Độ tin cậy của code:** Tool `hn_search` có tính phòng vệ cao, xử lý được các input lệch chuẩn từ mô hình LLM. Bộ test bao phủ sâu và đầy đủ kịch bản lỗi.
- **Phối hợp nhóm:** Thiết kế contract và schema chuẩn xác, tạo điều kiện cho member tích hợp, không xảy ra quá nhiều xung đột.
- **Tư duy lập trình phòng vệ (Defensive Programming):** Tool cho LLM bắt buộc phải có guardrails (tự ép kiểu, kẹp biên, chuẩn hóa lỗi về dạng dict `{"error": ...}`) để xử lý input sai lệch từ model mà không làm gãy vòng lặp Agent.
- **Mocking & Unit Test cô lập:** Sử dụng `pytest` kết hợp `fake_http` giúp kiểm thử toàn bộ lỗi biên và sự cố mạng (503, Timeout) nhanh chóng, ổn định mà không cần gọi API thật.
- **Tư duy Contract-First:** Chốt sớm schema và tài liệu `TOOL.md` là chìa khóa để 3 người làm việc song song, độc lập và tối ưu tiến độ.
