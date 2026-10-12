# Nhóm thực hiện K4 Track 3B — ST1

Repo chung: https://github.com/nguyenanh123565/K4-Track-3B-Day24-NguyenDinhAnh-02573-Eval-Guard

Trưởng nhóm: Nguyễn Đình Anh — MSSV 2A202602573 (người dùng xác nhận).
Người tích hợp: Nguyễn Đình Anh phối hợp với Codex trong phiên làm việc này.
Người nộp: Nguyễn Đình Anh theo phân công dự kiến cho trưởng nhóm; chưa có bằng chứng gửi bài.
Deadline: theo doc/SUBMISSION.md, mặc định 23:59 ngày làm lab, Asia/Ho_Chi_Minh;
ngày cụ thể và điều chỉnh áp dụng theo thông báo coach, chưa có trong repo.
Phiên bản đã có trên remote trước lượt rà soát này:
`5f89e4c325c435efb777a35ef9e31aa302f0356c`.
Đây là bằng chứng phiên bản repo, không phải commit bản nộp cuối hay bằng chứng
đóng góp riêng của từng thành viên. Các chỉnh sửa tài liệu hiện tại chưa commit.

## Thành viên và phân công

| STT | Họ và tên | MSSV | Vai trò / công việc thật | Bằng chứng |
|---|---|---|---|---|
| 1 | Nguyễn Đình Anh | 2A202602573 | Trưởng nhóm; phụ trách tích hợp code/docs và verification với Codex hỗ trợ | Phiên làm việc và source hiện có; commit 5f89e4c là bằng chứng chung của repo |

### Thành viên còn lại — phân công dự kiến

Tên: Nguyễn Danh GIa Minh

MSSV:2A202602441 __

Phân công dự kiến: review ba báo cáo, kiểm tra checker, rà soát tài liệu nộp và
hỗ trợ verification cuối. Đây không phải đóng góp đã xác nhận. Chưa có bằng chứng
commit/PR của người này. Khi xác nhận danh tính, bổ sung vào bảng thành viên và
mục INDIVIDUAL; không tạo danh tính hoặc lịch sử đóng góp giả.

## Môi trường và bằng chứng

Windows/PowerShell; Python runtime target: 3.11.9, được xác nhận có trên máy
bằng `py -3.11 -B --version`.
Các checks trong phiên hỗ trợ dùng interpreter `python` 3.12.3; không suy ra
full runtime 3.11 đã pass. Repo chưa có log xác nhận compiler, virtualenv và
interpreter của lượt sinh answers; không suy ra các thông tin đó từ file JSON.

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
- Phạm vi phụ trách tích hợp trong phiên hỗ trợ: Tasks Phase A/B/C, m1–m5,
  adapters M2/M4, runtime/debug thứ tự import Torch, kiểm tra answers fallback,
  report/TEAM integration và final verification. Codex trực tiếp hỗ trợ viết
  source và tài liệu; không coi mọi dòng code là do cá nhân tự viết.
- Setup answers: có artifact fallback thật trong repo; chưa có log để quy từng
  thao tác chạy setup hoặc môi trường sinh answers cho một người cụ thể.
- Bằng chứng: source/tests/docs/answers và commit repo 5f89e4c; không có PR riêng
  hoặc bằng chứng tách biệt đóng góp từng người.
- Cách kiểm tra chung: offline suite 98 passed, 3 deselected; answers fallback đã có.
- Nội dung kỹ thuật đã kiểm tra: model provenance, calibration đúng answer
  nguồn, phân biệt mock/live, guard decisions và latency đúng scope. Đây là
  nội dung phiên làm việc, không phải tự nhận xét học tập do cá nhân cung cấp.
- Giới hạn: quota cạn; chưa có RAGAS/judge/guard live artifacts.
- AI hỗ trợ: Codex hỗ trợ tích hợp modules/adapters, Tasks A/B/C, checks và tài liệu;
  không tự quy mọi thay đổi thành đóng góp của một cá nhân.

Phần INDIVIDUAL của thành viên còn lại được hoàn thiện sau khi xác nhận hai
trường danh tính ở trên; hiện chỉ có phân công dự kiến, không có đóng góp xác nhận.

## Cập nhật sau khi nộp

Repo đã được push tới phiên bản 5f89e4c trong phiên trước. Không có bằng chứng
gửi link qua kênh coach, xác định bản nộp cuối hoặc chấp thuận sửa sau deadline.
Lượt tài liệu này chỉ sửa working tree, không commit/push.

Chưa có live evidence do OpenAI quota exhausted.
