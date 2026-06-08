from app.Utils.predictor import predict_students
from app.Utils.advisor import getStrengths, getPerformanceCategory, analyze_student
from app.Utils.simulator import simulate_change, find_best_improvements, simulate_improvement_plan, generate_improvement_plans
from app.Utils.report_generator import generate_student_report

student = {
    "Age": 20,
    "Gender": "Male",
    "Hours_Studied": 5,
    "Attendance": 90,
    "Sleep_Hours": 7,
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
    "Hours_Studied": 3,
    "Attendance": 75,
    "Sleep_Hours": 4,
    "Stress_Level": 6,
    "Screen_Time": 7,
    "Previous_GPA": 2.7,
    "Part_Time_Job": "No",
    "Study_Method": "Online",
    "Diet_Quality": "Good",
    "Internet_Quality": "Good",
    "Extracurricular": "Yes",
    "Tutoring_Sessions_Per_Week": 0,
    "Family_Income_Level": "Medium",
    "Exam_Anxiety_Score": 6
}

score = predict_students(student)

report = generate_student_report(student_struggling)

print(report)