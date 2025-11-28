# import mysql.connector
# from mysql.connector import Error

# # ------------------------------
# # Connect to MySQL
# # ------------------------------
# def create_connection():
#     try:
#         conn = mysql.connector.connect(
#             host="localhost",
#             user="root",            
#             password="syeda1234@",
#             database="ckd_project"  
#         )
#         return conn
#     except Error as e:
#         print(f"❌ Error connecting to MySQL: {e}")
#         return None

# # ------------------------------
# # Save record to MySQL
# # ------------------------------
# def save_patient_record(data):
#     conn = create_connection()
#     if conn is None:
#         return False

#     try:
#         cursor = conn.cursor()
#         query = """
#             INSERT INTO patient_records (
#                 patient_id, age, bmi, systolic_bp, diastolic_bp,
#                 serum_creatinine, gfr, hemoglobin_levels, protein_in_urine,
#                 fasting_blood_sugar, hba1c, family_history_kd,
#                 prediction, probability, notes
#             ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
#         """
#         cursor.execute(query, data)
#         conn.commit()
#         cursor.close()
#         conn.close()
#         return True
#     except Error as e:
#         print(f"❌ Error saving record: {e}")
#         return False

import os
import mysql.connector
from mysql.connector import Error
from urllib.parse import urlparse

def create_connection():
    try:
        db_url = os.environ.get("MYSQL_URL")

        if db_url:
            parsed = urlparse(db_url)

            conn = mysql.connector.connect(
                host=parsed.hostname,
                user=parsed.username,
                password=parsed.password,
                port=parsed.port,
                database=parsed.path.lstrip("/")
            )
        else:
            # Local fallback
            conn = mysql.connector.connect(
                host="localhost",
                user="root",
                password="syeda1234@",
                database="ckd_project"
            )

        return conn

    except Error as e:
        print("❌ DB connection error:", e)
        return None
import json
from datetime import datetime

def save_patient_record(record):
    """
    Saves the patient's data into MySQL database.
    'record' is the tuple passed from app.py.
    """
    conn = create_connection()
    if conn is None:
        print("❌ Could not connect to DB")
        return False

    try:
        cursor = conn.cursor()

        # Create the table if it doesn't exist
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS records (
                id INT AUTO_INCREMENT PRIMARY KEY,
                patient_id VARCHAR(255),
                data_json TEXT,
                prediction INT,
                probability FLOAT,
                note TEXT,
                created_at DATETIME
            )
        """)

        # Extract fields
        patient_id = record[0]
        prediction = record[-3]
        probability = record[-2]
        note = record[-1]

        # Convert the middle part to JSON
        data_json = json.dumps(record[1:-3], default=str)

        cursor.execute("""
            INSERT INTO records (patient_id, data_json, prediction, probability, note, created_at)
            VALUES (%s, %s, %s, %s, %s, %s)
        """, (patient_id, data_json, prediction, probability, note, datetime.now()))

        conn.commit()
        conn.close()
        return True

    except Exception as e:
        print("❌ Error saving patient:", e)
        return False
