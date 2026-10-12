# K4 Track 3B — Production Eval + Guardrail Stack

**Bài nhóm: mỗi nhóm dùng và nộp một repo chung của trưởng nhóm.**
Mỗi người khai phần thực tế đã làm trong [doc/TEAM.md](doc/TEAM.md).

**Thời lượng trên lớp:** 15 phút kiểm tra sẵn sàng + 90 phút thực hành
(Phase A/B/C, mỗi phase 30 phút). Cài dependencies, build tools, tải model,
indexing và sinh 50 answers được làm **trước buổi học**, không gộp vào 15 phút.

**Điểm:** 100 điểm bắt buộc + tối đa 10 bonus cho bài lab.

**Repo đề bài:** [K4-Track-3B-Day24-Eval-Guard](https://github.com/VinUni-AI20k/K4-Track-3B-Day24-Eval-Guard).
Nhóm ST1, repo hiện tại: [Day24 ST1](https://github.com/nguyenanh123565/K4-Track-3B-Day24-NguyenDinhAnh-02573-Eval-Guard).
Tên repo theo mẫu nộp bài được mô tả trong doc/SUBMISSION.md.

## Cấu trúc repo

- `src/`: Tasks Phase A/B/C đã implement, modules m1–m5 và phần hỗ trợ.
- `scripts/`: setup, runner và checker; chạy từ gốc repo.
- `fixtures/`: bộ câu hỏi và dữ liệu kiểm thử được cấp sẵn.
- `data/`: tài liệu nguồn cho RAG.
- `doc/`: đề bài, hướng dẫn, TEAM và mẫu báo cáo.
- `requirements/`: dependencies và constraints.
- `infra/`: Docker Compose; `guardrails/`: cấu hình guard.
- `tests/`: tests offline và integration tùy chọn.
- `artifacts/`: kết quả nhóm tự tạo sau khi làm bài.

## Mục tiêu và nơi viết kết quả

Nhóm đánh giá pipeline RAG, độ tin cậy của LLM Judge và guard input/output.
**Trạng thái hiện tại:** Tasks A/B/C và adapters đã implement; offline suite
98 passed, 3 integration deselected. Python runtime target 3.11.9 có trên máy;
checks trong phiên hỗ trợ chạy bằng Python 3.12.3, không chứng minh full runtime 3.11.
TEAM và ba báo cáo đã mô tả phương pháp, bằng chứng và giới hạn; chỉ hai trường
Tên/MSSV thành viên còn lại dành cho tự điền.
`artifacts/answers_50q.json` có 50 records, factual 20/multi_hop 20/adversarial 10,
extractive_fallback 50/50 và generation_model null 50/50.
Chưa có live evidence do OpenAI quota exhausted. Lỗi người dùng báo là HTTP 429
credit_balance_exhausted; repo không có log API để xác nhận độc lập.
Thiếu ragas_50q.json, judge_results.json và guard_results.json; không có scores,
kappa, guard pass rate hoặc latency live. Không dùng mock results làm experiment.
Các file `fixtures/test_set_50q.json`,
`fixtures/human_labels_10q.json`, `fixtures/adversarial_set_20.json`, `fixtures/clean_set_8.json` và
`fixtures/output_set_4.json` là dữ liệu đề bài được cấp sẵn, không phải kết quả đã chạy.

Dùng **`artifacts/` cho dữ liệu kết quả JSON** và **`doc/reports/` cho báo cáo
Markdown**. Đóng góp cá nhân nằm ở `doc/TEAM.md`, không viết thay cho phân tích kỹ
thuật. File sinh tự động vẫn phải commit vào repo bài nộp sau khi kiểm tra secrets.

| Nội dung | Đường dẫn từ gốc repo | Người phụ trách | Cách tạo |
|---|---|---|---|
| Thành viên, công việc, điều đã học | `doc/TEAM.md` | Từng người, trưởng nhóm đối chiếu | Điền tay |
| Answers và contexts của pipeline | `artifacts/answers_50q.json` | Người tích hợp pipeline | `scripts/setup_answers.py --live` |
| RAGAS từng câu, bottom 10, cluster | `artifacts/ragas_50q.json` | Phase A | Runner tự lưu kết quả thật |
| Phân tích lỗi và hướng sửa | `doc/reports/failure_clusters.md` | Phase A | Điền tay từ JSON |
| Pairwise, nhãn 0/1, κ, bias | `artifacts/judge_results.json` | Phase B | Runner tự lưu kết quả thật |
| Diễn giải κ và bias | `doc/reports/bias_report.md` | Phase B | Điền tay từ JSON |
| 20 attacks, 8 clean inputs, output, latency | `artifacts/guard_results.json` | Phase C | Runner tự lưu kết quả thật |
| Kiến trúc, CI gates, monitoring | `doc/reports/blueprint.md` | Cả nhóm, người tích hợp | Điền tay; đề xuất CI/CD |

Đọc [đề bài](doc/ASSIGNMENT.md), [checkpoints](doc/CHECKPOINTS.md),
[rubric](doc/RUBRIC.md), [quy định](doc/RULES.md) và [nộp bài](doc/SUBMISSION.md).
Giao diện mã bài trước nằm trong [PIPELINE_INTERFACE.md](doc/PIPELINE_INTERFACE.md);
schema và cách chạy nằm trong [REPORT_SCHEMAS.md](doc/REPORT_SCHEMAS.md).

## Chuẩn bị trước buổi học

Môi trường mục tiêu là **Python 3.11.9**. Dùng `requirements/requirements-test.lock.txt` cho
unit tests offline và `requirements/requirements.txt` cùng `requirements/constraints-core.txt` cho full
runtime. NeMo/Annoy cần compiler C++ trên Windows. Nhóm phải kiểm tra cài đặt,
imports và model trên máy của mình theo [ENVIRONMENT.md](doc/ENVIRONMENT.md).

1. Làm theo [ENVIRONMENT.md](doc/ENVIRONMENT.md), chuẩn bị compiler, Docker và
   dependencies trước buổi học. Windows có thể chạy trực tiếp Python trong
   virtualenv nếu PowerShell không cho kích hoạt; không cần đổi policy toàn máy.
2. Đưa năm module `m1`–`m5` từ bài RAG trước vào `src/`, đối chiếu bảng giao
   diện. `pipeline.py` có thể giữ làm tham khảo; setup **không gọi file này**.
3. Tải spaCy và model embedding/rerank, khởi động Qdrant đã pin
   `qdrant/qdrant:v1.9.7`; kiểm tra key trong `.env`.
4. Từ gốc repo, sinh answers trước buổi học:

```bash
python scripts/setup_answers.py --live
```

Đầu ra cần 50 bản ghi thuộc 20 factual, 20 multi_hop, 10 adversarial. Mỗi bản ghi
có answer, contexts và ground_truth riêng biệt; `generation_mode` ghi rõ LLM hay
extractive fallback, `generation_model` là ID model hoặc null với fallback.
Không dùng ground truth thay answer để tạo điểm đẹp. Task 2 trả RagasEvaluation
với evaluator_models từ m4; metadata phiên bản 2 tách model theo từng vai trò.

## Kiểm tra trên lớp và chạy thực nghiệm

Trong 15 phút đầu, xác nhận virtualenv, Qdrant, module/interface và 50 answers
đã sẵn sàng; điền thành viên/phân công. Cài đặt cold-cache hoặc tải model chưa
xong là việc chuẩn bị còn thiếu, không giả định sẽ hoàn tất trong mốc 15 phút.

1. Các hàm Tasks A/B/C đã implement. Tests mặc định dùng mock, không gọi
   API và không tải spaCy/model; pass offline không chứng minh live experiment.
2. Chạy unit tests; dùng `-m support` khi chỉ kiểm tra phần scaffold cung cấp:

```bash
python -m pytest tests/ -q
python -m pytest tests/ -m support -q
```

3. Sau khi implement, chạy một batch thực nghiệm thật. `--live` xác nhận dùng
   API và mạng; có chi phí. Runner không tạo báo cáo hợp lệ từ TODO còn nguyên.

```bash
python scripts/run_experiments.py --phase a --live
python scripts/run_experiments.py --phase b --live
python scripts/run_experiments.py --phase c --live --latency-samples 20
```

Phase B dùng đúng `model_answer` của 10 bản ghi human labels cho nhãn 0/1; không
dùng answer pipeline mới và không gửi human_label/human_note vào judge.
Phase C đòi **ít nhất 15/20 attacks**, kiểm tra **8/8 câu sạch được allowed**,
và kiểm tra output. Bonus giữ mốc **18/20 attacks**, kèm clean controls đạt.

4. Điền ba báo cáo Markdown và TEAM, rồi kiểm tra bằng chứng đã lưu:

```bash
python scripts/check_lab.py
```

Checker mặc định không chạy pytest lại và không gọi API. Nếu muốn gộp unit tests
với kiểm tra bài nộp, chỉ chạy `python scripts/check_lab.py --with-tests`.
Checker validate Answers/Phase A/B/C bằng JSON Schema trước khi đối chiếu nguồn
và phép tính; thiếu/sai generation_mode, pair_sources hoặc metadata đều bị từ chối.
Trong repo hiện tại, source và answers pass checker; ba live artifacts còn thiếu.
TEAM vẫn cần xác nhận danh tính thành viên còn lại trước khi nộp hoàn chỉnh.
Integration tests là lựa chọn thay cho chạy batch B/C riêng, không chạy cả hai
để tránh trả phí hai lần: `python -m pytest -m integration --run-live`.

Trưởng nhóm nộp một link repo theo kênh coach công bố. Deadline mặc định là
**23:59 ngày làm lab, Asia/Ho_Chi_Minh (UTC+07:00)** theo SUBMISSION/ASSIGNMENT/RULES;
repo chưa có thông báo coach xác nhận ngày cụ thể. Áp dụng điều chỉnh của
key coach trong 48 giờ sau lab theo quy ước chung. Blueprint là đề xuất CI/CD,
không mặc nhiên là workflow đã chạy.
