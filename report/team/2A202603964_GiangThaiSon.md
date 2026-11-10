# Báo cáo cá nhân — Người 3: Eval Dataset & Reporting

> Vai trò Người 3 đã được tách khỏi phần xây dựng UI. UI, kiểm thử giao diện, tunnel/deploy và link dùng thử thuộc trách nhiệm riêng của Người 4.

---

## 1. Thông tin thành viên

- Họ tên: Giang Thái Sơn
- MSSV: 2A202603964
- Email: giangson309@gmail.com
- GitHub: son309

---

## 2. Phần việc phụ trách

- **Eval Dataset (CP4):** thiết kế và rà soát đúng 10 case trong `starter_v0/data/eval_group.json`, gồm 5 single-turn và 5 multi-turn.
- Bảo đảm mỗi case có `failure_type`, `expect`, `metadata.what_it_tests` và có case kiểm tra khả năng route tới tool mới `hn_search`.
- Chạy hoặc đối chiếu group eval, kiểm tra `provider_error_cases == 0`, `measured_cases == total_cases` và phân tích các case FAIL trước khi chấp nhận kết quả.
- **Reporting (phần báo cáo của CP5):** tổng hợp bằng chứng group eval, live chat, giới hạn của agent và reflection vào `report/team/group_report.md`.
- Rà soát báo cáo nhóm để số liệu trong bảng khớp với `runs/*.json`, `transcripts/*.transcript.json` và `artifacts/version_log.csv`.
- Phối hợp với Người 4 bằng cách bàn giao câu hỏi mẫu, tình huống demo và yêu cầu bằng chứng; không phụ trách code Streamlit, kiểm thử UI hoặc tunnel/deploy.

---

## 3. Đóng góp cụ thể

### 3.1. Bộ eval nhóm

- Hoàn thiện cấu trúc bộ eval nhóm gồm đúng **10 case: 5 single-turn và 5 multi-turn**.
- Phủ các nhóm lỗi quan trọng:
  - `wrong_tool`: phân biệt Hacker News, Twitter/social search, policy và paper.
  - `wrong_arg_value`: kiểm tra `sort`, `limit`, `max_results` và `timeframe`.
  - `missing_info`: agent phải hỏi lại rồi dùng thông tin người dùng bổ sung ở lượt sau.
  - `wrong_boundary`: chỉ gọi `send` sau khi người dùng xác nhận; không gửi nếu người dùng từ chối.
  - `out_of_scope`: không gọi tool cho yêu cầu đặt vé máy bay.
- Bổ sung 4 case liên quan tới tool mới `hn_search`: `G01`, `G02`, `G06`, `G07`.
- Đối chiếu hai lần chạy group eval:
  - `v3-final`: 9/10 PASS, case accuracy `0.90`, không có provider error.
  - `v4`: 10/10 PASS, case accuracy `1.00`, không có provider error.

### 3.2. Bằng chứng live chat và báo cáo

- Rà soát transcript live chat 5 lượt, bảo đảm có đủ ba tình huống bắt buộc:
  1. Yêu cầu research thông thường.
  2. Yêu cầu thiếu thông tin rồi người dùng bổ sung ở lượt sau.
  3. Yêu cầu đăng/gửi và xác nhận trước khi gọi action tool.
- Tổng hợp bảng B3 về team eval cases và bảng B4 về live-chat evidence trong báo cáo nhóm.
- Đối chiếu các bảng metric với run JSON thay vì ghi theo cảm nhận.
- Ghi nhận trung thực giới hạn của agent: eval có thể PASS theo argument nhưng câu hỏi xác nhận vẫn chưa thể hiện đầy đủ nguyên văn nội dung sẽ gửi.

### 3.3. Phối hợp với Người 4

- Cung cấp các câu hỏi mẫu và kịch bản demo cho UI.
- Yêu cầu UI hiển thị tool call, tool error và ghi transcript thay vì che lỗi.
- Bàn giao tiêu chí báo cáo cho Người 4: lệnh chạy, dependency, bằng chứng kiểm thử và link public.
- Phần code `starter_v0/app.py`, Streamlit, tunnel/deploy và link dùng thử không thuộc phạm vi cá nhân của Người 3.

---

## 4. Bằng chứng

- Eval dataset: [`starter_v0/data/eval_group.json`](../../starter_v0/data/eval_group.json).
- Group run v3-final: [`starter_v0/runs/v3-final_B_group_openrouter_20261110T185319916584.json`](../../starter_v0/runs/v3-final_B_group_openrouter_20261110T185319916584.json).
- Group run v4: [`starter_v0/runs/v4_B_group_openrouter_20261110T195922985028.json`](../../starter_v0/runs/v4_B_group_openrouter_20261110T195922985028.json).
- Live-chat transcript: [`starter_v0/transcripts/v3-final_openrouter_20261110T190651824993.transcript.json`](../../starter_v0/transcripts/v3-final_openrouter_20261110T190651824993.transcript.json).
- Báo cáo nhóm: [`report/team/group_report.md`](group_report.md), đặc biệt các mục B3, B4 và B6.

> Trước khi nộp, thành viên cần bổ sung email/GitHub và bảo đảm có commit kỹ thuật hoặc commit báo cáo mang đúng danh tính Git của mình. Danh sách file là bằng chứng đầu ra của vai trò; lịch sử commit là bằng chứng về người thực hiện.

---

## 5. Tự đánh giá

- **Điểm làm tốt:** bộ eval nhóm bao phủ routing, argument, missing information, multi-turn, action boundary và out-of-scope; bản v4 đạt 10/10 mà không có provider error.
- **Điều học được:** eval case phải kiểm tra đúng hành vi cần đo và chỉ đặt những argument thực sự quan trọng trong `expect`; nếu kiểm tra quá ít thì case có thể PASS dù ý nghĩa câu trả lời chưa đúng hoàn toàn.
- **Hạn chế:** kết quả model có tính dao động; một thay đổi giúp group eval có thể làm giảm base eval. Vì vậy cần giữ cả run trước/sau và không kết luận chỉ từ một câu trả lời đẹp.
- **Phối hợp nhóm:** Người 3 chịu trách nhiệm dữ liệu eval và bằng chứng báo cáo; Người 4 chịu trách nhiệm riêng cho UI và triển khai, tránh chồng chéo quyền sở hữu công việc.
