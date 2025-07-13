from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import joblib
from pydantic import BaseModel, EmailStr
import numpy as np
import csv
import os

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

model = joblib.load("model/lead_model.pkl")

class LeadInput(BaseModel):
    email: EmailStr
    phone: str
    income: float
    creditScore: float
    ageGroup: str
    familyStatus: str
    comments: str

def encode_age(age):
    mapping = {"18-25": 0, "26-35": 1, "36-50": 2, "51+": 3}
    return mapping.get(age, -1)

def encode_family(family):
    mapping = {"Single": 0, "Married": 1, "Married with Kids": 2}
    return mapping.get(family, -1)

@app.post("/score")
def get_score(data: LeadInput):
    # Encode categorical fields
    age_encoded = encode_age(data.ageGroup)
    family_encoded = encode_family(data.familyStatus)

    # Predict using the model
    features = np.array([[data.income, data.creditScore, age_encoded, family_encoded]])
    initial_score = model.predict_proba(features)[0][1]

    # Rule-based reranking
    reranked_score = initial_score
    if "urgent" in data.comments.lower():
        reranked_score += 0.1
    elif "not interested" in data.comments.lower():
        reranked_score -= 0.2
    reranked_score = min(1.0, max(0.0, reranked_score))

    # Prepare data for CSV
    row = [
        data.email,
        data.phone,
        data.income,
        data.creditScore,
        data.ageGroup,
        data.familyStatus,
        data.comments,
        round(initial_score, 2),
        round(reranked_score, 2)
    ]

    # Write to CSV
    file_path = "leads.csv"
    write_header = not os.path.exists(file_path)

    with open(file_path, mode="a", newline="") as file:
        writer = csv.writer(file)
        if write_header:
            writer.writerow([
                "Email", "Phone", "Income", "Credit Score", "Age Group",
                "Family Status", "Comments", "Initial Score", "Reranked Score"
            ])
        writer.writerow(row)

    return {
        "initial_score": round(initial_score, 2),
        "reranked_score": round(reranked_score, 2)
    }
