import pickle
import pandas as pd 

with open("models/best_xgboost_model.pkl", "rb") as f:
    model = pickle.load(f)

with open("models/model_features.pkl", "rb") as f:
    model_features = pickle.load(f)

def createEngineeredFeatures(df):
    
    df["Study_Efficiency"] = (
        df["Hours_Studied"]
        / (df["Stress_Level"] + 1)
    )

    df["Sleep_Study_Balance"] = (
        df["Sleep_Hours"]
        * df["Hours_Studied"]
    )

    df["Anxiety_Attendance"] = (
        df["Exam_Anxiety_Score"]
        * df["Attendance"]
    )

    df["Academic_Consistency"] = (
        df["Previous_GPA"]
        / df["Attendance"]
    )

    df["Productivity_Score"] = (
        df["Hours_Studied"]
        + df["Attendance"] / 10
        + df["Sleep_Hours"]
    )

    df["Stress_per_Study_Hour"] = (
        df["Stress_Level"]
        / (df["Hours_Studied"] + 1)
    )

    return df

def predict_students(student_data):
    df = pd.DataFrame([student_data])
    df = createEngineeredFeatures(df)

    df = pd.get_dummies(
        df,
        drop_first=True,
        dtype=int
    )

    df = df.reindex(
        columns=model_features,
        fill_value=0
    )

    prediction = model.predict(df)[0]

    return prediction