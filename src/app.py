from flask import Flask, render_template, request, jsonify
import os
import joblib
import pandas as pd
import time
from difflib import SequenceMatcher

from database import save_patient_record
from download import download_bp, save_csv_record, save_pdf_record

# ----------------------------------------------------------
# FLASK CONFIG
# ----------------------------------------------------------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

app = Flask(
    __name__,
    static_folder=os.path.join(BASE_DIR, "static"),
    template_folder=os.path.join(BASE_DIR, "templates")
)

app.register_blueprint(download_bp)

# ----------------------------------------------------------
# CKD CHATBOT KNOWLEDGE BASE
# ----------------------------------------------------------
CKD_KNOWLEDGE = {
    "ckd": "CKD (Chronic Kidney Disease) is a long-term condition where kidney function gradually decreases.",
    "gfr": "GFR measures kidney filtration rate. Normal GFR is ≥90 ml/min.",
    "creatinine": "High creatinine indicates reduced kidney function.",
    "stages": "CKD stages: Stage 1 (≥90), Stage 2 (60–89), Stage 3 (30–59), Stage 4 (15–29), Stage 5 (<15).",
    "diet": "CKD patients should limit salt, processed foods, and excessive protein.",
    "bp": "High blood pressure damages kidney blood vessels and increases CKD risk.",
    "diabetes": "Diabetes is the leading cause of CKD.",
    "protein": "Protein in urine is an early sign of kidney damage.",
    "dialysis": "Dialysis is required in Stage 5 CKD when kidneys fail.",
}

# ----------------------------------------------------------
# FORM → FEATURE MAPPING
# ----------------------------------------------------------
FORM_TO_FEATURE = {
    "patient_id": "PatientID",
    "age": "Age",
    "bmi": "BMI",
    "systolic_bp": "SystolicBP",
    "diastolic_bp": "DiastolicBP",
    "sugar": "FastingBloodSugar",
    "hba1c": "HbA1c",
    "creatinine": "SerumCreatinine",
    "gfr": "GFR",
    "protein": "ProteinInUrine",
    "hemoglobin": "HemoglobinLevels",
    "family_history": "FamilyHistoryKidneyDisease"
}

# ----------------------------------------------------------
# LOAD MODEL
# ----------------------------------------------------------
MODEL_DIR = os.path.join(BASE_DIR, "..", "models")

model = joblib.load(os.path.join(MODEL_DIR, "ckd_model.pkl"))
scaler = joblib.load(os.path.join(MODEL_DIR, "scaler.pkl"))
feature_names = joblib.load(os.path.join(MODEL_DIR, "feature_names.pkl"))

print("✅ Model loaded successfully")

# ----------------------------------------------------------
# CKD STAGING FUNCTION (KDIGO CORRECT)
# ----------------------------------------------------------
def get_ckd_stage(gfr):
    try:
        gfr = float(gfr)
    except:
        return "Unknown", "Invalid GFR value"

    if gfr >= 90:
        return "Stage 1 CKD", "Normal GFR with kidney damage. Monitor regularly."
    elif gfr >= 60:
        return "Stage 2 CKD", "Mild reduction in GFR. Lifestyle modification advised."
    elif gfr >= 45:
        return "Stage 3a CKD", "Mild–moderate reduction. Control BP and sugar."
    elif gfr >= 30:
        return "Stage 3b CKD", "Moderate–severe reduction. Nephrologist consultation advised."
    elif gfr >= 15:
        return "Stage 4 CKD", "Severe reduction. High risk, close supervision needed."
    else:
        return "Stage 5 CKD", "Kidney failure. Dialysis or transplant evaluation required."

# ----------------------------------------------------------
# CHATBOT UTILS
# ----------------------------------------------------------
def similarity(a, b):
    return SequenceMatcher(None, a.lower(), b.lower()).ratio()

def chatbot_reply(user_msg):
    user_msg = user_msg.lower()
    best_score = 0
    best_answer = None

    for key, answer in CKD_KNOWLEDGE.items():
        score = similarity(user_msg, key)
        if score > best_score:
            best_score = score
            best_answer = answer

    if best_score > 0.4:
        return best_answer

    return "I can help with CKD, GFR, creatinine, diet, stages, BP, or diabetes."

# ----------------------------------------------------------
# CHATBOT ROUTE
# ----------------------------------------------------------
@app.route("/chatbot", methods=["POST"])
def chatbot():
    data = request.get_json()
    msg = data.get("message", "")
    return jsonify({"reply": chatbot_reply(msg)})

# ----------------------------------------------------------
# MAIN ROUTE
# ----------------------------------------------------------
@app.route("/", methods=["GET", "POST"])
def index():
    prediction = stage = advice = prob = risk_label = None
    download_url = download_pdf_url = None

    if request.method == "POST":
        form = request.form

        # -------------------------------
        # PREPARE MODEL INPUT
        # -------------------------------
        data = {}

        for feat in feature_names:
            form_key = next(
                (k for k, v in FORM_TO_FEATURE.items() if v.lower() == feat.lower()),
                None
            )

            val = form.get(form_key, "") if form_key else ""
            val = val.replace("%", "").replace(",", ".")

            try:
                data[feat] = float(val) if val != "" else 0.0
            except:
                data[feat] = 0.0

        df = pd.DataFrame([[data[c] for c in feature_names]],
                          columns=feature_names)

        scaled = scaler.transform(df)

        # -------------------------------
        # MODEL PREDICTION
        # -------------------------------
        prediction = int(model.predict(scaled)[0])
        prob = float(model.predict_proba(scaled)[0][1])

        # -------------------------------
        # FINAL INTERPRETATION LOGIC ✅
        # -------------------------------
        if prediction == 1:
            stage, advice = get_ckd_stage(data.get("GFR", 0))
            risk_label = "CKD Detected"
        else:
            stage = "Normal Kidney Function"
            advice = (
                "No significant CKD risk detected. "
                "Maintain healthy lifestyle and regular checkups."
            )
            risk_label = "No Significant CKD Risk"

        # -------------------------------
        # SAVE RECORD
        # -------------------------------
        record = (
            form.get("patient_id") or f"anon_{int(time.time())}",
            *data.values(),
            prediction,
            prob,
            "Stored via CKD App"
        )
        save_patient_record(record)

        # -------------------------------
        # SAVE CSV / PDF
        # -------------------------------
        csv_data = {"PatientID": form.get("patient_id")}
        csv_data.update(data)
        csv_data.update({
            "Prediction": prediction,
            "Probability": prob,
            "Stage": stage,
            "Advice": advice
        })

        download_url = save_csv_record(csv_data, feature_names)
        try:
            download_pdf_url = save_pdf_record(csv_data)
        except:
            pass

    return render_template(
        "index.html",
        prediction=prediction,
        stage=stage,
        prob=prob,
        advice=advice,
        risk_label=risk_label,
        download_url=download_url,
        download_pdf_url=download_pdf_url
    )

# ----------------------------------------------------------
# RUN APP
# ----------------------------------------------------------
if __name__ == "__main__":
    app.run(app.run(host="0.0.0.0", port=10000))
