from app.Utils.predictor import predict_students
from app.Utils.advisor import getStrengths, getPerformanceCategory, analyze_student
from app.Utils.simulator import simulate_change, find_best_improvements, simulate_improvement_plan, generate_improvement_plans
from app.Utils.report_generator import generate_student_report

student = {
    "Age": 20,
    "Gender": "Male",
    "Hours_Studied": 5,
    "Attendance": 83,
    "Sleep_Hours": 6,
    "Stress_Level": 4,
    "Screen_Time": 3,
    "Previous_GPA": 3.5,
    "Part_Time_Job": "No",
    "Study_Method": "Online",
    "Diet_Quality": "Good",
    "Internet_Quality": "Good",
    "Extracurricular": "Yes",
    "Tutoring_Sessions_Per_Week": 2,
    "Family_Income_Level": "Medium",
    "Exam_Anxiety_Score": 4
}

student_struggling = {
    "Age": 20,
    "Gender": "Male",
    "Hours_Studied": 5,
    "Attendance": 83,
    "Sleep_Hours": 6,
    "Stress_Level": 4,
    "Screen_Time": 7,
    "Previous_GPA": 3.23,
    "Part_Time_Job": "No",
    "Study_Method": "Hybrid",
    "Diet_Quality": "Good",
    "Internet_Quality": "Good",
    "Extracurricular": "Yes",
    "Tutoring_Sessions_Per_Week": 2,
    "Family_Income_Level": "Medium",
    "Exam_Anxiety_Score": 6
}

score = predict_students(student)

report = generate_student_report(student_struggling)

print(report)