Chronic Kidney Disease (CKD) Prediction Web App
✔ Flask • Machine Learning • MySQL • Railway Deployment

This project is a Chronic Kidney Disease (CKD) Prediction System built using:

Flask (Python)

Machine Learning Model (scikit-learn)

MySQL Database (local + Railway cloud)

Bootstrap UI + JS for interactivity

Downloadable CSV & PDF Reports

CKD Chatbot (rule-based)

🚀 Features
🧠 ML Prediction

Predicts CKD risk probability

Calculates disease stage using GFR

Shows medical recommendations

📥 Downloads

Download report as CSV

Download report as PDF

📊 Database

Stores all patient records in MySQL

Works both locally & on Railway cloud MySQL

🤖 CKD Chatbot

Ask:
✔ What is CKD?
✔ Symptoms
✔ GFR meaning
✔ Creatinine meaning
✔ Stages

Beautiful Frontend UI
Custom-designed with CSS, JS & images.
*PROJECT STRUCTURE*
CHRONIC_PROJECT/
│── data/
│── models/
│   ├── ckd_model.pkl
│   ├── scaler.pkl
│   ├── feature_names.pkl
│
│── src/
│   ├── app.py
│   ├── database.py
│   ├── download.py
│   ├── predict.py
│   ├── train_model.py
│   ├── static/
│   │   ├── style.css
│   │   ├── script.js
│   │   └── kidney-bg.jpg
│   ├── templates/
│       └── index.html
│
│── requirements.txt
│── Procfile
│── runtime.txt (optional)
│── README.md



nstallation (Local System)
1️⃣ Clone the repo
git<>
cd CHRONIC_PROJECT

2️⃣ Create virtual environment
python -m venv venv


Activate it

venv\Scripts\activate     # Windows
source venv/bin/activate  # Mac/Linux

3️⃣ Install dependencies
pip install -r requirements.txt

4️⃣ Set up MySQL locally

Create database:

CREATE DATABASE ckd_project;


Create table:

CREATE TABLE patient_records(
    id INT AUTO_INCREMENT PRIMARY KEY,
    patient_id VARCHAR(50),
    age FLOAT,
    bmi FLOAT,
    systolic_bp FLOAT,
    diastolic_bp FLOAT,
    serum_creatinine FLOAT,
    gfr FLOAT,
    hemoglobin_levels FLOAT,
    protein_in_urine FLOAT,
    fasting_blood_sugar FLOAT,
    hba1c FLOAT,
    family_history_kd FLOAT,
    prediction INT,
    probability FLOAT,
    notes TEXT
);

5️⃣ Run App
cd src
python app.py


Visit:
👉 http://127.0.0.1:5000

☁️ Deployment (Railway)
1️⃣ Create New Project → Deploy from GitHub

Railway: https://railway.app

2️⃣ Add MySQL Database Plugin

Railway automatically provides:

MYSQLHOST

MYSQLPORT

MYSQLUSER

MYSQLPASSWORD

MYSQLDATABASE

MYSQL_URL

3️⃣ Add to your Environment Variables

Go to:

Project → Variables

Add 👇 manually:

MYSQL_HOST = ${{ MySQL.MYSQLHOST }}
MYSQL_PORT = ${{ MySQL.MYSQLPORT }}
MYSQL_USER = ${{ MySQL.MYSQLUSER }}
MYSQL_PASSWORD = ${{ MySQL.MYSQLPASSWORD }}
MYSQL_DB = ${{ MySQL.MYSQLDATABASE }}
MYSQL_URL = ${{ MySQL.MYSQL_URL }}

4️⃣ Deploy

Railway automatically builds using:

Procfile
web: gunicorn app:app

requirements.txt (full working one)
Flask
gunicorn
pandas
numpy
scikit-learn
joblib
mysql-connector-python
reportlab

runtime.txt (optional)
python-3.10

🧪 Testing After Deployment

Run:

railway logs


Check:
✔ App running
✔ Connected to MySQL
✔ ML model loaded
✔ Predictions working

📚 API Endpoints
1️⃣ Home Page

GET /
Loads UI.

2️⃣ Prediction

POST /
Form submission.

3️⃣ Chatbot

POST /chatbot

Body:

{
  "message": "What is CKD?"
}


Response:

{
  "reply": "CKD stands for Chronic Kidney Disease..."
}
🎯 Future Improvements
✔ Add real-time charts
✔ Add login system
✔ Deploy as full-featured health monitoring dashboard



*Author*
Syeda Kanees Fathima
*Support*
If this project helped you, please star the GitHub repo ⭐💙
