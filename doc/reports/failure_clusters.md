# Phân tích lỗi Phase A — ST1

## Bằng chứng và trạng thái

Nguồn hiện có: artifacts/answers_50q.json, fixtures và source Tasks 1–4.
Answers có 50 records: factual 20, multi_hop 20, adversarial 10;
extractive_fallback 50/50, generation_model null 50/50.
Chưa có artifacts/ragas_50q.json, timestamp hoặc evaluator metadata của lượt thật.
RAGAS scores, bottom 10, matrix và nhóm yếu nhất chưa có; không điền 0 thay số liệu.
Phụ trách tích hợp báo cáo: Nguyễn Đình Anh với Codex hỗ trợ; thành viên còn lại
review theo phân công dự kiến trong TEAM, chưa có bằng chứng review cá nhân.

Chưa có live evidence do OpenAI quota exhausted.

Theo người dùng, OpenAI API trả HTTP 429 insufficient_quota / credit_balance_exhausted;
repo chưa lưu log lỗi. Chưa có RAGAS live evidence. Offline suite 98 passed,
3 integration deselected chỉ kiểm tra logic với mocks, không thay experiment.

## Methodology và contract

Task 1 group theo distribution, không sửa dữ liệu. Task 2 gọi m4 một lần với
question/answer/contexts/ground_truth theo thứ tự, giữ ids và fields nguồn.
Bốn metrics Python float hữu hạn [0,1]: faithfulness (context hỗ trợ answer),
answer_relevancy (đáp ứng question), context_precision (retrieval đúng) và
context_recall (retrieval đủ). Evaluator IDs lấy từ m4 thực dùng, không lấy JUDGE_MODEL.

avg_score là trung bình bốn metrics. Bottom 10 sort tăng dần, rank từ 1, kèm
question_id/distribution/question/avg_score/worst_metric/diagnosis/suggested_fix.
Diagnosis/fix từ DIAGNOSTIC_TREE là gợi ý; exporter giữ nguyên rows Task 3.

Matrix worst_metric × distribution đếm mỗi câu một cell, không coi mọi câu là
failure. Mean chỉ tính nhóm không rỗng; nhóm yếu có mean thấp nhất, không chọn
count lớn nhất. Dominant metric có tổng matrix lớn nhất. Counts 20/20/10 là kích
thước fixture, không phải kết quả chất lượng.

## Phần chờ evaluation thật và giới hạn

Sau khi có ragas_50q.json hợp lệ, bổ sung scores/summaries, bottom rows, matrix,
models/timestamp và đối chiếu answer/contexts/reference của các câu yếu để phân
biệt retrieval, generation, phiên bản và phủ định. Chưa kết luận nhóm nào yếu,
adversarial thấp hơn factual, nhận ra version conflict hoặc đạt bonus.

Answers extractive fallback không chứng minh generation LLM thành công. Không
trình bày synthetic/mock artifacts như experiment, không đổi run_kind thành live.
Phân bố nhỏ và evaluator/model/fallback phải được ghi rõ khi diễn giải kết quả sau này.
