DISPLAY_NAMES = {

    "Hours_Studied":
        "Study Hours",

    "Sleep_Hours":
        "Sleep Duration",

    "Stress_Level":
        "Stress Level",

    "Attendance":
        "Attendance",

    "Tutoring_Sessions_Per_Week":
        "Tutoring Sessions"
}

FEATURE_CAPS = {
    "Hours_Studied": 6,
    "Sleep_Hours": 8,
    "Stress_Level": 3,
    "Attendance": 95,
    "Tutoring_Sessions_Per_Week": 2
}

def needs_improvement(student, feature):
    cap = FEATURE_CAPS[feature]

    value = student[feature]

    if feature == "Stress_Level":
        return value > cap
    
    return value < cap

def clamp(value, minimum, maximum):
    return max(minimum, min(value, maximum))

def build_conservative_plan(student):

    plan = {}

    if needs_improvement(student, "Hours_Studied"):
        plan["Hours_Studied"] = clamp(
            student["Hours_Studied"] + 1,
            0,
            FEATURE_CAPS["Hours_Studied"]
        )

    if needs_improvement(student, "Sleep_Hours"):
        plan["Sleep_Hours"] = clamp(
            student["Sleep_Hours"] + 1,
            0,
            FEATURE_CAPS["Sleep_Hours"]
        )

    if needs_improvement(student, "Stress_Level"):
        plan["Stress_Level"] = clamp(
            student["Stress_Level"] - 1,
            FEATURE_CAPS["Stress_Level"],
            10
        )

    if needs_improvement(student, "Attendance"):
        plan["Attendance"] = clamp(
            student["Attendance"] + 2,
            0,
            FEATURE_CAPS["Attendance"]
        )

    if needs_improvement(student, "Tutoring_Sessions_Per_Week"):
        plan["Tutoring_Sessions_Per_Week"] = clamp(
            student["Tutoring_Sessions_Per_Week"] + 1,
            0,
            FEATURE_CAPS["Tutoring_Sessions_Per_Week"]
        )

    return plan

def build_moderate_plan(student):

    plan = {}

    if needs_improvement(student, "Hours_Studied"):
        plan["Hours_Studied"] = clamp(
            student["Hours_Studied"] + 2,
            0,
            FEATURE_CAPS["Hours_Studied"]
        )

    if needs_improvement(student, "Sleep_Hours"):
        plan["Sleep_Hours"] = clamp(
            student["Sleep_Hours"] + 2,
            0,
            FEATURE_CAPS["Sleep_Hours"]
        )

    if needs_improvement(student, "Stress_Level"):
        plan["Stress_Level"] = clamp(
            student["Stress_Level"] - 2,
            FEATURE_CAPS["Stress_Level"],
            10
        )

    if needs_improvement(student, "Attendance"):
        plan["Attendance"] = clamp(
            student["Attendance"] + 5,
            0,
            FEATURE_CAPS["Attendance"]
        )

    if needs_improvement(student, "Tutoring_Sessions_Per_Week"):
        plan["Tutoring_Sessions_Per_Week"] = clamp(
            student["Tutoring_Sessions_Per_Week"] + 1,
            0,
            FEATURE_CAPS["Tutoring_Sessions_Per_Week"]
        )

    return plan

def build_ambitious_plan(student):

    plan = {}

    if needs_improvement(student, "Hours_Studied"):
        plan["Hours_Studied"] = clamp(
            student["Hours_Studied"] + 3,
            0,
            FEATURE_CAPS["Hours_Studied"]
        )

    if needs_improvement(student, "Sleep_Hours"):
        plan["Sleep_Hours"] = clamp(
            student["Sleep_Hours"] + 3,
            0,
            FEATURE_CAPS["Sleep_Hours"]
        )

    if needs_improvement(student, "Stress_Level"):
        plan["Stress_Level"] = clamp(
            student["Stress_Level"] - 3,
            FEATURE_CAPS["Stress_Level"],
            10
        )

    if needs_improvement(student, "Attendance"):
        plan["Attendance"] = clamp(
            student["Attendance"] + 10,
            0,
            FEATURE_CAPS["Attendance"]
        )

    if needs_improvement(student, "Tutoring_Sessions_Per_Week"):
        plan["Tutoring_Sessions_Per_Week"] = clamp(
            student["Tutoring_Sessions_Per_Week"] + 2,
            0,
            FEATURE_CAPS["Tutoring_Sessions_Per_Week"]
        )

    return plan



def simulate_change(student, feature, newValue, predictor):

    modified = student.copy()
    modified[feature] = newValue
    current_score = predictor(student)
    new_score = predictor(modified)
    gain = new_score - current_score

    return {
        "feature": feature,
        "current_value": student[feature],
        "suggested_value": newValue, 
        "current_score": round(float(current_score), 2),
        "new_score": round(float(new_score), 2),
        "gain": round(float(gain), 2)
    }

def find_best_improvements(student, predictor):

    candidate_changes = {}

    if student["Sleep_Hours"] < 8:
        candidate_changes["Sleep_Hours"] = 8

    if student["Attendance"] < 95:
        candidate_changes["Attendance"] = 95

    if student["Stress_Level"] > 3:
        candidate_changes["Stress_Level"] = 3

    if student["Hours_Studied"] < 6:
        candidate_changes["Hours_Studied"] = 6

    if student["Tutoring_Sessions_Per_Week"] < 2:
        candidate_changes["Sleep_Hours"] = 2
    

    results = []

    for feature, target in candidate_changes.items():
        result = simulate_change(student, feature, target, predictor)

        results.append(result)

    results.sort(key=lambda x: x["gain"], reverse=True)

    return results[:3]

def simulate_improvement_plan(student, predictor):
    improved_student = student.copy()

    changes = []

    if student["Hours_Studied"] < 6:
        old = student["Hours_Studied"]
        improved_student["Hours_Studied"] = 6
        changes.append(f"Increase Study Hours from {old} to 6")

    if student["Sleep_Hours"] < 8:
        old = student["Sleep_Hours"]
        improved_student["Sleep_Hours"] = 8
        changes.append(f"Increase Sleep Hours from {old} to 8")

    if student["Stress_Level"] > 3:
        old = student["Stress_Level"]
        improved_student["Stress_Level"] = 3
        changes.append(f"Reduce Stress Levels from {old} to 3")

    if student["Attendance"] < 95:
        old = student["Attendance"]
        improved_student["Attendance"] = 95
        changes.append(f"Increase Attendance from {old}% to 95%")

    if student["Tutoring_Sessions_Per_Week"] < 2:
        old = student["Tutoring_Sessions_Per_Week"]
        improved_student["Tutoring_Sessions_Per_Week"] = 2
        changes.append(f"Increase weekly Tutoring Sessions from {old} to 2")

    current_score = predictor(student)
    improved_score = predictor(improved_student)

    gain = improved_score - current_score

    return {
        "current_score": round(float(current_score), 2),
        "improved_score": round(float(improved_score), 2),
        "gain": round(float(gain), 2),
        "changes": changes
    }

def simulate_plan(student, predictor, plan_name, target_values):

    improved_student = student.copy()

    changes = []

    for feature, target in target_values.items():
        current = student[feature]
        if feature == "Stress_Level":
            if current > target: 
                improved_student[feature] = target
                
                display_name = DISPLAY_NAMES.get(feature, feature)

                changes.append(f"{display_name}: {current} -> {target}")

        else:
            if current < target:
                improved_student[feature] = target

                display_name = DISPLAY_NAMES.get(feature, feature)

                changes.append(f"{display_name}: {current} -> {target}")

    current_score = predictor(student)
    improved_score = predictor(improved_student)

    return {
        "plan": plan_name,
        "current_score": round(float(current_score), 2),
        "improved_score": round(float(improved_score), 2),
        "gain": round(float(improved_score - current_score), 2),
        "changes": changes
    }

CONSERVATIVE_PLAN = {
    "Hours_Studied": 4,
    "Sleep_Hours": 7,
    "Stress_Level": 5,
    "Attendance": 85,
    "Tutoring_Sessions_Per_Week": 1
}

MODERATE_PLAN = {
    "Hours_Studied": 5,
    "Sleep_Hours": 7,
    "Stress_Level": 4,
    "Attendance": 90,
    "Tutoring_Sessions_Per_Week": 1
}

AMBITIOUS_PLAN = {
    "Hours_Studied": 6,
    "Sleep_Hours": 8,
    "Stress_Level": 3,
    "Attendance": 95,
    "Tutoring_Sessions_Per_Week": 2
}

def generate_improvement_plans(student, predictor):
    conservative = build_conservative_plan(student)
    moderate = build_moderate_plan(student)
    ambitious = build_ambitious_plan(student)


    plans = []

    plans.append(simulate_plan(
        student,
        predictor,
        "Conservative",
        conservative
        )
    )

    plans.append(simulate_plan(
        student,
        predictor,
        "Moderate",
        moderate
        )
    )

    plans.append(simulate_plan(
        student,
        predictor,
        "Ambitious",
        ambitious
        )
    )

    for plan in plans:
        print(plan['plan'])
        print(plan['changes'])
        print(plan['gain'])
        print()

    return plans


    

    