import joblib
import numpy as np

# Load trained model + scaler
model = joblib.load("models/ckd_model.pkl")
scaler = joblib.load("models/scaler.pkl")

print("✅ CKD Prediction Model Loaded (Simplified Version)\n")

# Only key features for prediction
key_features = [
    "Age",
    "BMI",
    "SystolicBP",
    "DiastolicBP",
    "SerumCreatinine",
    "GFR",
    "HemoglobinLevels",
    "ProteinInUrine",
    "FastingBloodSugar",
    "HbA1c",
    "FamilyHistoryKidneyDisease"
]

print("👉 Enter patient details (press Enter to use default = 0):")
patient_data = []

for feature in key_features:
    value = input(f"{feature}: ")
    if value.strip() == "":
        value = 0
    patient_data.append(float(value))

# Fill missing features with 0 so total = 51
total_features = 51
full_data = patient_data + [0] * (total_features - len(patient_data))

# Reshape + scale
full_data = np.array(full_data).reshape(1, -1)
full_data_scaled = scaler.transform(full_data)

# Predict
prediction = model.predict(full_data_scaled)[0]

print("\n🔮 Prediction Result:")
if prediction == 1:
    print("⚠️ Patient is at risk of Chronic Kidney Disease (CKD)")
else:
    print("✅ Patient is Healthy (No CKD)")
