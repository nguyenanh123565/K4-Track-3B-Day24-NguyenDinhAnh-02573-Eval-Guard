# Nhóm thực hiện K4 Track 3B — ST1

Repo chung: https://github.com/nguyenanh123565/K4-Track-3B-Day24-NguyenDinhAnh-02573-Eval-Guard

Trưởng nhóm: Nguyễn Đình Anh — MSSV 2A202602573 (người dùng xác nhận).
Người tích hợp/người nộp: Chưa cung cấp phân công cụ thể.
Ngày lab/deadline áp dụng: Chưa xác định trong TEAM; xem tài liệu submission — Asia/Ho_Chi_Minh.
Commit dùng để chấm: Chưa chốt commit bản nộp cuối.

## Thành viên và phân công

| STT | Họ và tên | MSSV | Vai trò / công việc thật | Bằng chứng |
|---|---|---|---|---|
| 1 | Nguyễn Đình Anh | 2A202602573 | Trưởng nhóm; đóng góp cụ thể chưa xác nhận | Thông tin người dùng cung cấp; commit/PR cá nhân chưa cung cấp |

Danh sách hiện chỉ có một thành viên được xác nhận. Chưa cung cấp thông tin
thành viên khác; chưa đủ bằng chứng kết luận chỉ một người thực tế làm toàn bộ bài.

## Môi trường và bằng chứng

Windows/PowerShell; Python runtime target: 3.11.9, được xác nhận có trên máy
bằng `py -3.11 -B --version`.
Các checks trong phiên hỗ trợ dùng interpreter `python` 3.12.3; không suy ra
full runtime 3.11 đã pass. Compiler/virtualenv/interpreter sinh answers:
Chưa cung cấp môi trường thực tế của lượt sinh answers.

Offline suite: `python -B -m pytest tests/ -p no:cacheprovider -q --tb=short`:
98 passed, 3 deselected. Integration không chạy; SDK/guard/evaluator được mock,
không phải bằng chứng API/model live. Import m1–m5 và Torch-first runtime đã pass.

Đã đọc toàn bộ artifacts/answers_50q.json: 50 records, factual 20, multi_hop 20,
adversarial 10; generation_mode=extractive_fallback 50/50, generation_model=null
50/50. Không phải 50 lượt generation LLM thành công. Ba JSON reports A/B/C chưa có.

Theo lỗi người dùng báo: OpenAI live API trả HTTP 429 insufficient_quota /
credit_balance_exhausted. Chưa có log lỗi trong repo; không gọi lại API để xác nhận.
Không dùng synthetic/mock artifacts làm experiment hoặc đổi run_kind thành live.

## INDIVIDUAL

### NguyenDinhAnh-2A202602573

- Vai trò: trưởng nhóm ST1.
- Phân công/đóng góp thật: Chưa cung cấp mô tả cá nhân ngoài vai trò trưởng nhóm.
- Bằng chứng cá nhân: Chưa có bằng chứng commit/PR cá nhân trong thông tin đã cung cấp.
- Cách kiểm tra chung: offline suite 98 passed, 3 deselected; answers fallback đã có.
- Điều đã học: Chưa cung cấp ghi nhận cá nhân.
- Giới hạn: quota cạn; chưa có RAGAS/judge/guard live artifacts.
- AI hỗ trợ: Codex hỗ trợ tích hợp modules/adapters, Tasks A/B/C, checks và tài liệu;
  không tự quy mọi thay đổi thành đóng góp của một cá nhân.

Không có mục INDIVIDUAL cho thành viên chưa được xác nhận.

## Cập nhật sau khi nộp

Chưa cung cấp trạng thái nộp hoặc thông tin cập nhật sau deadline; chưa có
bằng chứng về commit bản nộp cuối hoặc chấp thuận cập nhật của coach.
