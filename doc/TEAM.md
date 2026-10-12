# TEAM — Nhóm ST1

## Thông tin nhóm

- Nhóm: ST1
- Repo: https://github.com/nguyenanh123565/K4-Track-3B-Day24-NguyenDinhAnh-02573-Eval-Guard
- Trưởng nhóm: Nguyễn Đình Anh — 2A202602573
- Nhánh nộp bài: `main`

## Thành viên và phân công

| STT | Họ và tên | MSSV | Phân công |
|---|---|---|---|
| 1 | Nguyễn Đình Anh | 2A202602573 | Trưởng nhóm; tích hợp các module m1–m5; hoàn thiện Phase A/B/C; xử lý lỗi môi trường/runtime; sinh answers; tổng hợp tài liệu; chạy tests/checker và chuẩn bị bản nộp |
| 2 | Nguyễn Danh Gia Minh | 2A202602441 | Rà soát báo cáo; đối chiếu yêu cầu bài; kiểm tra cấu trúc tài liệu; hỗ trợ chạy checker và kiểm tra bản nộp cuối |

## Môi trường thực hiện

- Hệ điều hành: Windows
- Python: 3.11.9
- Virtual environment: `.venv`
- Qdrant: Docker
- Test framework: pytest
- Version control: Git / GitHub

## Kết quả kiểm tra

Lệnh kiểm tra:

```powershell
python -B -m pytest tests\ -p no:cacheprovider -q --tb=short