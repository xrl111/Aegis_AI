import pandas as pd
from typing import List
from datetime import datetime

from src.input.loader import DataLoader
from src.normalize import normalize_grades, normalize_attendance, normalize_submissions
from src.merge import merge_cross_course_grades, merge_cross_course_attendance
from src.baseline import check_data_sufficiency
from src.detection import (
    compute_grade_signal, 
    compute_attendance_signal, 
    compute_submission_signal,
    evaluate_fusion,
    check_seasonal_suppression
)
from src.alert import determine_alert_level, explain_grade_signal, explain_attendance_signal, explain_submission_signal
from src.exceptions import InsufficientDataError
from api.schemas import StudentSummary, StudentDetail, SignalOut, TimelinePoint

# Giả định đường dẫn data (trong thực tế có thể dùng config)
DATA_DIR = "data/sample"

class StudentService:
    def __init__(self):
        self.loader = DataLoader(DATA_DIR)
        self.df_students = self.loader.load_students()
        self.df_courses = self.loader.load_courses()
        self.df_grades = self.loader.load_grades()
        self.df_attendance = self.loader.load_attendance()
        
        # 1. Normalize All
        self.norm_grades = normalize_grades(self.df_grades)
        self.norm_attendance = normalize_attendance(self.df_attendance)
        
        # 2. Merge All
        self.merged_grades = merge_cross_course_grades(self.norm_grades)
        self.merged_attendance = merge_cross_course_attendance(self.norm_attendance)

    def get_all_students(self) -> List[StudentSummary]:
        summaries = []
        for _, student in self.df_students.iterrows():
            student_id = student["student_id"]
            
            # Tính detail để lấy alert_level (hơi chậm nếu data lớn, nhưng OK cho sample)
            try:
                detail = self.get_student_detail(student_id)
                summary = StudentSummary(
                    student_id=student_id,
                    student_name=student["name"],
                    major=student["major"],
                    alert_level=detail.alert_level,
                    headline=detail.headline,
                    triggered_signal_count=sum(1 for s in detail.signals if s.is_triggered),
                    updated_at=datetime.utcnow()
                )
            except Exception:
                # Fallback if something fails completely
                summary = StudentSummary(
                    student_id=student_id,
                    student_name=student["name"],
                    major=student["major"],
                    alert_level="insufficient_data",
                    headline="Lỗi xử lý dữ liệu",
                    triggered_signal_count=0,
                    updated_at=datetime.utcnow()
                )
            summaries.append(summary)
            
        return summaries

    def get_student_detail(self, student_id: str) -> StudentDetail:
        student_info = self.df_students[self.df_students["student_id"] == student_id].iloc[0]
        
        # Extract student's merged data
        s_grades = self.merged_grades[self.merged_grades["student_id"] == student_id]
        s_att = self.merged_attendance[self.merged_attendance["student_id"] == student_id]
        
        signals_out = []
        is_seasonal = False # Giả định đơn giản cho demo
        
        # --- GRADE SIGNAL ---
        grade_signal_result = None
        try:
            check_data_sufficiency(s_grades, student_id, "grade", 3)
            # Truyền Series normalized_score
            g_res = compute_grade_signal(s_grades["merged_score"])
            grade_signal_result = g_res
            signals_out.append(SignalOut(
                signal_type="grade",
                is_triggered=g_res["is_triggered"],
                data_sufficiency=g_res["data_sufficiency"],
                explanation=explain_grade_signal(g_res)
            ))
        except InsufficientDataError:
            grade_signal_result = {"is_triggered": False, "z_score": 0.0, "data_sufficiency": "insufficient"}
            signals_out.append(SignalOut(
                signal_type="grade",
                is_triggered=False,
                data_sufficiency="insufficient",
                explanation="Chưa đủ dữ liệu điểm số."
            ))
            
        # --- ATTENDANCE SIGNAL ---
        att_signal_result = None
        try:
            check_data_sufficiency(s_att, student_id, "attendance", 3)
            current_rate = float(s_att.iloc[-1]["merged_rate"])
            a_res = compute_attendance_signal(current_rate)
            att_signal_result = a_res
            signals_out.append(SignalOut(
                signal_type="attendance",
                is_triggered=a_res["is_triggered"],
                data_sufficiency=a_res["data_sufficiency"],
                explanation=explain_attendance_signal(a_res)
            ))
        except InsufficientDataError:
            att_signal_result = {"is_triggered": False, "current_rate": 0.0, "data_sufficiency": "insufficient"}
            signals_out.append(SignalOut(
                signal_type="attendance",
                is_triggered=False,
                data_sufficiency="insufficient",
                explanation="Chưa đủ dữ liệu điểm danh."
            ))
            
        # --- SUBMISSION SIGNAL (Stub) ---
        sub_res = compute_submission_signal(1.0) # Fake perfect submissions
        signals_out.append(SignalOut(
            signal_type="submission",
            is_triggered=sub_res["is_triggered"],
            data_sufficiency=sub_res["data_sufficiency"],
            explanation=explain_submission_signal(sub_res)
        ))
        
        # --- FUSION & ALERT LEVEL ---
        fusion = evaluate_fusion(grade_signal_result, att_signal_result, sub_res)
        
        alert_level = determine_alert_level(
            triggered_count=fusion["triggered_count"],
            is_seasonal_suppressed=is_seasonal,
            previous_level="stable"
        )
        
        # Nếu cả điểm và danh đều thiếu -> insufficient_data
        if grade_signal_result["data_sufficiency"] == "insufficient" and att_signal_result["data_sufficiency"] == "insufficient":
            alert_level = "insufficient_data"
            
        # --- HEADLINE GENERATION ---
        headline = self._generate_headline(alert_level)
        
        # --- TIMELINE ---
        timeline = self._build_timeline(s_grades, s_att)

        return StudentDetail(
            student_id=student_id,
            student_name=student_info["name"],
            major=student_info["major"],
            alert_level=alert_level,
            headline=headline,
            signals=signals_out,
            timeline=timeline,
            alert_history=[],
            is_seasonal_suppressed=is_seasonal
        )
        
    def _generate_headline(self, level: str) -> str:
        if level == "stable":
            return "Học sinh đang duy trì kết quả ổn định."
        elif level == "watch":
            return "Có sự sụt giảm nhẹ, cần theo dõi thêm."
        elif level == "review":
            return "Sụt giảm nghiêm trọng hoặc nhiều tín hiệu xấu cùng lúc."
        elif level == "improving":
            return "Có dấu hiệu cải thiện so với tuần trước."
        else:
            return "Chưa đủ dữ liệu hệ thống để đánh giá."
            
    def _build_timeline(self, s_grades: pd.DataFrame, s_att: pd.DataFrame) -> List[TimelinePoint]:
        # Tạo một timeline map đơn giản dựa trên index (giả lập tuần)
        timeline_dict = {}
        
        for i, row in s_grades.iterrows():
            idx = str(row["assessment"])
            timeline_dict[idx] = {"week": f"Week_{idx}", "grade_value": float(row["merged_score"])}
            
        # Trộn attendance (dùng session map sang week tương đối)
        for i, row in s_att.iterrows():
            sess = row["session"]
            # Map session 1-18 to 6 weeks (3 sessions/week)
            week_idx = ((int(sess) - 1) // 3) + 1
            idx = f"W{week_idx}"
            
            if idx not in timeline_dict:
                timeline_dict[idx] = {"week": f"Week_{idx}"}
            timeline_dict[idx]["attendance_value"] = float(row["merged_rate"])
            
        # Convert dict to list
        pts = []
        for v in timeline_dict.values():
            pts.append(TimelinePoint(
                week=v.get("week"),
                grade_value=v.get("grade_value"),
                attendance_value=v.get("attendance_value"),
                submission_value=None
            ))
            
        return pts
