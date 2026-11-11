# Báo cáo cá nhân — HoVaTen-MSSV

> Đổi tên file thành `MSSV_HoTen.md` (ví dụ `20241234_NguyenVanAn.md`) và điền mục 1 trước khi nộp.

## 1. Thông tin thành viên

- Họ tên: Bùi Đình Quý Anh
- MSSV: 2A202603969
- Email: buiquyanh9@gmail.com
- GitHub: https://github.com/buiquyanh9-ai

## 2. Phần việc phụ trách

- Setup môi trường và API key cho cả nhóm; quản lý repo nộp bài.
- Chạy baseline v0 và vòng tối ưu v1–v4 (prompt + tool declaration), ghi `version_log.csv`.
- Điều phối việc dùng AI (Claude Code) để viết tool mới, unit test, eval case nhóm, UI và báo cáo nhóm; review và kiểm tra lại kết quả.
- Chạy chat live và demo UI.

## 3. Đóng góp cụ thể

**Tự thực hiện:**

- Lấy và cấu hình key OpenRouter / Tavily / Firecrawl / RapidAPI trong `starter_v0/.env` (không commit).
- Chạy baseline v0 (`runs/v0_B_base_openrouter_20261110T171017818123.json`, 0.65).
- **v1:** tự viết và thử nhiều biến thể `system_prompt.md` (5 lần chạy, 4 bản prompt), chốt bản bỏ 3 chỉ dẫn xấu của starter (prompt hash `962dbad29898`, 0.65 → 0.85); chỉ giữ run khớp hash đã commit.
- Quyết định quy trình: dừng vòng tối ưu ở v3, gom thay đổi bắt buộc vào `v3-final`, sau đó thêm v4 dựa trên lỗi G05 của run nhóm.
- Chạy chat live 5 lượt bằng `chat.py` (`transcripts/v3-final_openrouter_20261110T190651824993.transcript.json`) đủ 3 tình huống: yêu cầu thường, thiếu thông tin rồi bổ sung, yêu cầu đăng Telegram.
- Chạy UI Streamlit trong buổi lab cho coach thử (`transcripts/v4_openrouter_ui_20261110T204527398264.transcript.json`).
- Tạo / quản lý repo GitHub nộp bài, push code, mời thành viên.

**Thực hiện cùng AI (Claude Code), mình review và kiểm tra:**

- Phân tích lỗi v0 (bảng B2) và các giả thuyết v2 (`clarify`), v3 (`send`), v4 (phạm vi research).
- Tool mới `hn_search` (`starter_v0/tools/hn_search/`) + 11 unit test (`tests/test_tools_todo.py`).
- Viết lại description mọi tool trong `tools.yaml` (v3-final).
- 10 eval case nhóm (`data/eval_group.json`).
- UI Streamlit (`starter_v0/app.py`).
- Phần lớn nội dung `report/team/group_report.md`.

## 4. Bằng chứng

- File/commit/PR:
  - Commit `a892fc3` (CP1 baseline v0), `a4b70f1` (v1), `461aec4` (v2), `32b00e8` (v3), `b27837a` (tool mới + test + eval nhóm + UI), `5d32c0b` (v4), `4c3d571` (transcript chat live).
  - `starter_v0/artifacts/version_log.csv` (v0 → v4), `starter_v0/runs/*.json` (8 run hợp lệ).
- AI/công cụ đã dùng và cách tự kiểm tra kết quả:
  - **Claude Code (Claude Opus 5.5) trong VS Code**: dùng để giải thích đề, phân tích run JSON, viết code tool mới, unit test, eval case, UI và soạn báo cáo. Các commit có dòng `Co-Authored-By: Claude` là phần AI hỗ trợ.
  - **Cách tự kiểm tra:** chạy `pytest` (78 passed, 0 failed); mỗi version đều chạy eval thật và đối chiếu hash + metric trong `version_log.csv` với run JSON; tự chạy chat live và UI để xem agent hành xử thật; đọc lại từng case FAIL trong run JSON trước khi chấp nhận giả thuyết; kiểm tra `runs/` và `transcripts/` không lộ API key trước khi commit.

## 5. Tự đánh giá

- Điểm làm tốt: chạy đủ v0–v4 bằng API thật, mỗi version một giả thuyết, ghi trung thực cả version không tăng điểm (v3) và version làm tụt một case (v4 – R10).
- Điều học được: sửa prompt ảnh hưởng nhiều case cùng lúc (v4 sửa G05 nhưng R10 FAIL lại); eval chấm theo args không phân biệt được "hỏi xác nhận" với "hỏi nội dung gắn nhãn yes_no" (R12).
- Hạn chế: phần lớn code (tool mới, test, UI) được viết cùng AI — cần tự đọc lại để giải thích được khi coach hỏi; chưa làm bonus (Telegram thật, model local).
