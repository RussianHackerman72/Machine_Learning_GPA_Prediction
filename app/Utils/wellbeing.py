def academic_score(student):
    attendance = student["Attendance"]
    prev_gpa = student["Previous_GPA"]
    hours_studied = student["Hours_Studied"]
    tutoring = student["Tutoring_Sessions_Per_Week"]

    attendance_score = attendance
    gpa_score = (prev_gpa / 4.0) * 100
    study_score = min(hours_studied / 10 * 100, 100)
    tutoring_score = min(tutoring / 5 * 100, 100)

    return round((attendance_score*0.3) + (gpa_score*0.3) + (study_score*0.25) + (tutoring_score*0.15), 1)

def wellbeing_score(student):
    sleep = student["Sleep_Hours"]
    stress = student["Stress_Level"]
    exam_anxiety = student["Exam_Anxiety_Score"] 

    sleep_score = max(0, 100-abs(sleep-8)*15)
    stress_score = 100 - ((stress-1)/9 * 100)
    anxiety_score = 100 - ((exam_anxiety-1)/9*100)



    return round((sleep_score*0.35) +  (stress_score*0.35) + (anxiety_score*0.3), 1)

def score_category(score):
    if score >= 85:
        return "Excellent"

    elif score >= 70:
        return "Good"

    elif score >= 55:
        return "Moderate"

    return "Needs Attention"




