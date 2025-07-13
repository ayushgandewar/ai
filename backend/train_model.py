import pandas as pd
from sklearn.linear_model import LogisticRegression
import joblib
import os

# Sample training data
data = pd.DataFrame([
    {"income": 50000, "creditScore": 650, "ageGroup": "18-25", "familyStatus": "Single", "label": 0},
    {"income": 120000, "creditScore": 780, "ageGroup": "26-35", "familyStatus": "Married", "label": 1},
    {"income": 70000, "creditScore": 710, "ageGroup": "36-50", "familyStatus": "Married with Kids", "label": 1},
    {"income": 30000, "creditScore": 580, "ageGroup": "18-25", "familyStatus": "Single", "label": 0},
    {"income": 95000, "creditScore": 760, "ageGroup": "51+", "familyStatus": "Married", "label": 1},
    {"income": 40000, "creditScore": 600, "ageGroup": "26-35", "familyStatus": "Single", "label": 0},
])

# Encoding helpers
age_map = {"18-25": 0, "26-35": 1, "36-50": 2, "51+": 3}
family_map = {"Single": 0, "Married": 1, "Married with Kids": 2}

# Encode categorical columns
data["ageEncoded"] = data["ageGroup"].map(age_map)
data["familyEncoded"] = data["familyStatus"].map(family_map)

# Features and label
X = data[["income", "creditScore", "ageEncoded", "familyEncoded"]]
y = data["label"]

# Train model
model = LogisticRegression()
model.fit(X, y)

# Save model
os.makedirs("model", exist_ok=True)
joblib.dump(model, "model/lead_model.pkl")

print("✅ LogisticRegression model trained and saved.")
