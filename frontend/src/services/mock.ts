import type {
  OverviewStats,
  StudentSummary,
  StudentDetail,
} from '@/types'



// ── Dashboard: Xu hướng theo tuần ──
export const mockWeeklyTrend = [
  { week: 'W06', stable: 30, watch: 6, review: 3, improving: 2, insufficient: 7 },
  { week: 'W07', stable: 28, watch: 8, review: 3, improving: 2, insufficient: 7 },
  { week: 'W08', stable: 27, watch: 9, review: 4, improving: 3, insufficient: 5 },
  { week: 'W09', stable: 26, watch: 10, review: 4, improving: 3, insufficient: 5 },
  { week: 'W10', stable: 25, watch: 10, review: 5, improving: 4, insufficient: 4 },
  { week: 'W11', stable: 25, watch: 10, review: 5, improving: 4, insufficient: 4 },
  { week: 'W12', stable: 25, watch: 10, review: 5, improving: 4, insufficient: 4 },
]

// ── Dashboard: Phân bố theo ngành ──
export const mockMajorDistribution = [
  { major: 'Khoa học Máy tính', stable: 9, watch: 3, review: 2, improving: 1, insufficient: 1 },
  { major: 'Kỹ thuật Phần mềm', stable: 9, watch: 4, review: 1, improving: 1, insufficient: 2 },
  { major: 'Trí tuệ nhân tạo', stable: 7, watch: 3, review: 2, improving: 2, insufficient: 1 },
]

// ── Dashboard: Thống kê tín hiệu ──
export const mockSignalStats = {
  grade: { triggered: 8, total: 44, label: 'Điểm học tập' },
  attendance: { triggered: 6, total: 44, label: 'Điểm danh' },
  submission: { triggered: 4, total: 44, label: 'Nộp bài' },
}

// ── Dashboard: HS cần ưu tiên ──
export const mockPriorityStudents = [
  { student_id: 'SV040', student_name: 'Tôn Văn Nghĩa', major: 'Khoa học Máy tính', alert_level: 'review' as const, triggered_signal_count: 3, headline: 'Vắng mặt 3 buổi và nộp bài trễ 2 lần' },
  { student_id: 'SV036', student_name: 'Đỗ Văn Hùng', major: 'Trí tuệ nhân tạo', alert_level: 'review' as const, triggered_signal_count: 2, headline: 'Điểm giảm liên tục 3 tuần' },
  { student_id: 'SV037', student_name: 'Tạ Thị Kim', major: 'Khoa học Máy tính', alert_level: 'review' as const, triggered_signal_count: 2, headline: 'Điểm số và đi học đều giảm' },
  { student_id: 'SV038', student_name: 'Võ Văn Long', major: 'Kỹ thuật Phần mềm', alert_level: 'review' as const, triggered_signal_count: 2, headline: 'Nộp bài trễ và vắng mặt nhiều' },
  { student_id: 'SV039', student_name: 'Thạch Thị Minh', major: 'Trí tuệ nhân tạo', alert_level: 'review' as const, triggered_signal_count: 2, headline: 'Điểm quiz giảm mạnh 3 tuần' },
  { student_id: 'SV026', student_name: 'Trần Thị Bình', major: 'Kỹ thuật Phần mềm', alert_level: 'watch' as const, triggered_signal_count: 1, headline: 'Vắng mặt 2 buổi liên tiếp' },
  { student_id: 'SV027', student_name: 'Vũ Thanh Giang', major: 'Khoa học Máy tính', alert_level: 'watch' as const, triggered_signal_count: 1, headline: 'Nộp bài trễ 2 bài gần nhất' },
  { student_id: 'SV029', student_name: 'Đặng Văn Kiên', major: 'Trí tuệ nhân tạo', alert_level: 'watch' as const, triggered_signal_count: 1, headline: 'Điểm quiz tuần trước thấp hơn' },
]

export const mockStats: OverviewStats = {
  total_students: 48,
  stable_count: 25,
  watch_count: 10,
  review_count: 5,
  insufficient_count: 4,
  improving_count: 4,
  weekly_trend: mockWeeklyTrend,
  major_distribution: mockMajorDistribution,
  signal_stats: mockSignalStats,
  priority_students: mockPriorityStudents,
}

export const mockStudents: StudentSummary[] = [
  // ── STABLE (25) ──
  { student_id: 'SV001', student_name: 'Nguyễn Văn An', major: 'Khoa học Máy tính', alert_level: 'stable', headline: 'Học tập ổn định, điểm số duy trì tốt', triggered_signal_count: 0, updated_at: '2026-07-17T14:00:00Z' },
  { student_id: 'SV002', student_name: 'Lê Hoàng Chương', major: 'Khoa học Máy tính', alert_level: 'stable', headline: 'Hoàn thành tốt tất cả bài kiểm tra', triggered_signal_count: 0, updated_at: '2026-07-17T10:00:00Z' },
  { student_id: 'SV003', student_name: 'Bùi Thị Lan', major: 'Khoa học Máy tính', alert_level: 'stable', headline: 'Điểm duy trì ổn định qua các tuần', triggered_signal_count: 0, updated_at: '2026-07-16T09:00:00Z' },
  { student_id: 'SV004', student_name: 'Mai Phương Nhi', major: 'Trí tuệ nhân tạo', alert_level: 'stable', headline: 'Hoàn thành tốt các bài kiểm tra gần đây', triggered_signal_count: 0, updated_at: '2026-07-16T13:00:00Z' },
  { student_id: 'SV005', student_name: 'Phạm Văn Phúc', major: 'Khoa học Máy tính', alert_level: 'stable', headline: 'Điểm số bình thường, không có thay đổi', triggered_signal_count: 0, updated_at: '2026-07-15T11:00:00Z' },
  { student_id: 'SV006', student_name: 'Đỗ Thị Hà', major: 'Kỹ thuật Phần mềm', alert_level: 'stable', headline: 'Tham gia đầy đủ các buổi học', triggered_signal_count: 0, updated_at: '2026-07-15T08:00:00Z' },
  { student_id: 'SV007', student_name: 'Vũ Minh Tuấn', major: 'Kỹ thuật Phần mềm', alert_level: 'stable', headline: 'Nộp bài đúng hạn, điểm khá tốt', triggered_signal_count: 0, updated_at: '2026-07-14T16:00:00Z' },
  { student_id: 'SV008', student_name: 'Ngô Thanh Hằng', major: 'Trí tuệ nhân tạo', alert_level: 'stable', headline: 'Học tập đều đặn, kết quả tốt', triggered_signal_count: 0, updated_at: '2026-07-14T10:00:00Z' },
  { student_id: 'SV009', student_name: 'Trịnh Văn Khoa', major: 'Khoa học Máy tính', alert_level: 'stable', headline: 'Không có thay đổi đáng chú ý', triggered_signal_count: 0, updated_at: '2026-07-13T09:00:00Z' },
  { student_id: 'SV010', student_name: 'Lý Thị Mai', major: 'Kỹ thuật Phần mềm', alert_level: 'stable', headline: 'Điểm số duy trì ở mức khá', triggered_signal_count: 0, updated_at: '2026-07-13T14:00:00Z' },
  { student_id: 'SV011', student_name: 'Hồ Quang Nam', major: 'Trí tuệ nhân tạo', alert_level: 'stable', headline: 'Tham gia tích cực các hoạt động nhóm', triggered_signal_count: 0, updated_at: '2026-07-12T11:00:00Z' },
  { student_id: 'SV012', student_name: 'Dương Thị Oanh', major: 'Khoa học Máy tính', alert_level: 'stable', headline: 'Kết quả thi giữa kỳ tốt', triggered_signal_count: 0, updated_at: '2026-07-12T08:00:00Z' },
  { student_id: 'SV013', student_name: 'Đinh Văn Phương', major: 'Kỹ thuật Phần mềm', alert_level: 'stable', headline: 'Ổn định qua các tuần học', triggered_signal_count: 0, updated_at: '2026-07-11T15:00:00Z' },
  { student_id: 'SV014', student_name: 'Tô Thị Quỳnh', major: 'Trí tuệ nhân tạo', alert_level: 'stable', headline: 'Nộp bài đúng hạn, điểm cao', triggered_signal_count: 0, updated_at: '2026-07-11T10:00:00Z' },
  { student_id: 'SV015', student_name: 'Cao Văn Rạng', major: 'Khoa học Máy tính', alert_level: 'stable', headline: 'Không có dấu hiệu bất thường', triggered_signal_count: 0, updated_at: '2026-07-10T09:00:00Z' },
  { student_id: 'SV016', student_name: 'Mạc Thị Sương', major: 'Kỹ thuật Phần mềm', alert_level: 'stable', headline: 'Điểm lab và quiz đều tốt', triggered_signal_count: 0, updated_at: '2026-07-10T14:00:00Z' },
  { student_id: 'SV017', student_name: 'Lưu Văn Tâm', major: 'Trí tuệ nhân tạo', alert_level: 'stable', headline: 'Hoạt động học tập bình thường', triggered_signal_count: 0, updated_at: '2026-07-09T11:00:00Z' },
  { student_id: 'SV018', student_name: 'Vương Thị Usa', major: 'Khoa học Máy tính', alert_level: 'stable', headline: 'Điểm số ổn định, không cần theo dõi', triggered_signal_count: 0, updated_at: '2026-07-09T08:00:00Z' },
  { student_id: 'SV019', student_name: 'Bạch Văn Vũ', major: 'Kỹ thuật Phần mềm', alert_level: 'stable', headline: 'Tham gia học đều đặn', triggered_signal_count: 0, updated_at: '2026-07-08T15:00:00Z' },
  { student_id: 'SV020', student_name: 'Phan Thị Xuân', major: 'Trí tuệ nhân tạo', alert_level: 'stable', headline: 'Kết quả tốt, không có thay đổi', triggered_signal_count: 0, updated_at: '2026-07-08T10:00:00Z' },
  { student_id: 'SV021', student_name: 'Khưu Văn Yến', major: 'Khoa học Máy tính', alert_level: 'stable', headline: 'Điểm duy trì tốt qua các kỳ', triggered_signal_count: 0, updated_at: '2026-07-07T09:00:00Z' },
  { student_id: 'SV022', student_name: 'Tăng Thị Ái', major: 'Kỹ thuật Phần mềm', alert_level: 'stable', headline: 'Không có dấu hiệu cần theo dõi', triggered_signal_count: 0, updated_at: '2026-07-07T14:00:00Z' },
  { student_id: 'SV023', student_name: 'Nguyễn Văn Bình', major: 'Trí tuệ nhân tạo', alert_level: 'stable', headline: 'Học tập chăm chỉ, kết quả ổn', triggered_signal_count: 0, updated_at: '2026-07-06T11:00:00Z' },
  { student_id: 'SV024', student_name: 'Lý Văn Cường', major: 'Khoa học Máy tính', alert_level: 'stable', headline: 'Điểm số tốt, đi học đầy đủ', triggered_signal_count: 0, updated_at: '2026-07-06T08:00:00Z' },
  { student_id: 'SV025', student_name: 'Trương Văn Dũng', major: 'Kỹ thuật Phần mềm', alert_level: 'stable', headline: 'Hoàn thành tốt các nhiệm vụ học tập', triggered_signal_count: 0, updated_at: '2026-07-05T15:00:00Z' },

  // ── WATCH (10) ──
  { student_id: 'SV026', student_name: 'Trần Thị Bình', major: 'Kỹ thuật Phần mềm', alert_level: 'watch', headline: 'Vắng mặt 2 buổi liên tiếp gần đây', triggered_signal_count: 1, updated_at: '2026-07-18T09:15:00Z' },
  { student_id: 'SV027', student_name: 'Vũ Thanh Giang', major: 'Khoa học Máy tính', alert_level: 'watch', headline: 'Nộp bài trễ ở 2 bài gần nhất', triggered_signal_count: 1, updated_at: '2026-07-18T08:00:00Z' },
  { student_id: 'SV028', student_name: 'Ngô Đạt Minh', major: 'Kỹ thuật Phần mềm', alert_level: 'watch', headline: 'Tần suất vắng mặt tăng nhẹ so với trước', triggered_signal_count: 1, updated_at: '2026-07-18T07:45:00Z' },
  { student_id: 'SV029', student_name: 'Đặng Văn Kiên', major: 'Trí tuệ nhân tạo', alert_level: 'watch', headline: 'Điểm quiz tuần trước thấp hơn bình thường', triggered_signal_count: 1, updated_at: '2026-07-17T16:00:00Z' },
  { student_id: 'SV030', student_name: 'Bành Thị Lệ', major: 'Khoa học Máy tính', alert_level: 'watch', headline: 'Nộp bài muộn 1 lần trong tuần này', triggered_signal_count: 1, updated_at: '2026-07-17T12:00:00Z' },
  { student_id: 'SV031', student_name: 'Chu Văn Minh', major: 'Kỹ thuật Phần mềm', alert_level: 'watch', headline: 'Vắng 1 buổi học lý thuyết', triggered_signal_count: 1, updated_at: '2026-07-16T14:00:00Z' },
  { student_id: 'SV032', student_name: 'Hà Thị Nga', major: 'Trí tuệ nhân tạo', alert_level: 'watch', headline: 'Điểm lab giảm nhẹ so với tuần trước', triggered_signal_count: 1, updated_at: '2026-07-16T10:00:00Z' },
  { student_id: 'SV033', student_name: 'Kim Văn Oai', major: 'Khoa học Máy tính', alert_level: 'watch', headline: 'Bài nộp gần nhất đến hạn muộn', triggered_signal_count: 1, updated_at: '2026-07-15T09:00:00Z' },
  { student_id: 'SV034', student_name: 'Lã Thị Phương', major: 'Kỹ thuật Phần mềm', alert_level: 'watch', headline: 'Tần suất nộp bài trễ tăng', triggered_signal_count: 1, updated_at: '2026-07-15T14:00:00Z' },
  { student_id: 'SV035', student_name: 'Ông Văn Quang', major: 'Trí tuệ nhân tạo', alert_level: 'watch', headline: 'Điểm danh có dấu hiệu giảm', triggered_signal_count: 1, updated_at: '2026-07-14T11:00:00Z' },

  // ── REVIEW (5) ──
  { student_id: 'SV036', student_name: 'Đỗ Văn Hùng', major: 'Trí tuệ nhân tạo', alert_level: 'review', headline: 'Điểm giảm liên tục 3 tuần, cần giáo viên xem xét', triggered_signal_count: 2, updated_at: '2026-07-18T11:30:00Z' },
  { student_id: 'SV037', student_name: 'Tạ Thị Kim', major: 'Khoa học Máy tính', alert_level: 'review', headline: 'Điểm số và đi học đều giảm đáng kể', triggered_signal_count: 2, updated_at: '2026-07-18T10:00:00Z' },
  { student_id: 'SV038', student_name: 'Võ Văn Long', major: 'Kỹ thuật Phần mềm', alert_level: 'review', headline: 'Nộp bài trễ và vắng mặt nhiều tuần này', triggered_signal_count: 2, updated_at: '2026-07-17T15:00:00Z' },
  { student_id: 'SV039', student_name: 'Thạch Thị Minh', major: 'Trí tuệ nhân tạo', alert_level: 'review', headline: 'Điểm quiz giảm mạnh 3 tuần liên tiếp', triggered_signal_count: 2, updated_at: '2026-07-17T09:00:00Z' },
  { student_id: 'SV040', student_name: 'Tôn Văn Nghĩa', major: 'Khoa học Máy tính', alert_level: 'review', headline: 'Vắng mặt 3 buổi và nộp bài trễ 2 lần', triggered_signal_count: 3, updated_at: '2026-07-16T14:00:00Z' },

  // ── IMPROVING (4) ──
  { student_id: 'SV041', student_name: 'Phạm Minh Đức', major: 'Trí tuệ nhân tạo', alert_level: 'improving', headline: 'Điểm số cải thiện rõ rệt sau thời gian khó khăn', triggered_signal_count: 0, updated_at: '2026-07-17T11:00:00Z' },
  { student_id: 'SV042', student_name: 'Trịnh Quốc Bảo', major: 'Khoa học Máy tính', alert_level: 'improving', headline: 'Điểm danh cải thiện rõ rệt sau buổi trò chuyện', triggered_signal_count: 0, updated_at: '2026-07-17T15:30:00Z' },
  { student_id: 'SV043', student_name: 'Diệp Văn Phong', major: 'Kỹ thuật Phần mềm', alert_level: 'improving', headline: 'Nộp bài đúng hạn trở lại sau 2 tuần trễ', triggered_signal_count: 0, updated_at: '2026-07-16T12:00:00Z' },
  { student_id: 'SV044', student_name: 'Giang Thị Thu', major: 'Trí tuệ nhân tạo', alert_level: 'improving', headline: 'Điểm quiz tuần này tốt hơn đáng kể', triggered_signal_count: 0, updated_at: '2026-07-15T10:00:00Z' },

  // ── INSUFFICIENT DATA (4) ──
  { student_id: 'SV045', student_name: 'Hoàng Thị Em', major: 'Kỹ thuật Phần mềm', alert_level: 'insufficient_data', headline: 'Chưa đủ dữ liệu để đánh giá', triggered_signal_count: 0, updated_at: '2026-07-16T16:00:00Z' },
  { student_id: 'SV046', student_name: 'Lý Thùy Dung', major: 'Kỹ thuật Phần mềm', alert_level: 'insufficient_data', headline: 'Mới nhập học, cần thêm thời gian đánh giá', triggered_signal_count: 0, updated_at: '2026-07-15T10:00:00Z' },
  { student_id: 'SV047', student_name: 'Nghiêm Văn Tài', major: 'Trí tuệ nhân tạo', alert_level: 'insufficient_data', headline: 'Chưa đủ bài kiểm tra để phân tích', triggered_signal_count: 0, updated_at: '2026-07-14T08:00:00Z' },
  { student_id: 'SV048', student_name: 'Lâm Thị Uyên', major: 'Khoa học Máy tính', alert_level: 'insufficient_data', headline: 'Vừa chuyển ngành, chưa có đủ dữ liệu', triggered_signal_count: 0, updated_at: '2026-07-13T09:00:00Z' },
]

// ── Chi tiết cho SV036 (review) ──
export const mockStudentDetail: StudentDetail = {
  student_id: 'SV001',
  student_name: 'Nguyễn Văn A',
  major: 'Khoa học Máy tính',
  cgpa: 8.2,
  total_credits: 75,
  alert_level: 'stable',
  headline: 'Điểm giảm liên tục 3 tuần, cần giáo viên xem xét',
  signals: [
    {
      signal_type: 'grade',
      is_triggered: true,
      data_sufficiency: 'sufficient',
      explanation:
        'Điểm quiz các tuần gần đây thấp hơn đáng kể so với mức bình thường của em. Trước đây em thường đạt 7-8 điểm, nhưng 3 tuần gần nhất chỉ còn 4-5 điểm.',
    },
    {
      signal_type: 'attendance',
      is_triggered: true,
      data_sufficiency: 'sufficient',
      explanation:
        'Em đã vắng mặt 3 buổi trong 2 tuần gần đây, trong khi trước đó em đi học đều đặn.',
    },
    {
      signal_type: 'submission',
      is_triggered: false,
      data_sufficiency: 'sufficient',
      explanation:
        'Em vẫn nộp bài đúng hạn, tuy nhiên chất lượng bài nộp có giảm nhẹ.',
    },
  ],
  timeline: [
    { week: '2026-W06', grade_value: 0.85, attendance_value: 0.95, submission_value: 1.0 },
    { week: '2026-W07', grade_value: 0.80, attendance_value: 0.90, submission_value: 1.0 },
    { week: '2026-W08', grade_value: 0.78, attendance_value: 0.85, submission_value: 0.9 },
    { week: '2026-W09', grade_value: 0.65, attendance_value: 0.70, submission_value: 0.9 },
    { week: '2026-W10', grade_value: 0.50, attendance_value: 0.60, submission_value: 0.8 },
    { week: '2026-W11', grade_value: 0.42, attendance_value: 0.55, submission_value: 0.9 },
    { week: '2026-W12', grade_value: 0.38, attendance_value: 0.50, submission_value: 0.85 },
  ],
  alert_history: [
    {
      date: '2026-07-18T11:30:00Z',
      level: 'review',
      headline: 'Điểm giảm và vắng mặt nhiều',
      details: [
        'Điểm quiz W10-W12 giảm 45% so với baseline',
        'Vắng mặt 3 buổi trong 2 tuần',
        'Cần giáo viên liên hệ và hỗ trợ',
      ],
    },
    {
      date: '2026-07-11T09:00:00Z',
      level: 'watch',
      headline: 'Bắt đầu có dấu hiệu giảm',
      details: ['Điểm quiz W09 thấp hơn bình thường', 'Vắng 1 buổi học'],
    },
    {
      date: '2026-07-04T09:00:00Z',
      level: 'stable',
      headline: 'Học tập bình thường',
      details: ['Điểm số ổn định', 'Điểm danh đầy đủ'],
    },
  ],
  courses: [
    {
      course_id: "CS101",
      course_name: "Nhập môn Lập trình",
      semester: 1,
      grades: [
          { assessment: 'Lab 1', score: 8.0, class_average: 7.5 },
          { assessment: 'Lab 2', score: 7.5, class_average: 7.0 },
          { assessment: 'Midterm', score: 8.5, class_average: 7.0 },
      ],
      attendance_rate: 0.8
    }
  ],
  is_seasonal_suppressed: false,
}
