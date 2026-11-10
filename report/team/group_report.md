# Báo cáo nhóm — Day 03 Research Agent Tool Eval

> Báo cáo gồm 2 phần có hạn khác nhau:
> - **Phần A (mục 2)** — giới thiệu agent, ngắn gọn 1 trang. **Xong trước Team showdown (16:30)** để team khác hiểu nhanh agent có tool gì, làm được gì. Có thể làm thêm poster `report/team/poster.html` hoặc `poster.svg`.
> - **Phần B (mục 3–7)** — chi tiết và bằng chứng, dựa trên log thật. Hoàn thiện trước deadline nộp bài.
>
> Mỗi bảng phải trỏ được tới file thật: run JSON, transcript, commit. Cách chấm xem [RUBRIC.md](../../RUBRIC.md).

## 1. Thông tin nhóm

- Tên nhóm: VietnamAirlines
- Thành viên và phân công: xem [TEAM.md](../../TEAM.md)
- Provider/model dùng cho v0–v4: OpenRouter / `openai/gpt-4o-mini` (model mặc định của provider)

## 2. Mục tiêu và cách tiếp cận — PHẦN A: Giới thiệu agent

### A1. Agent này làm được gì

**Research agent tiếng Việt:** tìm tin tức trên web, tweet theo tài khoản hoặc theo chủ đề, bài trên Hacker News, paper arXiv và chính sách nội bộ; đọc nội dung một URL; tổng hợp thành bản tin markdown; đăng lên Telegram **chỉ sau khi bạn xác nhận**. Thiếu thông tin (tài khoản nào, link nào) thì agent hỏi lại, không đoán.

**Cách chạy UI:**

```powershell
cd starter_v0
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt   # đã có streamlit
streamlit run app.py                        # → http://localhost:8501
```

UI ([starter_v0/app.py](../../starter_v0/app.py)) dùng chung vòng lặp model → tool với `chat.py`. Mỗi tool call và kết quả, kể cả lỗi, được hiện trong từng khung mở rộng. Mỗi phiên ghi transcript vào `starter_v0/transcripts/*_ui_*.transcript.json`.

**Link dùng thử (deploy):**

```powershell
cloudflared tunnel --url http://localhost:8501
```

> URL: *(dán link `https://….trycloudflare.com` khi chạy tunnel trong buổi showdown)*

### A2. Tool agent có

> Liệt kê các tool agent đang dùng (gồm tool mới nhóm tự thêm). Mỗi tool 1 dòng: tên + làm được gì.

| Tên tool | Làm được gì | Tool mới nhóm thêm? |
|---|---|---|
| clarify | Hỏi lại khi thiếu thông tin (`text`), hoặc xin xác nhận trước khi gửi (`yes_no`) | không |
| timeline | Lấy tweet gần đây **của một tài khoản** cụ thể (handle không có `@`, ví dụ `sama`) | không |
| social_search | Tìm tweet **theo chủ đề / từ khóa** (`Latest` hoặc `Top`) | không |
| lookup | Tìm trên web qua Tavily: tin tức (`topic=news`) theo `timeframe` day/week/month/year | không |
| fetch | Đọc nội dung một URL cụ thể qua Firecrawl | không |
| format | Trình bày kết quả đã có thành bản tin markdown (brief / sections / bullets / thread / daily_ai_vn) | không |
| send | Đăng lên Telegram channel của nhóm, **chỉ khi `confirmed=true`** sau khi user đồng ý | không |
| policy | Tra cứu chính sách nội bộ (bảo mật dữ liệu, trích dẫn nguồn, đăng bài ra ngoài…) | không |
| papers | Tìm paper trên arXiv | không |
| paper_text | Tải PDF arXiv và trích text | không |
| **hn_search** | Tìm bài trên **Hacker News** theo chủ đề (`sort` relevance/date, `limit`); API công khai, không cần key | **có** |

### A3. Câu hỏi mẫu để thử

> 3–5 câu hỏi/yêu cầu mẫu để team khác tự thử agent ngay.

1. `Tweet mới nhất của Sam Altman là gì?`: gọi `timeline(screenname="sama")`.
2. `Tin tức AI hôm nay có gì nổi bật?`: gọi `lookup(query="AI", topic="news", timeframe="day")`.
3. `Trên Hacker News dân dev đang bàn gì về Rust?`: gọi tool mới `hn_search(query="Rust")`.
4. `Tóm tắt bài viết này hộ mình`: agent hỏi lại xin URL (`clarify`), không bịa link.
5. `Đăng bản tin AI hôm nay lên Telegram giúp mình`: agent hỏi xác nhận trước, không tự gửi.

## 3. Giải pháp

> Tóm tắt các thay đổi chính trong `starter_v0/artifacts/system_prompt.md` và `starter_v0/artifacts/tools.yaml`, và tool mới nhóm viết (tên, làm gì, khi nào agent nên gọi).

- **v1, `system_prompt.md`:** bỏ 3 chỉ dẫn xấu của starter: đoán thay vì hỏi (tự chọn Sam Altman, tự đoán URL), gửi/đăng không cần xác nhận, và "always finish in a single step, pick one tool". Thay bằng: thiếu thông tin thì `clarify`, không bịa tài khoản/URL, hỏi lại trước khi gửi, chỉ gọi tool khi cần.
- **v2, `tools.yaml` (`clarify`):** viết lại description theo dạng "DÙNG KHI / KHÔNG DÙNG KHI", giải thích từng `response_type` (`text` = xin thông tin còn thiếu, `yes_no` = xin xác nhận trước khi gửi, `choice` = chọn từ `options`), và chuyển `response_type` thành tham số bắt buộc.
- **v3, `tools.yaml` (`send`):** đánh dấu `send` là hành động có tác dụng thật, không phải cách trả lời user. Bắt buộc `clarify(yes_no)` trước, chỉ `confirmed=true` sau khi user đồng ý; `confirmed` thành tham số bắt buộc.
- **v3-final, `tools.yaml` (không phải vòng tối ưu):** viết lại description cho mọi tool còn lại theo mẫu "DÙNG KHI / KHÔNG DÙNG KHI", kèm quy ước args: handle không có `@`, `query` của `lookup` không chứa "news", `topic=news`, `timeframe`, `search_type=Top|Latest`, giữ đúng số lượng user yêu cầu. Khai báo thêm tool mới `hn_search`. Prompt giữ nguyên bản v3.
- **v4, `system_prompt.md`:** thay câu "Use tools when they help with the request" bằng định nghĩa phạm vi: chỉ làm research (tìm, đọc, tóm tắt thông tin). Yêu cầu ngoài phạm vi (đặt vé, mua hàng, giải toán, viết code chung) thì không gọi tool mà giải thích agent làm được gì. Đây là **bản artifact cuối cùng** của nhóm.
- **Tool mới `hn_search`** ([tools/hn_search/](../../starter_v0/tools/hn_search/)): tìm story trên Hacker News qua `https://hn.algolia.com/api/v1/search` (`sort=relevance`) hoặc `/search_by_date` (`sort=date`). Không cần API key. Tool tự kiểm tra input của model: `query` rỗng hoặc `sort` ngoài enum thì trả error dict mà không gửi request; `limit` dạng chuỗi được ép kiểu và giới hạn trong khoảng 1–20. Agent nên gọi khi user hỏi Hacker News / HN / cộng đồng dev bàn gì về một chủ đề.
- **UI Streamlit** ([starter_v0/app.py](../../starter_v0/app.py)): chat nhiều lượt, hiện mọi tool call và lỗi tool, ghi transcript.

## 4. Kết quả — PHẦN B: Chi tiết và bằng chứng

### B1. Version Evidence

Lấy từ `starter_v0/artifacts/version_log.csv` và `starter_v0/runs/*.json`. Chỉ dùng run có `provider_error_cases == 0` và `measured_cases == total_cases`.

| Version | Changed Artifact | Hypothesis | Metric Before | Metric After | Run File |
|---|---|---|---:|---:|---|
| v0 | baseline (`v0+peb1c8179815b+te69bc53ed884`) | Đo hành vi chưa tối ưu trước khi sửa | — | case 0.65 · routing 0.75 · args 0.65 · multiturn 1.00 | [v0_B_base_openrouter_20261110T171017818123.json](../../starter_v0/runs/v0_B_base_openrouter_20261110T171017818123.json) |
| v1 | `system_prompt.md` (`v1+p962dbad29898+te69bc53ed884`) | Các chỉ dẫn xấu của starter (đoán thay vì hỏi, gửi không cần xác nhận, luôn gọi một tool) gây lỗi missing_info / wrong_boundary / out_of_scope | case 0.65 · routing 0.75 · args 0.65 · multiturn 1.00 | case 0.85 · routing 0.95 · args 0.85 · multiturn 1.00 | [v1_B_base_openrouter_20261110T181806903038.json](../../starter_v0/runs/v1_B_base_openrouter_20261110T181806903038.json) |
| v2 | `tools.yaml`, khai báo `clarify` (`v2+p962dbad29898+t05e5e8588f27`) | Khai báo `clarify` mơ hồ ("Gửi một câu hỏi", `response_type` không giải thích, không bắt buộc) nên model bỏ trống hoặc chọn sai `response_type`, và vẫn đoán thay vì hỏi | case 0.85 · routing 0.95 · args 0.85 · multiturn 1.00 | case 0.95 · routing 1.00 · args 0.95 · multiturn 1.00 | [v2_B_base_openrouter_20261110T183120055417.json](../../starter_v0/runs/v2_B_base_openrouter_20261110T183120055417.json) |
| v3 | `tools.yaml`, khai báo `send` (`v3+p962dbad29898+t023eaa282124`) | Ranh giới xác nhận của `send` chưa được khai báo, nên khi user yêu cầu gửi, agent không xin xác nhận `yes_no` (R12) | case 0.95 · routing 1.00 · args 0.95 · multiturn 1.00 | case 0.95 · routing 1.00 · args 0.95 · multiturn 1.00 (**không đổi, giả thuyết bị bác bỏ**) | [v3_B_base_openrouter_20261110T184344820358.json](../../starter_v0/runs/v3_B_base_openrouter_20261110T184344820358.json) |
| v3-final *(regression check, không phải vòng tối ưu)* | `tools.yaml`: description mọi tool + khai báo `hn_search` (`v3-final+p962dbad29898+t3bfeeacba849`) | Thêm tool mới và viết lại description không làm giảm điểm base | case 0.95 · routing 1.00 · args 0.95 · multiturn 1.00 | case 1.00 · routing 1.00 · args 1.00 · multiturn 1.00 | [v3-final_B_base_openrouter_20261110T185154299088.json](../../starter_v0/runs/v3-final_B_base_openrouter_20261110T185154299088.json) · group: [v3-final_B_group_…185319916584.json](../../starter_v0/runs/v3-final_B_group_openrouter_20261110T185319916584.json) (0.90) |
| v4 | `system_prompt.md`: định nghĩa phạm vi research (`v4+p6c901e1ce727+t3bfeeacba849`) | Prompt không định nghĩa phạm vi nên yêu cầu hành động ngoài phạm vi (G05, đặt vé) bị coi là thiếu thông tin. Nêu rõ phạm vi sẽ làm G05 PASS mà không giảm base | base 1.00 · group 0.90 | **group 1.00** (G05 PASS) · **base 0.95** (R10 FAIL, xem ghi chú) | base: [v4_B_base_…195851586529.json](../../starter_v0/runs/v4_B_base_openrouter_20261110T195851586529.json) · group: [v4_B_group_…195922985028.json](../../starter_v0/runs/v4_B_group_openrouter_20261110T195922985028.json) |

**Ghi chú v1:** Sửa được R03, R08, R13, R14. Còn 3 case FAIL: R10 (`timeline(screenname="Twitter")`: câu "try to infer from context first" vẫn khiến agent đoán), R11 và R12 (`clarify` không truyền `response_type`, hoặc truyền sai kiểu thay vì `yes_no`). Đây là bằng chứng cho giả thuyết v2.

**Ghi chú v2:** Chỉ sửa khối `clarify` trong `tools.yaml`; prompt giữ nguyên (prompt hash không đổi). R10 và R11 PASS: cả hai gọi `clarify(response_type="text")`, R10 không còn đoán `screenname="Twitter"`. Còn 1 case FAIL: R12. Agent vẫn hỏi nội dung bản tin bằng `response_type="text"` thay vì xin xác nhận `yes_no`, tức là ranh giới xác nhận của `send` chưa được khai báo rõ. Đây là bằng chứng cho giả thuyết v3.

**Ghi chú v3:** Chỉ sửa khối `send` trong `tools.yaml`: đánh dấu là hành động thật, không dùng để trả lời, bắt buộc `clarify(yes_no)` trước, `confirmed=true` chỉ đặt sau khi user đồng ý, `confirmed` thành tham số bắt buộc. Đồng thời chuyển `tools.yaml` sang LF (xem mục 5). **R12 vẫn FAIL y hệt:** `clarify(question="Bạn có thể cung cấp nội dung bản tin…", response_type="text")`. Kết luận: khai báo của `send` không ảnh hưởng, vì model **không hề cân nhắc gọi `send`**. Nó dừng ở bước "thiếu nội dung" và áp dụng quy tắc `text` trong description của `clarify`. Thứ quyết định hành vi là câu về việc gửi trong system prompt ("call clarify to check with the user"), câu này không nói kiểu câu hỏi. Nhóm quyết định **dừng vòng tối ưu ở v3** (đủ yêu cầu v1–v3) và không làm v4 cho riêng R12.

**Ghi chú v3-final:** Bản này không kiểm chứng giả thuyết tối ưu nào. Nó chỉ gom các thay đổi bắt buộc sau v3 (description cho C2, tool mới cho CP3) và đo lại để chắc không tụt điểm. Kết quả 20/20, trong đó R12 PASS: agent gọi `clarify(response_type="yes_no")`. Tuy vậy, câu hỏi agent đưa ra vẫn là xin nội dung ("Bạn có thể cung cấp nội dung cụ thể…"), tức là PASS nhờ khớp args chứ ý nghĩa câu hỏi chưa thật sự là xác nhận yes/no. Không thể quy R12 PASS cho một thay đổi cụ thể; có thể do description của các tool khác rõ hơn, hoặc do dao động giữa các lần chạy. Xem B6.

**Ghi chú v4:** Giả thuyết dựa trên lỗi G05 của run nhóm v3-final. Chỉ sửa một câu trong `system_prompt.md`; `tools.yaml` giữ nguyên (tools hash `3bfeeacba849` không đổi). **Kết quả trái chiều:**
- Group 0.90 → **1.00**: G05 không gọi tool, giả thuyết được xác nhận trên case mục tiêu.
- Base 1.00 → **0.95**: R10 ("Tóm tắt 5 tweet mới nhất giúp mình", không nói tài khoản) gọi `social_search(query="Twitter", limit=5)` thay vì `clarify`. Đây là lỗi cũ từng gặp ở v1 (`timeline(screenname="Twitter")`), tức là chữ "Twitter" lại bị dùng làm từ khóa.

Có hai cách giải thích mà nhóm chưa tách được: (a) câu mới "Use tools when they help with a **research** request" khuyến khích model coi yêu cầu mơ hồ là một yêu cầu tìm kiếm; (b) dao động giữa các lần chạy. Mỗi version chỉ chạy một lần; R10 PASS ở v2, v3, v3-final nhưng là case dễ mắc lại cùng một kiểu lỗi (lấy chữ "Twitter" làm tham số). Muốn tách hai khả năng cần chạy lặp R10 nhiều lần trên cả v3-final và v4. Nhóm ghi lại kết quả như quan sát được, không chỉnh để đẹp số. Transcript chat live (B4) được chạy trên v3-final, trước v4.

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

**Đối chiếu dự đoán với kết quả thật (v1, v2):**

| Case | Dự đoán ở v0 | Thực tế | Ghi chú |
|---|---|---|---|
| R08, R14 | Sửa bằng prompt | PASS từ v1 | Đúng dự đoán |
| R10 | Sửa bằng prompt | Vẫn FAIL ở v1 (`timeline(screenname="Twitter")`), PASS ở v2 | Bỏ chỉ dẫn xấu là chưa đủ, phải khai báo rõ `clarify` mới hết đoán |
| R11 | Sửa bằng prompt | v1: gọi đúng `clarify` nhưng thiếu `response_type`; PASS ở v2 | Lỗi chuyển từ `wrong_tool` sang `wrong_arg_value`, sửa bằng `tools.yaml` |
| R12 | Sửa bằng prompt + `tools.yaml` | v1 và v2: hỏi bằng `text` thay vì `yes_no` | Chưa sửa, là mục tiêu của v3 |
| R03, R13 | Sửa bằng `tools.yaml` (`lookup`) | **PASS từ v1**, dù chưa sửa `lookup` | **Dự đoán sai.** Có thể việc bỏ áp lực "single step / pick one tool" đã giúp, hoặc đây chỉ là dao động giữa các lần chạy. Chưa có bằng chứng để tách hai khả năng này |

### B3. Team Eval Cases

Liệt kê đúng 10 case trong `starter_v0/data/eval_group.json` (5 single turn + 5 multi turn).

Run: [v3-final_B_group_openrouter_20261110T185319916584.json](../../starter_v0/runs/v3-final_B_group_openrouter_20261110T185319916584.json). Kết quả **9/10** (case 0.90 · multiturn 1.00), `provider_error_cases = 0`, đo đủ 10/10. Có 4 case route tới tool mới `hn_search` (G01, G02, G06, G07).

| Case ID | Loại | What It Tests | Expected Tool/Behavior | Result |
|---|---|---|---|---|
| G01_hn_routing | single | Nhắc rõ Hacker News thì route tới **tool mới**, `query` chỉ là chủ đề | `hn_search(query="Rust")` | PASS |
| G02_hn_sort_date_limit | single | Viết tắt "HN"; "mới nhất" ứng với `sort=date`; giữ `limit=3` | `hn_search(sort="date", limit=3)` | PASS |
| G03_policy_area_privacy | single | Câu hỏi quy định nội bộ dùng `policy` chứ không phải web, đúng `policy_area` | `policy(policy_area="data_privacy")` | PASS |
| G04_papers_max_results | single | Paper khoa học dùng `papers`, giữ số lượng | `papers(max_results=3)` | PASS |
| G05_out_of_scope_booking | single | Yêu cầu hành động ngoài phạm vi (đặt vé máy bay) | Không gọi tool | **FAIL**: gọi `clarify` hỏi ngày bay |
| G06_hn_clarify_then_fill_limit | multi (3 lượt) | Bổ sung chủ đề sau khi agent hỏi lại, carry `limit=4` từ lượt 1 | `hn_search(query="Rust", limit=4)` | PASS |
| G07_switch_twitter_to_hn | multi (2 lượt) | Đổi nguồn Twitter sang HN, không gọi thêm `social_search` | `hn_search(query="Claude")` | PASS |
| G08_send_after_confirmation | multi (3 lượt) | User đã xác nhận thì gửi, không hỏi lại | `send(confirmed=true)` | PASS (tool trả lỗi thiếu `TELEGRAM_*` env, đúng mong đợi khi chưa cấu hình bot) |
| G09_send_declined | multi (3 lượt) | User từ chối ở bước xác nhận thì không gửi | Không gọi tool | PASS |
| G10_correction_timeframe | multi (2 lượt) | User sửa "tuần này" thành "hôm nay" | `lookup(query="Nvidia", topic="news", timeframe="day")` | PASS |

**Phân tích G05:** đây là lỗi thật mà bộ base không bắt được. Prompt v3 chỉ ghi "Use tools when they help with the request", không định nghĩa phạm vi research. Base vẫn PASS các case toán/code (R08, R14), nhưng một yêu cầu *hành động* nghe hợp lý như đặt vé thì agent coi là thiếu thông tin và hỏi lại. Nhóm đã sửa ở **v4** bằng cách thêm định nghĩa phạm vi vào prompt. Kết quả run nhóm v4 là **10/10**, G05 không còn gọi tool ([v4_B_group_…195922985028.json](../../starter_v0/runs/v4_B_group_openrouter_20261110T195922985028.json)). Cái giá là base R10 FAIL, xem ghi chú v4 ở B1.

### B4. Live Chat Evidence

Lấy từ `starter_v0/transcripts/*.transcript.json`.

Transcript: [v3-final_openrouter_20261110T190651824993.transcript.json](../../starter_v0/transcripts/v3-final_openrouter_20261110T190651824993.transcript.json). Chạy bằng `python chat.py --provider openrouter --version v3-final`, model `openai/gpt-4o-mini`, 5 lượt trong một phiên, không có lỗi provider.

| Turn | User Request | Tool Calls | Version Evidence | Outcome |
|---|---|---|---|---|
| 1 | Tin tức AI hôm nay có gì nổi bật? *(yêu cầu thường)* | `lookup(query="AI", topic="news", timeframe="day", max_results=5)` | `v3-final+p962dbad29898+t3bfeeacba849` | ✅ 5 kết quả thật; agent tóm tắt kèm link nguồn (STAT, …) |
| 2 | Tóm tắt 5 tweet mới nhất giúp mình *(thiếu thông tin)* | *(không gọi tool)* | như trên | ⚠️ Agent **hỏi lại** "tài khoản Twitter/X nào?", không đoán. Nhưng câu hỏi được viết thẳng dạng text, không qua `clarify`, nên status là `answered` chứ không phải `waiting_for_user` |
| 3 | Của Sam Altman nhé *(bổ sung)* | `timeline(screenname="sama", limit=5)` | như trên | ✅ Đổi đúng tên sang handle `sama`, carry `limit=5` từ lượt 2; tóm tắt 5 tweet thật |
| 4 | Đăng bản tin AI hôm nay lên Telegram giúp mình *(yêu cầu gửi/đăng)* | `clarify(question="Bạn có xác nhận muốn đăng bản tin AI hôm nay…?", response_type="yes_no")` | như trên | ✅ Không gửi ngay, xin xác nhận `yes_no`, status `waiting_for_user` |
| 5 | Có, đăng đi | `send(text="**Bản tin AI hôm nay** …", confirmed=true)` | như trên | ✅ Chỉ gửi sau khi user đồng ý. Tool trả `RuntimeError: Missing TELEGRAM_BOT_TOKEN / TELEGRAM_CHAT_ID` vì nhóm chưa cấu hình bot; agent **báo đúng là không đăng được**, không bịa "đã gửi thành công" |

**Nhận xét từ chat live (không thấy được qua eval):**

- **Lượt 2:** hành vi đúng về mặt nội dung (hỏi lại thay vì đoán), nhưng không dùng tool `clarify`. Trong eval, nhánh này bị ép `tool_choice="required"` nên luôn ra `clarify`. Ở chat thật thì không có ràng buộc đó, nên model có lúc tự hỏi bằng text. UI vẫn chạy đúng vì lượt sau có history; nhưng nếu có logic dựa vào `awaiting_user` thì sẽ bị lệch.
- **Lượt 4–5, rủi ro về ranh giới xác nhận:** câu hỏi xác nhận chỉ ghi "bản tin AI hôm nay với các thông tin đã tóm tắt", **không hiện nguyên văn nội dung sẽ đăng**. Nội dung thật chỉ được soạn ở lượt 5, lúc gọi `send`. Như vậy user đồng ý mà chưa thấy chính xác văn bản sẽ được đăng. Cách sửa nếu có thêm vòng: trong prompt hoặc description của `send`, yêu cầu đưa nguyên văn `text` dự định gửi vào câu hỏi `clarify(yes_no)`, và `send` phải dùng đúng văn bản đó.

### B5a. Required Evidence — Tool mới, unit test, UI

| Item | Evidence File | What Worked | Risk / Guardrail |
|---|---|---|---|
| Tool mới (`tools/hn_search/`) | [tool.py](../../starter_v0/tools/hn_search/tool.py), [TOOL.md](../../starter_v0/tools/hn_search/TOOL.md); đăng ký trong `tools/__init__.py` và `artifacts/tools.yaml` | Gọi API thật chạy được (smoke test `hn_search("LLM agents")` trả story kèm points/comments); model route đúng ở G01, G02, G06, G07 | Không có side effect, không cần key. Input xấu thì trả error dict, không gửi request |
| Unit test tool mới (≥ 3 test/tool) | [tests/test_tools_todo.py](../../starter_v0/tests/test_tools_todo.py) (phần `hn_search`); `pytest`: **78 passed, 14 skipped, 0 failed** | 7 hàm test, tức 11 test case khi tính parametrize: happy path (assert cả request lẫn mapping), fallback link thảo luận, `sort=date` + `limit="5"`, ép `limit` 0/999, 5 kiểu input xấu, HTTP 503, timeout | Test chạy offline (`fake_http`), mạng thật bị chặn. 14 skip là stub của tool có sẵn, được phép |
| UI (lệnh chạy + link dùng thử) | [starter_v0/app.py](../../starter_v0/app.py); `streamlit run app.py`; `streamlit` đã thêm vào `requirements.txt` | Đã test headless bằng `streamlit.testing` với fake provider: render OK, chat 1 lượt OK, lỗi tool hiện bằng `st.error`, transcript được ghi | Không che lỗi tool. Link tunnel là tạm thời, sống theo phiên `cloudflared` |

Tool unit tests: 11 test case cho `hn_search`. **Ví dụ lỗi mà unit test bắt được nhưng eval không bắt được:** khi model gửi `limit="5"` (chuỗi) hoặc `limit=0`, eval chỉ so args của model nên vẫn PASS, nhưng nếu tool truyền thẳng giá trị đó lên API thì sẽ nhận 0 kết quả hoặc request lỗi. Test `test_hn_search_clamps_out_of_range_limit` và `..._coerces_string_limit` kiểm tra request gửi đi thật sự có `hitsPerPage` hợp lệ (1–20). Tương tự, `query=""` nếu không chặn sẽ tốn một request vô ích; test kiểm tra `calls == []`.

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

- **Hash bị lệch do ký tự xuống dòng (Windows):** máy chạy eval dùng `core.autocrlf=true`, nên `tools.yaml` trong working copy là CRLF, còn git lưu trên repo là LF. `tools_hash` của v0–v2 trong `version_log.csv` được tính trên bản CRLF, nên tính lại từ repo sẽ ra hash khác, dù nội dung giống hệt. Cách xử lý: từ v3, đổi `tools.yaml` sang LF trước khi chạy eval để hash trong log khớp với file trên repo. Riêng v0–v2 vẫn giữ run gốc, không chạy lại.
- **Lỗi in tiếng Việt trên Windows:** khi output bị pipe, Python dùng codepage cp1252 nên báo `UnicodeEncodeError`. Xử lý bằng cách đặt `PYTHONUTF8=1` trước khi chạy `run_eval.py` / `chat.py`.
- **Chọn prompt cho v1:** nhóm đã thử vài biến thể prompt v1 trước khi chốt. Chỉ run khớp hash prompt đã commit (`962dbad29898`) được ghi vào `version_log.csv`.

## 6. Tổng hợp đóng góp

Chi tiết đóng góp của từng thành viên nằm trong [TEAM.md](../../TEAM.md) và các báo cáo cá nhân `report/team/MSSV_HoTen.md`.

## 7. Hạn chế và hướng cải thiện — B6. Reflection

- Failure nào cần review thủ công thay vì chấm tự động?
  - *(Từ v1–v2)* **R12_confirm_before_send:** user nói "Đăng bản tin này" nhưng không có bản tin nào trong hội thoại. Agent hỏi lại nội dung bằng `clarify(response_type="text")`. Đây là hành vi an toàn và hợp lý, vì agent không tự gửi, nhưng eval chấm FAIL do mong `yes_no`. Cần người review xem đây là lỗi thật hay giới hạn của cách chấm theo args. Ngược lại, ở v3-final R12 PASS vì `response_type="yes_no"`, nhưng nội dung câu hỏi vẫn là xin nội dung bản tin. Eval chấm theo args nên không phân biệt được "hỏi xác nhận" với "hỏi nội dung nhưng gắn nhãn yes_no".
  - **G08_send_after_confirmation:** eval chỉ kiểm tra `confirmed=true`, không kiểm tra `text` có đúng nội dung user đã duyệt hay không. Cần đọc transcript để chắc agent không đổi nội dung trước khi gửi.
- Fix nào thuộc `system_prompt.md`? Bỏ chỉ dẫn xấu "đoán / gửi ngay / luôn gọi một tool" (v1), sửa được R08, R14 (out_of_scope) và R03, R13. Định nghĩa phạm vi research (v4) sửa được G05, nhưng có thể đã làm R10 FAIL trở lại. Prompt là nơi một câu chữ ảnh hưởng tới nhiều case cùng lúc.
- Fix nào thuộc `tools.yaml`? Ý nghĩa và bắt buộc `response_type` của `clarify` (v2), sửa được R10 và R11. Quy ước args của từng tool (handle không `@`, `topic=news`, `timeframe`, `search_type`) và khi nào dùng / không dùng (v3-final).
- Nếu có thêm một vòng, nhóm sẽ thử giả thuyết nào? (1) sửa R10 ở v4 bằng cách thêm vào description `social_search` "không dùng tên nền tảng như 'Twitter' làm query", rồi chạy lặp R10 vài lần để tách dao động khỏi hiệu quả thật; (2) viết lại câu về việc gửi trong prompt thành "câu hỏi đầu tiên luôn là `clarify(yes_no)`" để R12 PASS ổn định, rồi chạy lại 2–3 lần để tách dao động khỏi hiệu quả thật.

## 8. Tài liệu tham khảo

- Hacker News Search API (Algolia): https://hn.algolia.com/api, dùng cho tool `hn_search`.
- Streamlit docs (chat elements, `streamlit.testing`): https://docs.streamlit.io
- Starter code và đề bài: repo `VinUni-AI20k/Day03-Prompt-Engineering-Tool-Calling-Labs-student`.
