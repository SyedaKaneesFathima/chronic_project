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

def create_connection():
    try:
        db_url = os.environ.get("MYSQL_URL")

        if db_url:
            # Railway gives full URL
            conn = mysql.connector.connect(
                host=db_url.split("@")[1].split(":")[0],
                port=db_url.split(":")[-1].split("/")[0],
                user=db_url.split("//")[1].split(":")[0],
                password=db_url.split(":")[2].split("@")[0],
                database=db_url.split("/")[-1]
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
