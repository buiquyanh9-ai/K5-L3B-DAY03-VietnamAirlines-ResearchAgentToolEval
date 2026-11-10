# Báo cáo nhóm — Day 03 Research Agent Tool Eval

> Báo cáo gồm 2 phần có hạn khác nhau:
> - **Phần A (mục 2)** — giới thiệu agent, ngắn gọn 1 trang. **Xong trước Team showdown (16:30)** để team khác hiểu nhanh agent có tool gì, làm được gì. Có thể làm thêm poster `report/team/poster.html` hoặc `poster.svg`.
> - **Phần B (mục 3–7)** — chi tiết và bằng chứng, dựa trên log thật. Hoàn thiện trước deadline nộp bài.
>
> Mỗi bảng phải trỏ được tới file thật: run JSON, transcript, commit. Cách chấm xem [RUBRIC.md](../../RUBRIC.md).

## 1. Thông tin nhóm

- Tên nhóm: VietnamAirlines
- Thành viên và phân công: xem [TEAM.md](../../TEAM.md)
- Provider/model dùng cho v0–v3: OpenRouter / `openai/gpt-4o-mini` (model mặc định của provider)

## 2. Mục tiêu và cách tiếp cận — PHẦN A: Giới thiệu agent

### A1. Agent này làm được gì

> 1–2 câu mô tả agent dùng để làm gì (cho team khác hiểu nhanh).

Ví dụ: "Research agent: tìm tin theo từ khóa / theo tài khoản, đọc URL, tổng hợp thành digest, và gửi lên Telegram khi được xác nhận."

**Cách chạy UI:**

> Lệnh chạy UI (ví dụ `streamlit run app.py`) và dependency đã thêm vào `starter_v0/requirements.txt`.

**Link dùng thử (deploy):**

> Dán link public để team khác mở thử ngay. Cách deploy nhanh bằng Cloudflare Tunnel xem README. Nếu deploy Vercel/Streamlit Cloud thì dán link đó.
>
> URL:

### A2. Tool agent có

> Liệt kê các tool agent đang dùng (gồm tool mới nhóm tự thêm). Mỗi tool 1 dòng: tên + làm được gì.

| Tên tool | Làm được gì | Tool mới nhóm thêm? |
|---|---|---|
| clarify | hỏi lại người dùng khi thiếu thông tin | không |
|  |  |  |
|  |  |  |

### A3. Câu hỏi mẫu để thử

> 3–5 câu hỏi/yêu cầu mẫu để team khác tự thử agent ngay.

1.
2.
3.

## 3. Giải pháp

> Tóm tắt các thay đổi chính trong `starter_v0/artifacts/system_prompt.md` và `starter_v0/artifacts/tools.yaml`, và tool mới nhóm viết (tên, làm gì, khi nào agent nên gọi).

-

## 4. Kết quả — PHẦN B: Chi tiết và bằng chứng

### B1. Version Evidence

Lấy từ `starter_v0/artifacts/version_log.csv` và `starter_v0/runs/*.json`. Chỉ dùng run có `provider_error_cases == 0` và `measured_cases == total_cases`.

| Version | Changed Artifact | Hypothesis | Metric Before | Metric After | Run File |
|---|---|---|---:|---:|---|
| v0 | baseline (`v0+peb1c8179815b+te69bc53ed884`) | Đo hành vi chưa tối ưu trước khi sửa | — | case 0.65 · routing 0.75 · args 0.65 · multiturn 1.00 | [v0_B_base_openrouter_20261110T171017818123.json](../../starter_v0/runs/v0_B_base_openrouter_20261110T171017818123.json) |
| v1 | `system_prompt.md` (`v1+p962dbad29898+te69bc53ed884`) | Các chỉ dẫn xấu của starter (đoán thay vì hỏi, gửi không cần xác nhận, luôn gọi một tool) gây lỗi missing_info / wrong_boundary / out_of_scope | case 0.65 · routing 0.75 · args 0.65 · multiturn 1.00 | case 0.85 · routing 0.95 · args 0.85 · multiturn 1.00 | [v1_B_base_openrouter_20261110T181806903038.json](../../starter_v0/runs/v1_B_base_openrouter_20261110T181806903038.json) |
| v2 | `tools.yaml`, khai báo `clarify` (`v2+p962dbad29898+t05e5e8588f27`) | Khai báo `clarify` mơ hồ ("Gửi một câu hỏi", `response_type` không giải thích, không bắt buộc) nên model bỏ trống hoặc chọn sai `response_type`, và vẫn đoán thay vì hỏi | case 0.85 · routing 0.95 · args 0.85 · multiturn 1.00 | case 0.95 · routing 1.00 · args 0.95 · multiturn 1.00 | [v2_B_base_openrouter_20261110T183120055417.json](../../starter_v0/runs/v2_B_base_openrouter_20261110T183120055417.json) |
| v3 |  |  |  |  |  |

**Ghi chú v1:** Sửa được R03, R08, R13, R14. Còn 3 case FAIL: R10 (`timeline(screenname="Twitter")`: câu "try to infer from context first" vẫn khiến agent đoán), R11 và R12 (`clarify` không truyền `response_type`, hoặc truyền sai kiểu thay vì `yes_no`). Đây là bằng chứng cho giả thuyết v2.

**Ghi chú v2:** Chỉ sửa khối `clarify` trong `tools.yaml`; prompt giữ nguyên (prompt hash không đổi). R10 và R11 PASS: cả hai gọi `clarify(response_type="text")`, R10 không còn đoán `screenname="Twitter"`. Còn 1 case FAIL: R12. Agent vẫn hỏi nội dung bản tin bằng `response_type="text"` thay vì xin xác nhận `yes_no`, tức là ranh giới xác nhận của `send` chưa được khai báo rõ. Đây là bằng chứng cho giả thuyết v3.

### B2. Failure Analysis

Lấy từ `results[*].result.failures` trong run JSON.

Run v0: 13/20 PASS, 7 FAIL, `provider_error_cases = 0`, `measured_cases = total_cases = 20`. Toàn bộ 6 case multi-turn đều PASS; cả 7 case FAIL là single turn.

| Case ID | Failure Type | Actual Tool Calls | What Failed | Fix |
|---|---|---|---|---|
| R03_web_news_routing | `wrong_arg_value` | `lookup(query="AI news", topic="news", timeframe="day")` | Chọn đúng tool và đúng `topic`/`timeframe`, nhưng nhét chữ "news" vào `query`: `expected 'AI', got 'AI news'` | `tools.yaml`: mô tả `query` của `lookup` chỉ chứa chủ đề cốt lõi; ý "tin tức / hôm nay" đã thể hiện qua `topic` và `timeframe` |
| R08_out_of_scope | `out_of_scope` | `send(text="Nguyên hàm của x^2 là …")` | Câu toán ngoài phạm vi research, nhưng agent tự giải rồi dùng `send` làm kênh trả lời (tool trả `needs_confirmation` nên không gửi thật) | Prompt: định nghĩa phạm vi; ngoài phạm vi thì không gọi tool, từ chối và định hướng lại. Bỏ dòng "always … pick one tool" |
| R10_missing_handle | `missing_info` | `timeline(screenname="sama")` | Không nói của ai, agent tự đoán Sam Altman, làm đúng theo chỉ dẫn xấu "pick a well-known account like Sam Altman" | Prompt: bỏ chỉ dẫn đoán; thiếu tài khoản thì gọi `clarify(response_type="text")` |
| R11_missing_url | `missing_info` | `fetch(url="https://example.com/article")` | "Bài viết này" nhưng không có link, agent bịa URL theo chỉ dẫn "assume a likely URL" | Prompt: bỏ chỉ dẫn đoán URL; thiếu URL thì gọi `clarify` |
| R12_confirm_before_send | `wrong_boundary` | `send(text="Bản tin này đã được đăng lên Telegram.")` | Gửi ngay, không xin xác nhận, nội dung bịa; làm theo chỉ dẫn "just go ahead and do it" | Prompt và `tools.yaml`: trước mọi hành động gửi phải gọi `clarify(response_type="yes_no")`; chỉ gọi `send(confirmed=true)` sau khi user đồng ý |
| R13_parallel_web_and_tweets | `wrong_arg_value` | `lookup(query="AI news", timeframe="day")` + `social_search(query="AI", search_type="Latest", limit=5)` | Gọi đủ 2 tool, nhưng `lookup` thừa "news" trong `query` và thiếu `topic="news"` | `tools.yaml`: quy ước "tin tức/thời sự thì `topic=news`", `query` không chứa từ "news" |
| R14_out_of_scope_coding | `out_of_scope` | `send(text="def fibonacci(n): …")` | Yêu cầu viết code ngoài phạm vi, agent viết code rồi gọi `send` | Giống R08 |

**Nhận xét nguyên nhân gốc:**

- **5/7 lỗi (R08, R10, R11, R12, R14) do `system_prompt.md`:** 3 case làm theo đúng chỉ dẫn xấu của starter ("đoán thay vì hỏi", "gửi ngay"). 2 case out-of-scope do dòng "Always finish … Pick one tool" ép model phải gọi tool.
- **2/7 lỗi (R03, R13) do `tools.yaml`:** khai báo `lookup` không nói quy ước cho `query`/`topic`, nên model tự thêm "news" vào query và có lúc quên `topic`.
- **Pattern đáng chú ý:** 3/7 case FAIL gọi `send` dù user không hề yêu cầu gửi. Model dùng `send` như kênh "trả lời user", vì description chỉ ghi "Gửi một đoạn văn bản đi." cộng với áp lực phải gọi một tool. Guardrail trong code (`needs_confirmation`) đã chặn việc gửi thật, nhưng eval vẫn tính là lỗi.

### B3. Team Eval Cases

Liệt kê đúng 10 case trong `starter_v0/data/eval_group.json` (5 single turn + 5 multi turn).

| Case ID | What It Tests | Expected Tool/Behavior | Result |
|---|---|---|---|
|  |  |  |  |

### B4. Live Chat Evidence

Lấy từ `starter_v0/transcripts/*.transcript.json`.

| Turn | User Request | Tool Calls | Version Evidence | Outcome |
|---|---|---|---|---|
|  |  |  |  |  |

### B5a. Required Evidence — Tool mới, unit test, UI

| Item | Evidence File | What Worked | Risk / Guardrail |
|---|---|---|---|
| Tool mới (`tools/<tên>/`) |  |  |  |
| Unit test tool mới (≥ 3 test/tool) | `pytest` output (0 failed) |  |  |
| UI (lệnh chạy + link dùng thử) |  |  |  |

Tool unit tests: số test đã viết, và một ví dụ lỗi mà unit test bắt được nhưng eval không bắt được.

### B5. Bonus Evidence

Chỉ điền nếu nhóm làm bonus (ghi riêng, tối đa 10 điểm). Tool có sẵn (`send`, `policy`, `papers`, `paper_text`) không tự được bonus.

| Bonus | Evidence File | What Worked | Risk / Guardrail |
|---|---|---|---|
| Small Local Model | xem B7 |  |  |
| Hơn 3 tool mới (≥ 4) |  |  |  |
| `send` gửi thật lên Telegram sau xác nhận | transcript |  |  |
| Test challenge (0 skipped / regression test) | `pytest` output |  |  |

Test challenge: số bug tìm được trong tool có sẵn (nếu có), cách sửa, và test regression tương ứng.

### B7. Small Local Model Challenge (bonus)

Chỉ điền nếu nhóm làm bonus này.

| Version | Model (provider) | Prompt/Tools | case_accuracy | tool_routing | argument | multiturn | Run File |
|---|---|---|---|---|---|---|---|
| v3 | (cloud) | v3 |  |  |  |  |  |
| v3-<model> | (ollama) | v3 |  |  |  |  |  |
| v3-<model> | (ollama) | v3 |  |  |  |  |  |
| v4-local |  |  |  |  |  |  |  |
| v5-local |  |  |  |  |  |  |  |

Lỗi đặc thù của model nhỏ (đếm từ run JSON):

| Failure Pattern | Count | Example Case | Fix Tried | Helped? |
|---|---|---|---|---|
| wrong / hallucinated tool |  |  |  |  |
| invalid JSON args (`_invalid_json_arguments`) |  |  |  |  |
| no tool call / answered directly |  |  |  |  |
| missed `clarify` |  |  |  |  |
| repeated / unnecessary calls |  |  |  |  |

- Cái gì giúp model nhỏ gọi tool đúng hơn nhất? Bằng chứng?
- Bản prompt tối ưu cho local chạy trên model cloud thì sao?
- Khi nào nhóm sẽ chọn model local thay vì cloud cho agent này?

## 5. Khó khăn và cách xử lý

> Khó khăn chính và cách nhóm xử lý. Nếu gặp lỗi kỹ thuật (provider lỗi, hết quota API, tool không chạy), mô tả lỗi và dẫn bằng chứng: run JSON, log, ảnh chụp.

-

## 6. Tổng hợp đóng góp

Chi tiết đóng góp của từng thành viên nằm trong [TEAM.md](../../TEAM.md) và các báo cáo cá nhân `report/team/MSSV_HoTen.md`.

## 7. Hạn chế và hướng cải thiện — B6. Reflection

- Fix nào thuộc `system_prompt.md`?
- Fix nào thuộc `tools.yaml`?
- Failure nào cần review thủ công thay vì chấm tự động?
- Nếu có thêm một vòng, nhóm sẽ thử giả thuyết nào?

## 8. Tài liệu tham khảo

-
