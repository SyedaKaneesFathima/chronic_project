# # src/app.py
# from src.download import download_bp, save_csv_record, save_pdf_record
# from flask import Flask, render_template, request, jsonify
# import os
# import joblib
# import pandas as pd
# from src.database import save_patient_record
# from difflib import SequenceMatcher
# import time


# # ----------------------------------------------------------
# # FLASK CONFIG
# # ----------------------------------------------------------
# BASE_DIR = os.path.dirname(os.path.abspath(__file__))
# app = Flask(
#     __name__,
#     static_folder=os.path.join(BASE_DIR, "static"),
#     template_folder=os.path.join(BASE_DIR, "templates")
# )
# app.register_blueprint(download_bp)


# # ----------------------------------------------------------
# # CKD KNOWLEDGE BASE
# # ----------------------------------------------------------
# CKD_KNOWLEDGE = {
#     "0":"hello",
#     "1": "CKD stands for Chronic Kidney Disease, a long-term condition where kidney function gradually decreases.",
#     "2": "Symptoms of CKD include swelling, fatigue, nausea, vomiting, foamy urine and changes in urination.",
#     "3": "A major cause of CKD is diabetes.",
#     "4": "High blood pressure is the second biggest cause of CKD.",
#     "5": "Smoking increases kidney damage risk.",
#     "6": "CKD causes swelling because kidneys retain excess fluid.",
#     "7": "High creatinine means kidney function is reduced.",
#     "8": "GFR is the most important indicator of kidney health.",
#     "9": "Normal GFR is above 90.",
#     "10": "GFR below 15 means kidney failure.",
#     "11": "Avoid salty foods to protect kidneys.",
#     "12": "CKD patients should follow a low-potassium diet.",
#     "13": "Limit protein to reduce kidney workload.",
#     "14": "Diabetes + High BP increases CKD risk 3 times.",
#     "15": "Early CKD may show no symptoms.",
#     "16": "Stage 3 CKD means moderate kidney damage.",
#     "17": "Stage 5 CKD usually requires dialysis or transplant.",
#     "18": "Dialysis cleans the blood when kidneys fail.",
#     "19": "Drink balanced amounts of water, not too much or too little.",
#     "20": "Painkillers like ibuprofen damage kidneys.",
#     "21": "Exercise helps maintain healthy BP and kidney function.",
#     "22": "CKD can cause anemia due to low hemoglobin.",
#     "23": "Fluid buildup may cause breathlessness.",
#     "24": "Foamy urine means protein leakage.",
#     "25": "High BP damages kidney blood vessels.",
#     "26": "CKD may reduce appetite.",
#     "27": "High potassium causes heart rhythm problems.",
#     "28": "CKD increases risk of heart attack.",
#     "29": "Controlling sugar protects kidneys.",
#     "30": "Avoid packaged and processed foods.",
#     "31": "Limit red meat to reduce kidney strain.",
#     "32": "Limit salt to less than 2g/day.",
#     "33": "Drink clean water only.",
#     "34": "Avoid herbal supplements unless prescribed.",
#     "35": "Dairy contains high phosphorus.",
#     "36": "Muscle cramps are common in CKD.",
#     "37": "Dry and itchy skin is common in CKD.",
#     "38": "Healthy kidneys filter 180 liters of blood daily.",
#     "39": "Diabetes damages kidney filtering units.",
#     "40": "High BP causes kidney damage.",
#     "41": "Repeated infections can damage kidneys.",
#     "42": "Avoid alcohol as it dehydrates kidneys.",
#     "43": "Avoid sodas; they harm kidneys.",
#     "44": "Lemon water hydrates but doesn't cure CKD.",
#     "45": "Salt substitutes contain potassium—avoid them.",
#     "46": "Regular kidney tests help track CKD.",
#     "47": "Ultrasound detects kidney size and structure.",
#     "48": "CKD causes mineral imbalance.",
#     "49": "Sodium bicarbonate helps manage acidity.",
#     "50": "High uric acid worsens CKD.",
#     "51": "Avoid unnecessary antibiotics.",
#     "52": "Reduce sugar to prevent kidney stress.",
#     "53": "Bananas are high in potassium—limit them.",
#     "54": "Coconut water is high in potassium—avoid it.",
#     "55": "Avoid salty snacks completely.",
#     "56": "Milk should be taken moderately.",
#     "57": "Avoid protein powders unless advised.",
#     "58": "CKD cannot be cured but can be slowed.",
#     "59": "Early detection helps best outcomes.",
#     "60": "Obesity increases CKD risk.",
#     "61": "High cholesterol affects kidney function.",
#     "62": "Stress increases BP and worsens CKD.",
#     "63": "Good sleep improves kidney health.",
#     "64": "Avoid crash diets.",
#     "65": "CKD may require restricted fluid intake.",
#     "66": "Dialysis frequency depends on symptoms.",
#     "67": "Kidneys usually fail slowly over time.",
#     "68": "Transplant is best treatment for Stage 5 CKD.",
#     "69": "Blood in urine is a warning sign.",
#     "70": "Back pain isn't always kidney pain.",
#     "71": "CKD increases body acidity.",
#     "72": "Soak potatoes to reduce potassium.",
#     "73": "Tomatoes are high in potassium.",
#     "74": "Dairy cheese has high phosphorus.",
#     "75": "White bread has less potassium than wheat.",
#     "76": "Avoid pickles and papad.",
#     "77": "Sudden weight gain = fluid retention.",
#     "78": "Limit coffee intake.",
#     "79": "Avoid energy drinks totally.",
#     "80": "CKD increases bone disease risk.",
#     "81": "Calcium imbalance is common.",
#     "82": "Nuts are high in phosphorus—limit them.",
#     "83": "Olive oil is kidney-friendly.",
#     "84": "Safe fruits: apples, grapes, pineapple, pears.",
#     "85": "Berries are excellent for kidneys.",
#     "86": "Grapes have moderate potassium—limit them.",
#     "87": "Hydration can improve GFR temporarily.",
#     "88": "Avoid OTC medicines unless approved.",
#     "89": "Vomiting worsens dehydration.",
#     "90": "Control BP to slow CKD progression.",
#     "91": "Do not skip BP medicines.",
#     "92": "Metformin may be stopped in late CKD.",
#     "93": "ACE inhibitors help protect kidneys.",
#     "94": "A nephrologist is a kidney specialist.",
#     "95": "Urine protein test detects kidney damage early.",
#     "96": "CKD affects mental health too.",
#     "97": "Family history increases CKD risk.",
#     "98": "Avoid creatine supplements.",
#     "99": "Avoid IV saline unless prescribed.",
#     "100": "With proper care CKD progression can be slowed.",
#     "101": "CKD has 5 stages: Stage 1 (GFR ≥90), Stage 2 (60–89), Stage 3a (45–59), Stage 3b (30–44), Stage 4 (15–29), Stage 5 (<15, kidney failure).",
#     "102": "Common symptoms of CKD include swelling, itching, weakness, nausea, vomiting, foamy urine, high BP, and breathlessness."
# }


# # ----------------------------------------------------------
# # FORM FIELD → MODEL FEATURE MAPPING
# # ----------------------------------------------------------
# FORM_TO_FEATURE = {
#     "patient_id": "PatientID",
#     "age": "Age",
#     "gender": "Gender",
#     "ethnicity": "Ethnicity",
#     "socioeconomic": "SocioeconomicStatus",
#     "education": "EducationLevel",
#     "bmi": "BMI",
#     "smoking": "Smoking",
#     "alcohol": "AlcoholConsumption",
#     "physical_activity": "PhysicalActivity",
#     "diet_quality": "DietQuality",
#     "sleep_quality": "SleepQuality",
#     "family_history": "FamilyHistoryKidneyDisease",
#     "family_history_htn": "FamilyHistoryHypertension",
#     "family_history_dm": "FamilyHistoryDiabetes",
#     "previous_aki": "PreviousAcuteKidneyInjury",
#     "uti": "UrinaryTractInfections",
#     "systolic_bp": "SystolicBP",
#     "diastolic_bp": "DiastolicBP",
#     "sugar": "FastingBloodSugar",
#     "hba1c": "HbA1c",
#     "creatinine": "SerumCreatinine",
#     "bun": "BUNLevels",
#     "gfr": "GFR",
#     "protein": "ProteinInUrine",
#     "acr": "ACR",
#     "na": "SerumElectrolytesSodium",
#     "k": "SerumElectrolytesPotassium",
#     "calcium": "SerumElectrolytesCalcium",
#     "phosphorus": "SerumElectrolytesPhosphorus",
#     "hemoglobin": "HemoglobinLevels",
#     "chol_total": "CholesterolTotal",
#     "chol_ldl": "CholesterolLDL",
#     "chol_hdl": "CholesterolHDL",
#     "chol_tri": "CholesterolTriglycerides",
#     "ace_inhibitors": "ACEInhibitors",
#     "diuretics": "Diuretics",
#     "nsaids": "NSAIDsUse",
#     "statins": "Statins",
#     "antidiabetics": "AntidiabeticMedications",
#     "edema": "Edema",
#     "fatigue": "FatigueLevels",
#     "nausea": "NauseaVomiting",
#     "muscle_cramps": "MuscleCramps",
#     "itching": "Itching",
# }


# # ----------------------------------------------------------
# # LOAD MODEL
# # ----------------------------------------------------------
# MODEL_DIR = os.path.join(BASE_DIR, "..", "models")
# model = joblib.load(os.path.join(MODEL_DIR, "ckd_model.pkl"))
# scaler = joblib.load(os.path.join(MODEL_DIR, "scaler.pkl"))
# feature_names = joblib.load(os.path.join(MODEL_DIR, "feature_names.pkl"))


# # ----------------------------------------------------------
# # UTILITY FUNCTIONS
# # ----------------------------------------------------------
# def get_ckd_stage(gfr_value):
#     try:
#         gfr_value = float(gfr_value)
#     except:
#         return "Unknown", "Invalid GFR value"

#     if gfr_value >= 90:
#         return "Stage 1 (Normal)", "Maintain hydration and regular checkups."
#     elif gfr_value >= 60:
#         return "Stage 2 (Mild CKD)", "Reduce salt, follow healthy diet."
#     elif gfr_value >= 45:
#         return "Stage 3a", "Reduce protein intake, avoid junk food."
#     elif gfr_value >= 30:
#         return "Stage 3b", "Consult a nephrologist soon."
#     elif gfr_value >= 15:
#         return "Stage 4", "High risk — medical supervision needed."
#     else:
#         return "Stage 5 (Kidney Failure)", "Emergency care required."


# def similar(a, b):
#     return SequenceMatcher(None, a.lower(), b.lower()).ratio()


# def get_local_ckd_reply(user_msg):
#     msg = user_msg.lower()
#     best_score = 0
#     best_answer = None

#     smart_map = {
#         "hi":0,
#         "what is ckd": 1,
#         "symptoms": 102,
#         "ckd stages": 101,
#         "gfr": 8,
#         "creatinine": 7,
#         "diet": 11,
#         "dialysis": 18,
#         "transplant": 68
#     }

#     for q, res_id in smart_map.items():
#         score = similar(msg, q)
#         if score > best_score:
#             best_score = score
#             best_answer = CKD_KNOWLEDGE.get(str(res_id))

#     if best_score > 0.45:
#         return best_answer

#     return "Sorry, I didn't understand. Try asking about CKD stages, symptoms, GFR, creatinine, or diet."


# # ----------------------------------------------------------
# # CHATBOT ROUTE
# # ----------------------------------------------------------
# @app.route("/chatbot", methods=["POST"])
# def chatbot():
#     data = request.get_json()
#     msg = data.get("message", "")
#     return jsonify({"reply": get_local_ckd_reply(msg)})


# # ----------------------------------------------------------
# # MAIN PREDICTION ROUTE
# # ----------------------------------------------------------
# @app.route("/", methods=["GET", "POST"])
# def index():
#     prediction = stage = advice = prob = None
#     download_url = download_pdf_url = None

#     if request.method == "POST":
#         form = request.form

#         # Build feature dict for prediction
#         data = {}
#         for feat in feature_names:
#             form_key = next((k for k, v in FORM_TO_FEATURE.items() if v == feat), None)
#             val = form.get(form_key, "") or form.get(feat, "")

#             try:
#                 data[feat] = float(val) if val != "" else 0.0
#             except:
#                 data[feat] = val

#         # ML prediction
#         df = pd.DataFrame([[data[c] for c in feature_names]], columns=feature_names)
#         scaled = scaler.transform(df)

#         prediction = int(model.predict(scaled)[0])
#         prob = float(model.predict_proba(scaled)[0][1])

#         # Stage/advice
#         stage, advice = get_ckd_stage(data.get("GFR", 0))

#         # Save DB record
#         record = ( 
#             form.get("patient_id") or None,
#             *[data[k] for k in data],
#             prediction,
#             prob,
#             "Stored via CKD App"
#         )
#         save_patient_record(record)

#         # Build CSV data
#         csv_data = {"PatientID": form.get("patient_id") or f"anon_{int(time.time())}"}
#         for feat in feature_names:
#             csv_data[feat] = data[feat]

#         csv_data.update({
#             "prediction": prediction,
#             "probability": prob,
#             "Stage": stage,
#             "Advice": advice
#         })

#         # Save CSV file
#         download_url = save_csv_record(csv_data, feature_names=feature_names)

#         # Save PDF (optional)
#         try:
#             download_pdf_url = save_pdf_record(csv_data)
#         except:
#             download_pdf_url = None

#     return render_template("index.html",
#                            prediction=prediction,
#                            stage=stage,
#                            prob=prob,
#                            advice=advice,
#                            download_url=download_url,
#                            download_pdf_url=download_pdf_url)


# # ----------------------------------------------------------
# # RUN APP
# # ----------------------------------------------------------
# if __name__ == "__main__":
#     app.run(debug=True)


# src/app.py
from src.download import download_bp, save_csv_record, save_pdf_record
from flask import Flask, render_template, request, jsonify
import os
import joblib
import pandas as pd
from src.database import save_patient_record
from difflib import SequenceMatcher
import time

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
# CKD KNOWLEDGE BASE
# (kept as in your original file)
# ----------------------------------------------------------
CKD_KNOWLEDGE = {
    "0":"hello",
    "1": "CKD stands for Chronic Kidney Disease, a long-term condition where kidney function gradually decreases.",
    "2": "Symptoms of CKD include swelling, fatigue, nausea, vomiting, foamy urine and changes in urination.",
    "3": "A major cause of CKD is diabetes.",
    "4": "High blood pressure is the second biggest cause of CKD.",
    "5": "Smoking increases kidney damage risk.",
    "6": "CKD causes swelling because kidneys retain excess fluid.",
    "7": "High creatinine means kidney function is reduced.",
    "8": "GFR is the most important indicator of kidney health.",
    "9": "Normal GFR is above 90.",
    "10": "GFR below 15 means kidney failure.",
    "11": "Avoid salty foods to protect kidneys.",
    "12": "CKD patients should follow a low-potassium diet.",
    "13": "Limit protein to reduce kidney workload.",
    "14": "Diabetes + High BP increases CKD risk 3 times.",
    "15": "Early CKD may show no symptoms.",
    "16": "Stage 3 CKD means moderate kidney damage.",
    "17": "Stage 5 CKD usually requires dialysis or transplant.",
    "18": "Dialysis cleans the blood when kidneys fail.",
    "19": "Drink balanced amounts of water, not too much or too little.",
    "20": "Painkillers like ibuprofen damage kidneys.",
    "21": "Exercise helps maintain healthy BP and kidney function.",
    "22": "CKD can cause anemia due to low hemoglobin.",
    "23": "Fluid buildup may cause breathlessness.",
    "24": "Foamy urine means protein leakage.",
    "25": "High BP damages kidney blood vessels.",
    "26": "CKD may reduce appetite.",
    "27": "High potassium causes heart rhythm problems.",
    "28": "CKD increases risk of heart attack.",
    "29": "Controlling sugar protects kidneys.",
    "30": "Avoid packaged and processed foods.",
    "31": "Limit red meat to reduce kidney strain.",
    "32": "Limit salt to less than 2g/day.",
    "33": "Drink clean water only.",
    "34": "Avoid herbal supplements unless prescribed.",
    "35": "Dairy contains high phosphorus.",
    "36": "Muscle cramps are common in CKD.",
    "37": "Dry and itchy skin is common in CKD.",
    "38": "Healthy kidneys filter 180 liters of blood daily.",
    "39": "Diabetes damages kidney filtering units.",
    "40": "High BP causes kidney damage.",
    "41": "Repeated infections can damage kidneys.",
    "42": "Avoid alcohol as it dehydrates kidneys.",
    "43": "Avoid sodas; they harm kidneys.",
    "44": "Lemon water hydrates but doesn't cure CKD.",
    "45": "Salt substitutes contain potassium—avoid them.",
    "46": "Regular kidney tests help track CKD.",
    "47": "Ultrasound detects kidney size and structure.",
    "48": "CKD causes mineral imbalance.",
    "49": "Sodium bicarbonate helps manage acidity.",
    "50": "High uric acid worsens CKD.",
    "51": "Avoid unnecessary antibiotics.",
    "52": "Reduce sugar to prevent kidney stress.",
    "53": "Bananas are high in potassium—limit them.",
    "54": "Coconut water is high in potassium—avoid it.",
    "55": "Avoid salty snacks completely.",
    "56": "Milk should be taken moderately.",
    "57": "Avoid protein powders unless advised.",
    "58": "CKD cannot be cured but can be slowed.",
    "59": "Early detection helps best outcomes.",
    "60": "Obesity increases CKD risk.",
    "61": "High cholesterol affects kidney function.",
    "62": "Stress increases BP and worsens CKD.",
    "63": "Good sleep improves kidney health.",
    "64": "Avoid crash diets.",
    "65": "CKD may require restricted fluid intake.",
    "66": "Dialysis frequency depends on symptoms.",
    "67": "Kidneys usually fail slowly over time.",
    "68": "Transplant is best treatment for Stage 5 CKD.",
    "69": "Blood in urine is a warning sign.",
    "70": "Back pain isn't always kidney pain.",
    "71": "CKD increases body acidity.",
    "72": "Soak potatoes to reduce potassium.",
    "73": "Tomatoes are high in potassium.",
    "74": "Dairy cheese has high phosphorus.",
    "75": "White bread has less potassium than wheat.",
    "76": "Avoid pickles and papad.",
    "77": "Sudden weight gain = fluid retention.",
    "78": "Limit coffee intake.",
    "79": "Avoid energy drinks totally.",
    "80": "CKD increases bone disease risk.",
    "81": "Calcium imbalance is common.",
    "82": "Nuts are high in phosphorus—limit them.",
    "83": "Olive oil is kidney-friendly.",
    "84": "Safe fruits: apples, grapes, pineapple, pears.",
    "85": "Berries are excellent for kidneys.",
    "86": "Grapes have moderate potassium—limit them.",
    "87": "Hydration can improve GFR temporarily.",
    "88": "Avoid OTC medicines unless approved.",
    "89": "Vomiting worsens dehydration.",
    "90": "Control BP to slow CKD progression.",
    "91": "Do not skip BP medicines.",
    "92": "Metformin may be stopped in late CKD.",
    "93": "ACE inhibitors help protect kidneys.",
    "94": "A nephrologist is a kidney specialist.",
    "95": "Urine protein test detects kidney damage early.",
    "96": "CKD affects mental health too.",
    "97": "Family history increases CKD risk.",
    "98": "Avoid creatine supplements.",
    "99": "Avoid IV saline unless prescribed.",
    "100": "With proper care CKD progression can be slowed.",
    "101": "CKD has 5 stages: Stage 1 (GFR ≥90), Stage 2 (60–89), Stage 3a (45–59), Stage 3b (30–44), Stage 4 (15–29), Stage 5 (<15, kidney failure).",
    "102": "Common symptoms of CKD include swelling, itching, weakness, nausea, vomiting, foamy urine, high BP, and breathlessness."
}

# ----------------------------------------------------------
# FORM FIELD → MODEL FEATURE MAPPING
# ----------------------------------------------------------
FORM_TO_FEATURE = {
    "patient_id": "PatientID",
    "age": "Age",
    "gender": "Gender",
    "ethnicity": "Ethnicity",
    "socioeconomic": "SocioeconomicStatus",
    "education": "EducationLevel",
    "bmi": "BMI",
    "smoking": "Smoking",
    "alcohol": "AlcoholConsumption",
    "physical_activity": "PhysicalActivity",
    "diet_quality": "DietQuality",
    "sleep_quality": "SleepQuality",
    "family_history": "FamilyHistoryKidneyDisease",
    "family_history_htn": "FamilyHistoryHypertension",
    "family_history_dm": "FamilyHistoryDiabetes",
    "previous_aki": "PreviousAcuteKidneyInjury",
    "uti": "UrinaryTractInfections",
    "systolic_bp": "SystolicBP",
    "diastolic_bp": "DiastolicBP",
    "sugar": "FastingBloodSugar",
    "hba1c": "HbA1c",
    "creatinine": "SerumCreatinine",
    "bun": "BUNLevels",
    "gfr": "GFR",
    "protein": "ProteinInUrine",
    "acr": "ACR",
    "na": "SerumElectrolytesSodium",
    "k": "SerumElectrolytesPotassium",
    "calcium": "SerumElectrolytesCalcium",
    "phosphorus": "SerumElectrolytesPhosphorus",
    "hemoglobin": "HemoglobinLevels",
    "chol_total": "CholesterolTotal",
    "chol_ldl": "CholesterolLDL",
    "chol_hdl": "CholesterolHDL",
    "chol_tri": "CholesterolTriglycerides",
    "ace_inhibitors": "ACEInhibitors",
    "diuretics": "Diuretics",
    "nsaids": "NSAIDsUse",
    "statins": "Statins",
    "antidiabetics": "AntidiabeticMedications",
    "edema": "Edema",
    "fatigue": "FatigueLevels",
    "nausea": "NauseaVomiting",
    "muscle_cramps": "MuscleCramps",
    "itching": "Itching",
}

# ----------------------------------------------------------
# LOAD MODEL
# ----------------------------------------------------------
MODEL_DIR = os.path.join(BASE_DIR, "..", "models")
model = joblib.load(os.path.join(MODEL_DIR, "ckd_model.pkl"))
scaler = joblib.load(os.path.join(MODEL_DIR, "scaler.pkl"))
feature_names = joblib.load(os.path.join(MODEL_DIR, "feature_names.pkl"))

# ----------------------------------------------------------
# UTILITY FUNCTIONS
# ----------------------------------------------------------
def get_ckd_stage(gfr_value):
    try:
        gfr_value = float(gfr_value)
    except:
        return "Unknown", "Invalid GFR value"

    # If a probability (0-1) was accidentally passed, convert to percentage
    if 0 < gfr_value <= 1:
        gfr_value = gfr_value * 100

    if gfr_value >= 90:
        return "Stage 1 (Normal)", "Maintain hydration and regular checkups."
    elif gfr_value >= 60:
        return "Stage 2 (Mild CKD)", "Reduce salt, follow healthy diet."
    elif gfr_value >= 45:
        return "Stage 3a", "Reduce protein intake, avoid junk food."
    elif gfr_value >= 30:
        return "Stage 3b", "Consult a nephrologist soon."
    elif gfr_value >= 15:
        return "Stage 4", "High risk — medical supervision needed."
    else:
        return "Stage 5 (Kidney Failure)", "Emergency care required."


def similar(a, b):
    return SequenceMatcher(None, a.lower(), b.lower()).ratio()


def get_local_ckd_reply(user_msg):
    msg = user_msg.lower()
    best_score = 0
    best_answer = None

    smart_map = {
        "hi":0,
        "what is ckd": 1,
        "symptoms": 102,
        "ckd stages": 101,
        "gfr": 8,
        "creatinine": 7,
        "diet": 11,
        "dialysis": 18,
        "transplant": 68
    }

    for q, res_id in smart_map.items():
        score = similar(msg, q)
        if score > best_score:
            best_score = score
            best_answer = CKD_KNOWLEDGE.get(str(res_id))

    if best_score > 0.45:
        return best_answer

    return "Sorry, I didn't understand. Try asking about CKD stages, symptoms, GFR, creatinine, or diet."

# ----------------------------------------------------------
# CHATBOT ROUTE
# ----------------------------------------------------------
@app.route("/chatbot", methods=["POST"])
def chatbot():
    data = request.get_json()
    msg = data.get("message", "")
    return jsonify({"reply": get_local_ckd_reply(msg)})

# ----------------------------------------------------------
# MAIN PREDICTION ROUTE
# ----------------------------------------------------------
@app.route("/", methods=["GET", "POST"])
def index():
    prediction = stage = advice = prob = None
    download_url = download_pdf_url = None

    if request.method == "POST":
        form = request.form

        # Build feature dict for prediction (robust, case-insensitive, percent-safe)
        data = {}
        for feat in feature_names:
            # try to find mapped form key (case-insensitive)
            form_key = next((k for k, v in FORM_TO_FEATURE.items() if v.lower() == feat.lower()), None)

            # try multiple possible names in the incoming form
            val = ""
            if form_key:
                val = form.get(form_key, "")
            if not val:
                val = form.get(feat, "")
            if not val:
                val = form.get(feat.lower(), "")
            if not val:
                val = form.get(feat.upper(), "")

            # cleanup percent signs and comma decimals (e.g. "68.59%" or "68,59")
            if isinstance(val, str):
                val = val.strip().replace("%", "").replace(",", ".")

            try:
                data[feat] = float(val) if val != "" else 0.0
            except:
                data[feat] = val

        # --- DEBUG: inspect incoming form & parsed GFR (remove after verifying) ---
        # print("DEBUG form fields:", dict(form))
        # print("DEBUG parsed GFR (from data):", data.get("GFR", None))
        # -----------------------------------------------------------------------

        # ML prediction
        df = pd.DataFrame([[data[c] for c in feature_names]], columns=feature_names)
        scaled = scaler.transform(df)

        prediction = int(model.predict(scaled)[0])

        try:
            prob = float(model.predict_proba(scaled)[0][1])
        except Exception:
            prob = None

        # Stage/advice (use parsed numeric GFR)
        stage, advice = get_ckd_stage(data.get("GFR", 0))

        # Save DB record
        record = (
            form.get("patient_id") or None,
            *[data[k] for k in data],
            prediction,
            prob,
            "Stored via CKD App"
        )
        save_patient_record(record)

        # Build CSV data
        csv_data = {"PatientID": form.get("patient_id") or f"anon_{int(time.time())}"}
        for feat in feature_names:
            csv_data[feat] = data[feat]

        csv_data.update({
            "prediction": prediction,
            "probability": prob,
            "Stage": stage,
            "Advice": advice
        })

        # Save CSV file
        download_url = save_csv_record(csv_data, feature_names=feature_names)

        # Save PDF (optional)
        try:
            download_pdf_url = save_pdf_record(csv_data)
        except:
            download_pdf_url = None

    return render_template("index.html",
                           prediction=prediction,
                           stage=stage,
                           prob=prob,
                           advice=advice,
                           download_url=download_url,
                           download_pdf_url=download_pdf_url)

# ----------------------------------------------------------
# RUN APP
# ----------------------------------------------------------
if __name__ == "__main__":
    app.run(debug=True)

