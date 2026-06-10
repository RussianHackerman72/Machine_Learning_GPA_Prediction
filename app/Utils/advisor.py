
def getPerformanceCategory(score):

    if score >= 90:
        return "Excellent"
    
    elif score >= 80:
        return "Very Good"
    
    elif score >= 70:
        return "Good"
    
    elif score >= 60:
        return "Fair"
    
    else:
        return "Can be Improved further..."
    

def getStrengths(student):

    strengths = []

    if student["Attendance"] >= 90:
        strengths.append("Excellent Attendance")

    if student["Previous_GPA"] >= 3.5:
        strengths.append("Strong Academic History")

    if student["Sleep_Hours"] >= 7:
        strengths.append("Healthy Sleep Habits")

    if student["Tutoring_Sessions_Per_Week"] >= 2:
        strengths.append("Actively seeks academic support on your own")

    study_efficiency = (
        student["Hours_Studied"] / (student["Stress_Level"] + 1)
    )

    if study_efficiency >= 1:
        strengths.append("Efficient Study Habits")

    return strengths

def getWeaknesses(student):
    
    weaknesses = []

    if student["Attendance"] < 75:
        weaknesses.append("Low Attendance")

    if student["Stress_Level"] >= 7:
        weaknesses.append("High Stress Levels")

    if student["Sleep_Hours"] < 6:
        weaknesses.append("Unhealthy Sleep Habits")

    if student["Screen_Time"] > 6:
        weaknesses.append("Excessive unproductive screen time")

    if student["Exam_Anxiety_Score"] >= 7:
        weaknesses.append("High Anxiety regarding Exams")

    study_efficiency = (
        student["Hours_Studied"] / (student["Stress_Level"] + 1)
    )

    if study_efficiency < 0.5:
        weaknesses.append("Low Study Efficiency")

    return weaknesses


def getRecommendations(student):
    
    recommendations = []

    if student["Attendance"] < 75:
        recommendations.append("You should try to attend more classes when you can")

    if student["Stress_Level"] >= 7:
        recommendations.append("You should practice stress management or reduction techniques")

    if student["Sleep_Hours"] < 6:
        recommendations.append("You should aim for a daily average of 7-8 hours of sleep per night")

    if student["Screen_Time"] > 6:
        recommendations.append("You should reduce your unproductive screen time")

    if student["Tutoring_Sessions_Per_Week"] == 0:
        recommendations.append("You should Consider attending extra lessons or tutoring sessions")
    
    if student["Hours_Studied"] < 4:
        recommendations.append("Gradually Increase your daily study times")

    return recommendations

def analyze_student(student, pred_score):


    return {
        "score": pred_score,
        "category": getPerformanceCategory(pred_score),
        "strengths": getStrengths(student),
        "weaknesses": getWeaknesses(student),
        "recommendations": getRecommendations(student)

    }   



    