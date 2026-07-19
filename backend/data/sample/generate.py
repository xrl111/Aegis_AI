import pandas as pd
import numpy as np
import random
import os

# Set seed for reproducibility
np.random.seed(42)
random.seed(42)

def generate_sample_data(output_dir="backend/data/sample"):
    os.makedirs(output_dir, exist_ok=True)
    
    # 1. Generate Students
    num_normal = 15
    scenarios = ["gradual_decline", "gradual_decline", "sudden_drop", "consistent", "missing_data"]
    total_students = num_normal + len(scenarios)
    
    students_data = []
    student_behaviors = {}
    
    for i in range(1, total_students + 1):
        sid = f"SV{i:03d}"
        if i <= num_normal:
            behavior = "normal"
        else:
            behavior = scenarios[i - num_normal - 1]
            
        students_data.append({
            "student_id": sid,
            "name": f"Nguyễn Văn {chr(64+i) if i <= 26 else str(i)}",
            "major": "IT"
        })
        student_behaviors[sid] = behavior
        
    df_students = pd.DataFrame(students_data)
    df_students.to_csv(os.path.join(output_dir, "students.csv"), index=False, encoding="utf-8-sig")
    
    # 2. Generate Courses (Semester 2 only since Semester 1 is baseline, but let's generate both to have a baseline)
    # Actually, the user requirement says "bắt đầu dự báo từ kỳ 2 vì kỳ đầu chưa có dữ liệu nền".
    # So we need data for Sem 1 (Baseline) and Sem 2 (Current).
    courses_data = [
        {"course_id": "PRJ301", "course_name": "Java Web", "semester": 1},
        {"course_id": "DBI202", "course_name": "Databases", "semester": 1},
        {"course_id": "SWE201", "course_name": "Software Eng", "semester": 1},
        {"course_id": "SWT301", "course_name": "Software Testing", "semester": 2},
        {"course_id": "PRM392", "course_name": "Mobile Dev", "semester": 2},
        {"course_id": "ITE302", "course_name": "Ethics", "semester": 2},
        {"course_id": "WED201", "course_name": "Web Design", "semester": 2},
        {"course_id": "PRO192", "course_name": "OOP with Java", "semester": 2},
    ]
    df_courses = pd.DataFrame(courses_data)
    df_courses.to_csv(os.path.join(output_dir, "courses.csv"), index=False, encoding="utf-8-sig")
    
    # 3 & 4. Generate Grades and Attendance
    assessments = [
        "Lab_1", "Quiz_1", "Lab_2", "Quiz_2", 
        "ASM_1", "Lab_3", "Quiz_3", "Lab_4", 
        "Quiz_4", "ASM_2", "Final"
    ]
    
    grades_data = []
    attendance_data = []
    
    for sid, behavior in student_behaviors.items():
        if behavior == "missing_data":
            # Student enrolled but only attended 2 sessions and did 1 lab
            for c in courses_data:
                cid = c["course_id"]
                grades_data.append({"student_id": sid, "course_id": cid, "assessment": "Lab_1", "score": 5.0})
                attendance_data.append({"student_id": sid, "course_id": cid, "session": 1, "status": "Present"})
                attendance_data.append({"student_id": sid, "course_id": cid, "session": 2, "status": "Present"})
            continue
            
        for c in courses_data:
            cid = c["course_id"]
            sem = c["semester"]
            
            # Baseline score based on behavior
            base_score = 7.0 + np.random.normal(0, 0.5) if behavior != "consistent" else 8.0
            
            # Generate Grades
            for i, asm in enumerate(assessments):
                # Calculate specific score
                score = base_score + np.random.normal(0, 0.5)
                
                if behavior == "consistent":
                    score = 8.0  # Exactly same score to test MAD floor
                    
                if sem == 2:
                    if behavior == "gradual_decline":
                        score -= (i * 0.4) # gradually drop over time
                    elif behavior == "sudden_drop" and i >= 6: # drop after week 3 (mid term)
                        score -= 5.0
                        
                # clamp
                score = max(0.0, min(10.0, score))
                
                grades_data.append({
                    "student_id": sid,
                    "course_id": cid,
                    "assessment": asm,
                    "score": round(score, 1)
                })
                
            # Generate Attendance
            for sess in range(1, 19):
                status = "Present"
                prob_absent = 0.05
                
                if behavior == "consistent":
                    prob_absent = 0.0
                
                if sem == 2:
                    if behavior == "gradual_decline":
                        prob_absent = 0.05 + (sess * 0.03)
                    elif behavior == "sudden_drop" and sess >= 10:
                        prob_absent = 0.8
                        
                r = random.random()
                if r < prob_absent:
                    status = "Absent"
                elif r < prob_absent + 0.05 and behavior != "consistent":
                    status = "Late"
                    
                attendance_data.append({
                    "student_id": sid,
                    "course_id": cid,
                    "session": sess,
                    "status": status
                })

    df_grades = pd.DataFrame(grades_data)
    df_grades.to_csv(os.path.join(output_dir, "grades.csv"), index=False, encoding="utf-8-sig")
    
    df_att = pd.DataFrame(attendance_data)
    df_att.to_csv(os.path.join(output_dir, "attendance.csv"), index=False, encoding="utf-8-sig")

    print(f"Generated data for {len(student_behaviors)} students across {len(courses_data)} courses in {output_dir}")

if __name__ == "__main__":
    generate_sample_data()
