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
# ================================
start_time = time.time()

# Get project root
script_dir = os.path.dirname(os.path.abspath(__file__))      
project_root = os.path.abspath(os.path.join(script_dir, ".."))

# Dataset should be inside project_root/data
dataset_path = os.path.join(project_root, "data", "ckd_datset.csv")

print(f"📂 Loading dataset from: {dataset_path}")
data = pd.read_csv(dataset_path)

print(f"✅ Dataset Shape: {data.shape}")
print(f"✅ Columns: {list(data.columns)}\n")

# ================================
# Preprocessing
# ================================
print("Preprocessing data...")

X = data.drop(columns=["PatientID", "DoctorInCharge", "Diagnosis"])
y = data["Diagnosis"]

scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

print("Handling class imbalance with SMOTEENN...")
smote_enn = SMOTEENN(random_state=42)
X_resampled, y_resampled = smote_enn.fit_resample(X_scaled, y)

print("Splitting into train/test sets...")
X_train, X_test, y_train, y_test = train_test_split(
    X_resampled, y_resampled, test_size=0.2,
    random_state=42, stratify=y_resampled
)

# ================================
# Define Models
# ================================
print("Initializing models...")

num_normal = sum(y_resampled == 0)
num_ckd = sum(y_resampled == 1)
scale_pos_weight = num_normal / num_ckd

rf = RandomForestClassifier(
    n_estimators=300,
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
# Train Model
# ================================
print("Training ensemble model...")
ensemble.fit(X_train, y_train)
print("Training complete!")

# ================================
# Evaluate Model
# ================================
print("Evaluating...")
y_pred = ensemble.predict(X_test)

accuracy = accuracy_score(y_test, y_pred)
print(f"\nAccuracy: {accuracy * 100:.2f}%")
print("Classification Report:")
print(classification_report(y_test, y_pred))

# ================================
# Save Model & Scaler (STORE IN REPO ROOT)
# ================================
models_dir = os.path.join(project_root, "models")
os.makedirs(models_dir, exist_ok=True)

model_path = os.path.join(models_dir, "ckd_model.pkl")
scaler_path = os.path.join(models_dir, "scaler.pkl")
features_path = os.path.join(models_dir, "feature_names.pkl")

print(f"\nSaving model & scaler to: {models_dir}")
joblib.dump(ensemble, model_path)
joblib.dump(scaler, scaler_path)
joblib.dump(list(X.columns), features_path)

print("Model saved →", model_path)
print("Scaler saved →", scaler_path)
print("Feature names saved →", features_path)

# ================================
# Timer
# ================================
end_time = time.time()
print(f"\nTraining finished in {end_time - start_time:.2f} seconds")
