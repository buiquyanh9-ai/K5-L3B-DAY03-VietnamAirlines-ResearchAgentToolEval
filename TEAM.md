# Team

## Thông tin nhóm

- Tên nhóm: VietnamAirlines
- Lớp: L3B
- Repo nhóm: `K5-L3B-DAY03-VietnamAirlines-ResearchAgentToolEval` (xem [SUBMISSION.md](SUBMISSION.md))
- URL repo, nhánh nộp, commit chốt: https://github.com/buiquyanh9-ai/K5-L3B-DAY03-VietnamAirlines-ResearchAgentToolEval, nhánh `main`, commit chốt: b9890f33cbbd4eb1c3770e9a2adfc427d2a980af

## Thành viên

| STT | Họ tên | MSSV | Email | GitHub | Vai trò |
| --: | ------ | ---- | ----- | ------ | ------- |
| 1 | Nguyễn Thanh Tùng | 2A202603957 | Thtung13102004@gmail.com | [wewewewe07](https://github.com/wewewewe07) | **Người 1 — Tool Engineer & Testing:** tool mới, unit test, contract test; CP3 và hỗ trợ CP1 |
| 2 | Bùi Đình Quý Anh | 2A202603969 | buiquyanh9@gmail.com | [buiquyanh9-ai](https://github.com/buiquyanh9-ai) | **Người 2 — Prompt & Optimization Lead:** baseline v0, tối ưu v1–v3, base eval và version log; CP1–CP2 |
| 3 | Giang Thái Sơn | 2A202603964 | giangson309@gmail.com | [son309](https://github.com/son309) | **Người 3 — Eval Dataset, UI & Reporting:** 10 eval case, group eval, Streamlit UI, tunnel/deploy, live-chat evidence và báo cáo; CP4–CP5 |

## Nguyễn Thanh Tùng — 2A202603957

### Phần việc phụ trách

- Người 1 — Tool Engineer & Testing.
- Phụ trách CP3: thiết kế tool mới, viết unit test và giữ contract test hoạt động.
- Hỗ trợ CP1 bằng việc rà soát dependency, API key phụ trợ và test baseline.

### Đóng góp cụ thể

- Thiết kế tool mới `hn_search` để tìm bài viết và thảo luận trên Hacker News bằng Algolia API.
- Xử lý input xấu, ép kiểu `limit`, kẹp giới hạn `1–20`, fallback URL và chuẩn hóa lỗi thành error dictionary.
- Viết `TOOL.md`, đăng ký tool trong `tools/__init__.py` và phối hợp khai báo schema trong `tools.yaml`.
- Xây dựng các unit test cho happy path, bad input, sort theo ngày, boundary, HTTP error và timeout.

### Bằng chứng

- Báo cáo cá nhân: [`report/team/2A202603957_NguyenThanhTung.md`](report/team/2A202603957_NguyenThanhTung.md).
- Tool mới: [`starter_v0/tools/hn_search/tool.py`](starter_v0/tools/hn_search/tool.py) và [`TOOL.md`](starter_v0/tools/hn_search/TOOL.md).
- Unit test: [`starter_v0/tests/test_tools_todo.py`](starter_v0/tests/test_tools_todo.py).
- Đăng ký tool: [`starter_v0/tools/__init__.py`](starter_v0/tools/__init__.py) và [`starter_v0/artifacts/tools.yaml`](starter_v0/artifacts/tools.yaml).

## Bùi Đình Quý Anh — 2A202603969

### Phần việc phụ trách

- Người 2 — Prompt & Optimization Lead.
- Phụ trách CP1–CP2: baseline v0, tối ưu prompt/tool declaration từ v1 đến v3, chạy base eval và ghi version log.
- Quản lý repo, cấu hình provider/API key và kiểm tra bằng chứng run trước khi đưa vào báo cáo.

### Đóng góp cụ thể

- Chạy baseline v0, phân loại 7 case FAIL và ghi kết quả ban đầu `0.65`.
- Tối ưu `system_prompt.md` và `tools.yaml` qua các giả thuyết v1–v3; ghi trung thực cả vòng v3 không tăng điểm.
- Chạy và đối chiếu các run v0–v4, kiểm tra hash, metric và `provider_error_cases`.
- Ghi `artifacts/version_log.csv`, thực hiện live chat và phối hợp rà soát báo cáo nhóm.

### Bằng chứng

- Báo cáo cá nhân: [`report/team/2A202603969_BuiDinhQuyAnh_member1.md`](report/team/2A202603969_BuiDinhQuyAnh_member1.md).
- Prompt và tool declaration: [`starter_v0/artifacts/system_prompt.md`](starter_v0/artifacts/system_prompt.md) và [`tools.yaml`](starter_v0/artifacts/tools.yaml).
- Version log: [`starter_v0/artifacts/version_log.csv`](starter_v0/artifacts/version_log.csv).
- Run evidence: [`starter_v0/runs/`](starter_v0/runs/) và transcript [`v3-final_openrouter_20261110T190651824993.transcript.json`](starter_v0/transcripts/v3-final_openrouter_20261110T190651824993.transcript.json).

## Giang Thái Sơn — 2A202603964

### Phần việc phụ trách

- Người 3 — Eval Dataset, UI & Reporting.
- Phụ trách CP4: thiết kế 10 group eval case và đối chiếu kết quả group eval.
- Phụ trách CP5: xây dựng và kiểm thử Streamlit UI, ghi transcript, chuẩn bị tunnel/deploy, link dùng thử, live-chat evidence, bảng kết quả và reflection.

### Đóng góp cụ thể

- Hoàn thiện bộ `eval_group.json` gồm đúng 5 single-turn và 5 multi-turn.
- Bao phủ các lỗi routing, argument, missing information, action boundary và out-of-scope; có 4 case kiểm tra tool mới `hn_search`.
- Đối chiếu group run v3-final đạt `9/10` và v4 đạt `10/10`, đều không có provider error.
- Xây dựng `starter_v0/app.py` bằng Streamlit, hỗ trợ chat nhiều lượt, chọn provider/model, hiển thị tool call, kết quả và lỗi tool.
- Thêm dependency Streamlit, ghi transcript từ giao diện và chuẩn bị lệnh chạy/tunnel để người ngoài dùng thử.
- Tổng hợp bằng chứng group eval, live chat và giới hạn của agent vào báo cáo nhóm.

### Bằng chứng

- Báo cáo cá nhân: [`report/team/2A202603964_GiangThaiSon.md`](report/team/2A202603964_GiangThaiSon.md).
- Eval dataset: [`starter_v0/data/eval_group.json`](starter_v0/data/eval_group.json).
- Group runs: [`v3-final_B_group_openrouter_20261110T185319916584.json`](starter_v0/runs/v3-final_B_group_openrouter_20261110T185319916584.json) và [`v4_B_group_openrouter_20261110T195922985028.json`](starter_v0/runs/v4_B_group_openrouter_20261110T195922985028.json).
- UI: [`starter_v0/app.py`](starter_v0/app.py), [`starter_v0/requirements.txt`](starter_v0/requirements.txt) và transcript [`v4_openrouter_ui_20261110T204527398264.transcript.json`](starter_v0/transcripts/v4_openrouter_ui_20261110T204527398264.transcript.json).
- Báo cáo nhóm: [`report/team/group_report.md`](report/team/group_report.md), đặc biệt các mục B3, B4 và B6.
