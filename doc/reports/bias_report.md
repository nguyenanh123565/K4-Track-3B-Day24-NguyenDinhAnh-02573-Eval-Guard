# Đánh giá LLM Judge Phase B — ST1

## Trạng thái và nguồn

Chưa có artifacts/judge_results.json và judge live evidence vì quota người dùng
báo: HTTP 429 insufficient_quota / credit_balance_exhausted. Repo chưa chứa log
lỗi; không gọi lại API trong bước tài liệu này. Answers có 50 records với
extractive_fallback 50/50, generation_model null. Offline suite 98 passed,
3 integration deselected không thay kết quả judge thật. Winners/scores/reasoning,
kappa, agreement, bias rates, timestamp và model provenance live chưa có.
Người phụ trách báo cáo cụ thể chưa được phân công.

## Pairwise và swap

Question_ids cố định: 1,5,12,21,41. A từ artifacts/answers_50q.json:answer;
B từ fixtures/human_labels_10q.json:model_answer; question/reference từ
fixtures/test_set_50q.json. Không đổi candidates sau judge. Prompt đánh giá
accuracy theo reference, completeness, conciseness. JUDGE_MODEL là cấu hình
source, không phải bằng chứng model đã chạy thành công.

Hai lượt (A,B) và (B,A); raw winner A lượt hai chuyển thành original B, raw B
thành original A, tie giữ tie; scores cũng đảo tương ứng. Đồng thuận thì giữ
winner, bất đồng thì tie. Giữ reasoning hai lượt.
Position inconsistency rate = số cặp không đồng thuận / tổng cặp.
Verbosity chỉ xét winner A/B: số winner dài hơn / số decisive cases;
không có decisive thì hàm trả 0 theo contract. Đây là công thức, không phải số đo.
Các tỷ lệ là dấu hiệu, cần đọc nội dung trước khi kết luận nguyên nhân bias.

## Binary calibration và Cohen's kappa

Helper nhận đúng question/model_answer gốc của 10 human records cùng reference
đúng id, không dùng answer pipeline mới. Không truyền human_label/human_note vào
prompt. Chỉ đối chiếu human labels sau judge, giữ ids/thứ tự đồng bộ. Winner A/B
không được chuyển máy móc thành nhãn chất lượng 0/1.

Kappa = (observed agreement - chance agreement) / (1 - chance agreement), với
chance agreement từ marginal frequencies. Validate int 0/1, loại bool, list
không rỗng/cùng độ dài. Constant unanimous agreement dùng quy ước 1.0 trong hàm;
calibration supplied labels có cả hai classes.

## Giới hạn và phần chờ

Chờ judge_results.json thật mới điền năm cặp, mười judgments, kappa, rates,
reasoning, models và diễn giải case lệch human. Không tuyên bố đạt kappa >0.6
hay bonus. Năm cặp/mười nhãn có quy mô nhỏ; judge cần kiểm chứng bằng reference.
Không dùng mock/synthetic artifacts làm experiment, không đổi run_kind thành live.
