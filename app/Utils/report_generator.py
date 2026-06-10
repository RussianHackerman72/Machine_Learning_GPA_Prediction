from Utils.predictor import predict_students
from Utils.advisor import analyze_student
from Utils.simulator import generate_improvement_plans

def generate_student_report(student):
    score = predict_students(student)

    analysis = analyze_student(student, score)

    plans = generate_improvement_plans(student, predict_students)


    return {
        "Prediction": analysis,
        "Improvement Plans": plans
    }