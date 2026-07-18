# Aegis AI — Ràng buộc đạo đức

Tài liệu này quy định các ràng buộc đạo đức **bắt buộc** cho toàn bộ team.
Mọi thành viên phải đọc và tuân thủ trước khi contribute code.

---

## Nguyên tắc nền tảng

Hệ thống này can thiệp vào cuộc sống học sinh thật. Một cảnh báo sai có thể gây:
- Học sinh bị gọi lên không lý do → mất niềm tin
- Giáo viên mất thời gian vào false positive → bỏ qua true positive
- Bias ẩn → nhóm học sinh cụ thể bị flag nhiều hơn không công bằng

**Vì vậy, hệ thống ưu tiên "ít cảnh báo nhưng đáng tin" hơn "nhiều cảnh báo để không bỏ sót".**

---

## Bright Lines — Ranh giới KHÔNG BAO GIỜ vượt qua

### 🔴 1. Bảo vệ Privacy tuyệt đối

- KHÔNG đọc nội dung tin nhắn, email, bài viết cá nhân của học sinh
- KHÔNG phân tích cảm xúc (sentiment analysis) từ bất kỳ nguồn nào
- KHÔNG thu thập dữ liệu ngoài phạm vi: điểm, điểm danh, submission metadata
- KHÔNG lưu trữ dữ liệu cá nhân quá thời hạn cần thiết

### 🔴 2. Không gắn nhãn, không phán xét

- KHÔNG output "học sinh này SẼ bỏ học" — chỉ output "có thay đổi cần theo dõi"
- KHÔNG dùng ngôn ngữ tiêu cực: "nguy hiểm", "yếu kém", "có vấn đề"
- KHÔNG ranking học sinh theo mức độ "nguy cơ"
- Trạng thái phản ánh **thay đổi so với chính mình**, không phải đánh giá năng lực

### 🔴 3. Không so sánh với đám đông để tạo cảnh báo

- KHÔNG dùng Isolation Forest, clustering, hoặc bất kỳ kỹ thuật anomaly detection dựa trên cohort
- KHÔNG ranking, percentile, hay z-score so với lớp/trường
- Mọi z-score trong hệ thống là **so với chính học sinh đó** (intra-individual)
- **Ngoại lệ duy nhất**: Seasonal filter dùng class-level statistics CHỈ ĐỂ SUPPRESS cảnh báo

### 🔴 4. Hệ thống không tự hành động

- KHÔNG tự động gửi email/thông báo cho học sinh
- KHÔNG tự động ghi nhận vào hồ sơ kỷ luật
- KHÔNG tự động điều chỉnh ngưỡng cảnh báo
- Giáo viên là người quyết định cuối cùng trong MỌI trường hợp

---

## Kiểm tra trước khi merge

Trước khi merge bất kỳ PR nào, reviewer kiểm tra:

- [ ] Code có so sánh học sinh với nhau không? → REJECT nếu dùng để tạo cảnh báo
- [ ] Code có gắn label deterministic không? → REJECT
- [ ] Code có thu thập dữ liệu ngoài scope không? → REJECT
- [ ] Thiếu dữ liệu có được xử lý đúng (raise error / return insufficient)? → REJECT nếu return giá trị mặc định
- [ ] Cảnh báo có explanation bằng ngôn ngữ phi kỹ thuật không? → REJECT nếu hiển thị z-score thô
