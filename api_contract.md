# Aegis AI: API Contract & Frontend Integration Guide

Tài liệu này định nghĩa rõ **Input** (dữ liệu Frontend gửi đi) và **Output** (dữ liệu Frontend nhận về từ Backend). Team Frontend có thể dựa hoàn toàn vào các Interface này để bắt đầu thiết kế UI Components, Setup Store (Pinia), và Mock Data mà không cần chờ Backend hoàn thiện logic xử lý.

---

## 1. Các Quy định Chung (Frontend Rules)

> [!IMPORTANT]
> **Ràng buộc Đạo đức & Hiển thị (BẮT BUỘC):**
> 1. **KHÔNG** hiển thị chỉ số z-score, số liệu thô hoặc thuật ngữ thống kê (clustering, classification).
> 2. Mọi cảnh báo phải đi kèm giải thích bằng **Tiếng Việt** (trường `explanation` từ Backend).
> 3. Không gán nhãn dự đoán tương lai (như "sẽ bỏ học", "nguy hiểm"). Chỉ sử dụng các nhãn mức độ thay đổi (Alert Levels).

### Bảng Màu Quy Định cho UI (Alert Levels)

| Alert Level | Label (Tiếng Việt) | Màu Sắc Gợi Ý (CSS Variable) | Biểu Tượng Gợi Ý |
| :--- | :--- | :--- | :--- |
| `stable` | Ổn định | 🟢 Xanh lá (`var(--color-success)`) | Check circle |
| `watch` | Theo dõi thay đổi | 🟡 Vàng (`var(--color-warning)`) | Eye / Info |
| `review` | Cần giáo viên xem xét | 🟠 Cam (`var(--color-danger)`) | Alert triangle |
| `improving`| Đang cải thiện | 🔵 Xanh dương (`var(--color-info)`) | Trending up |
| `insufficient_data`| Chưa đủ dữ liệu | ⬜ Xám (`var(--color-neutral)`) | Dash / Clock |

---

## 2. API Endpoints & Data Models (Output)

Backend API cung cấp các dữ liệu đã được xử lý thành ngôn ngữ tự nhiên. Frontend **chỉ việc hiển thị**, không cần tính toán logic cảnh báo.

### 2.1. GET `/api/overview`
Dùng cho màn hình Dashboard tổng quan. Trả về thống kê số lượng học sinh theo từng nhóm.

**Output (JSON):**
```json
{
  "total_students": 20,
  "stable_count": 15,
  "watch_count": 2,
  "review_count": 1,
  "insufficient_count": 1,
  "improving_count": 1
}
```

### 2.2. GET `/api/students`
Dùng cho Component Danh sách học sinh (Student List / Data Table).

**Output (JSON Array of `StudentSummary`):**
```json
[
  {
    "student_id": "SV001",
    "student_name": "Nguyễn Văn A",
    "major": "IT",
    "alert_level": "review",
    "headline": "Điểm số sụt giảm mạnh so với tuần trước",
    "triggered_signal_count": 1,
    "updated_at": "2026-07-18T10:00:00Z"
  },
  {
    "student_id": "SV002",
    "student_name": "Nguyễn Văn B",
    "major": "IT",
    "alert_level": "stable",
    "headline": "Kết quả học tập duy trì ổn định",
    "triggered_signal_count": 0,
    "updated_at": "2026-07-18T10:00:00Z"
  }
]
```

### 2.3. GET `/api/students/{student_id}`
Dùng cho Màn hình Chi tiết Học sinh (Profile/Detail Page). Cung cấp toàn bộ tín hiệu và dữ liệu vẽ biểu đồ timeline.

**Output (`StudentDetail`):**
```json
{
  "student_id": "SV001",
  "student_name": "Nguyễn Văn A",
  "major": "IT",
  "alert_level": "review",
  "headline": "Điểm số sụt giảm mạnh so với tuần trước",
  "is_seasonal_suppressed": false,
  
  "signals": [
    {
      "signal_type": "grade",
      "is_triggered": true,
      "data_sufficiency": "sufficient",
      "explanation": "Kết quả 2 bài lab gần nhất thấp hơn đáng kể so với mức bình thường của học sinh này."
    },
    {
      "signal_type": "attendance",
      "is_triggered": false,
      "data_sufficiency": "sufficient",
      "explanation": "Chuyên cần duy trì ở mức tốt (100%)."
    }
  ],
  
  "timeline": [
    {
      "week": "2026-W12",
      "grade_value": 0.85,
      "attendance_value": 1.0,
      "submission_value": null
    },
    {
      "week": "2026-W13",
      "grade_value": 0.50,
      "attendance_value": 0.8,
      "submission_value": null
    }
  ],
  
  "alert_history": [
    {
      "date": "2026-07-10T10:00:00Z",
      "level": "watch",
      "headline": "Có dấu hiệu giảm điểm nhẹ",
      "details": ["Điểm Quiz 2 thấp hơn trung bình."]
    }
  ]
}
```

> [!TIP]
> **Biểu đồ Timeline:** Các giá trị `grade_value`, `attendance_value` đã được Normalize về thang đo `[0, 1]` (0 là cực kỳ tệ, 1 là cực kỳ tốt). Frontend có thể dùng Recharts hoặc Chart.js để vẽ multi-line chart chồng lên nhau trực tiếp bằng các số liệu này mà không cần tính toán quy đổi thang điểm.

---

## 3. Data Models (Input)

Hệ thống Aegis AI là hệ thống một chiều (one-way). Dữ liệu input duy nhất từ phía Frontend là ghi nhận phản hồi (Feedback/Action log) của giáo viên.

### 3.1. POST `/api/students/{student_id}/feedback`
Dùng cho Component form khi giáo viên quyết định hành động đối với một cảnh báo.

**Input (JSON Body):**
```json
{
  "student_id": "SV001",
  "teacher_id": "GV999",
  "action_taken": "meeting",  // Các tuỳ chọn: "contacted", "meeting", "dismissed", "noted"
  "notes": "Đã hẹn gặp sinh viên vào sáng thứ 3 để trao đổi về lý do rớt điểm đột ngột."
}
```

**Output:**
```json
{
  "success": true,
  "message": "Đã ghi nhận phản hồi."
}
```

---

## 4. Gợi ý cấu trúc Component cho Frontend

Để thiết kế đạt chất lượng premium, dynamic nhưng vẫn tuân thủ rule, Team Frontend nên chia các component như sau:

1. `StatusBadge.vue`: Nhận prop `alert_level` và render màu sắc + icon tự động.
2. `AlertCard.vue`: Hiển thị `headline` ở trạng thái thu gọn, và mở rộng ra để hiển thị mảng `signals` với `explanation`. Sử dụng micro-animations cho tương tác mở rộng.
3. `TimelineChart.vue`: Nhận prop `timeline` (Mảng TimelinePoint) để vẽ biểu đồ theo dõi trend cá nhân.
4. `ActionForm.vue`: Form nhập `FeedbackRequest` để submit lên API.
