# Blueprint CI/CD cho RAG và guardrails — ST1

Đây là kiến trúc/vận hành đề xuất, chưa phải workflow CI/CD đã triển khai.
Trưởng nhóm: Nguyễn Đình Anh, 2A202602573, phụ trách tích hợp và verification
với Codex hỗ trợ. Thành viên còn lại dự kiến review/checker/tài liệu; chưa có
bằng chứng người này đã thực hiện. Vận hành live là kế hoạch sau khi quota sẵn sàng.
Bằng chứng: source, fixtures, answers fallback và offline suite 98 passed,
3 integration deselected. Chưa có ba live JSON reports A/B/C.

Chưa có live evidence do OpenAI quota exhausted.

## Kiến trúc và failure actions đề xuất

Input → Presidio → NeMo input → RAG → NeMo output → response.
PII thì dừng request; input rail chặn jailbreak/off-topic/prompt injection.
RAG chỉ chạy khi allowed. Output bị flag dùng refusal/redaction, output sạch giữ
nguyên. Runner C hiện kiểm thử stages riêng, không chứng minh endpoint end-to-end.

Secrets ở biến môi trường/.env, không commit. Log request id/stage/decision/model
role/timing; redact PII, không ghi credentials/raw nội dung nhạy cảm. Đề xuất fail
closed khi guard timeout/API lỗi và báo dịch vụ tạm không khả dụng; không coi lỗi
là allowed. Không biến evaluator errors thành score 0 hoặc judge errors thành tie.

Answers hiện có 50 records, distribution 20/20/10, extractive_fallback 50/50,
generation_model null 50/50; công khai fallback, không tuyên bố generation LLM
thành công. Người dùng báo OpenAI HTTP 429 insufficient_quota /
credit_balance_exhausted; repo chưa chứa log. Đề xuất kiểm tra billing trước retry,
không retry hàng loạt khi quota cạn. Không gọi API trong bước tài liệu này.

## Latency và guard live chưa đo

Chưa có guard_results.json; attacks pass rate, clean false-positive rate, output
live decisions, raw samples/percentiles/budget_ok chưa có. Không dùng mocks làm số đo.

| Layer / scope | P50 ms | P95 ms | P99 ms | Tình trạng |
|---|---|---|---|---|
| Presidio | chưa đo | chưa đo | chưa đo | Chưa có raw live samples |
| NeMo input | chưa đo | chưa đo | chưa đo | Quota chưa được khắc phục |
| Input guard sequential | chưa đo | chưa đo | chưa đo | Task 12 bắt buộc |
| RAG | chưa đo | chưa đo | chưa đo | Ngoài scope Task 12 |
| NeMo output | chưa đo | chưa đo | chưa đo | Ngoài scope Task 12 |
| Full request/guard | chưa đo | chưa đo | chưa đo | Cần đo độc lập |

Contract source: scope=input_layers_sequential, percentile_method=linear; engines
trước đo, hai warm-up thật và ít nhất 20 timed samples khi nộp. Luôn đo Presidio
rồi NeMo input, không short-circuit; tổng từ tổng hai layers mỗi sample. Percentile
nội suy tại (n-1)*q; không cộng P95 riêng. Đây là phương pháp, không chứng nhận
đã warm-up/đo live. Target input layers 500ms không chứng minh full guard đạt 500ms.
Đề xuất đo full request riêng với warm-up, samples/timestamps và allowed/blocked paths.

## CI gates đề xuất

- Chạy offline pytest, fail job nếu exit code khác 0.
- Chạy check_lab trên saved evidence để kiểm schema/hashes/provenance/counts/
  metrics/labels/decisions/percentiles và tài liệu. Missing live artifact phải fail.
- Lab bắt buộc attacks ít nhất 15/20, clean 8/8 allowed và bốn output cases đúng.
- CI đề xuất attacks ít nhất 18/20, faithfulness ít nhất 0.75 và avg_score ít nhất
  0.65; cần viết job kiểm thresholds rõ ràng, không coi biến MIN_* tự tạo gate.
- Full guard P95 dưới 500ms chỉ xét khi có phép đo độc lập thật.

Chưa có workflow đã chạy hoặc bằng chứng đạt gates. Không đổi run_kind/mock
thành live để vượt checker; các gates đề xuất chưa tự được runner thực thi.

## Monitoring và kế hoạch cải tiến

Đề xuất theo dõi quota/429, stage errors, fallback ratio, PII/input block rates,
clean false positives và latency từng scope. Cảnh báo quota error, false positive
trên clean controls hoặc vượt target; nhóm chỉ định người xử lý và chu kỳ review.
Lấy samples được redact, tách distribution/policy version để kiểm drift.

Kế hoạch: khắc phục quota; chỉ chạy batch thật khi được phép; validate hashes và
schema; đọc lỗi đại diện trước sửa retrieval/prompt. Kiểm tra version conflict/
negation, bảo toàn clean controls, xác minh Qdrant server thay fallback memory,
đo scope đầy đủ trước tối ưu. Đây là kế hoạch từ giới hạn hiện tại, không phải
kết luận từ scores chưa có.

RAGAS mean/weakest distribution và kappa: chưa có. Guard pass rate/latency: chưa đo.
Offline Phase A/B/C pass chỉ chứng minh contracts với mocks; không dùng synthetic
artifacts như experiment. Fixtures 50/20/8/4 giới hạn khả năng suy rộng ngay cả
sau khi có kết quả live.
