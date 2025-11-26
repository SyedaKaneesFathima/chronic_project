import os
import time
import pandas as pd
import joblib

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier, VotingClassifier
from sklearn.metrics import accuracy_score, classification_report
from xgboost import XGBClassifier
from imblearn.combine import SMOTEENN

# ================================
# Load Dataset
start_time = time.time()

dataset_path = r"c:\Users\91814\OneDrive\Desktop\chronic_project\data\ckd_datset.csv"
print(f"📂 Loading dataset from: {dataset_path}")

data = pd.read_csv(dataset_path)
print(f"✅ Dataset Shape: {data.shape}")
print(f"✅ Columns: {list(data.columns)}\n")

print("Dataset columns:")
print(data.head(200), "\n")

# ================================
# Preprocessing
# ================================
print("Preprocessing data...")
X = data.drop(columns=["PatientID", "DoctorInCharge", "Diagnosis"])
y = data["Diagnosis"]

scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

print(" Handling class imbalance with SMOTEENN...")
smote_enn = SMOTEENN(random_state=42)
X_resampled, y_resampled = smote_enn.fit_resample(X_scaled, y)

print(" Splitting into train/test sets...")
X_train, X_test, y_train, y_test = train_test_split(
    X_resampled, y_resampled, test_size=0.2, random_state=42, stratify=y_resampled
)

# ================================
# Define Models with Progress Prints
# ================================
num_normal = sum(y_resampled == 0)
num_ckd = sum(y_resampled == 1)
scale_pos_weight = num_normal / num_ckd  # for XGBoost

print("Initializing models...")
rf = RandomForestClassifier(
    n_estimators=300,  # use 300 for final run
    random_state=42,
    class_weight="balanced",
    n_jobs=-1
)
gb = GradientBoostingClassifier(
    n_estimators=300,  
    random_state=42
)
xgb = XGBClassifier(
    eval_metric="logloss",
    random_state=42,
    scale_pos_weight=scale_pos_weight,
    n_estimators=300,  
    n_jobs=-1
)

ensemble = VotingClassifier(
    estimators=[("rf", rf), ("gb", gb), ("xgb", xgb)],
    voting="soft"
)

# ================================
# Train Model with Updates
# ================================
print(" !!Training ensemble model...")
ensemble.fit(X_train, y_train)
print("Training complete!")

# ================================
# Evaluate Model
# ================================
print("Evaluating model...")
y_pred = ensemble.predict(X_test)

accuracy = accuracy_score(y_test, y_pred)
print(f"\n Model Accuracy: {accuracy * 100:.2f}%\n")
print("Classification Report:")
print(classification_report(y_test, y_pred))

# ================================
# Save Model & Scaler
# ================================
print(" Saving model & scaler...")
os.makedirs("models", exist_ok=True)
joblib.dump(ensemble, "models/ckd_model.pkl")
joblib.dump(scaler, "models/scaler.pkl")
joblib.dump(list(X.columns), "models/feature_names.pkl")

print("\n Model saved to models/ckd_model.pkl")
print(" Scaler saved to models/scaler.pkl")
print(" Feature names saved to models/feature_names.pkl")

# ================================
# Timer
# ================================
end_time = time.time()
print(f"\n Training completed in {end_time - start_time:.2f} seconds")


