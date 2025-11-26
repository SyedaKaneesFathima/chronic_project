# src/download.py
import os
import csv
import time
from flask import Blueprint, send_from_directory, abort, url_for
from werkzeug.utils import safe_join

# Optional PDF library
try:
    from reportlab.lib.pagesizes import A4
    from reportlab.lib.units import mm
    from reportlab.pdfgen import canvas
    REPORTLAB_AVAILABLE = True
except Exception:
    REPORTLAB_AVAILABLE = False

download_bp = Blueprint("download", __name__)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
RECORDS_DIR = os.path.join(BASE_DIR, "records")
os.makedirs(RECORDS_DIR, exist_ok=True)


def _timestamped_name(prefix, ext):
    ts = int(time.time())
    safe_prefix = str(prefix).replace(" ", "_")
    return f"{safe_prefix}_{ts}.{ext}"


def save_csv_record(data_dict, feature_names=None):
    """
    Save CSV in RECORDS_DIR with columns in the order of feature_names (if provided).
    Returns: URL (endpoint) for downloading the file.
    """
    patient_id = data_dict.get("PatientID") or data_dict.get("patient_id") or f"anon_{int(time.time())}"
    filename = _timestamped_name(patient_id, "csv")
    filepath = os.path.join(RECORDS_DIR, filename)

    # Build fieldnames/order
    if feature_names:
        # include PatientID and timestamp at start, then feature_names, then metadata
        fieldnames = ["PatientID", "timestamp"] + list(feature_names) + ["prediction", "probability", "Stage", "Advice"]
    else:
        fieldnames = list(data_dict.keys())

    # prepare row using desired order
    row = {}
    row["PatientID"] = patient_id
    row["timestamp"] = int(time.time())

    if feature_names:
        for feat in feature_names:
            row[feat] = data_dict.get(feat, 0)
        row["prediction"] = data_dict.get("prediction", "")
        row["probability"] = data_dict.get("probability", "")
        row["Stage"] = data_dict.get("Stage", "")
        row["Advice"] = data_dict.get("Advice", "")
    else:
        row.update(data_dict)

    # write CSV
    with open(filepath, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerow(row)

    return url_for("download.download_record", filename=filename)


def save_pdf_record(data_dict, title="CKD Report"):
    """
    Create a PDF that includes only:
      - PatientID (if present)
      - Stage, Advice, prediction, probability (if present)
      - Only the user-provided fields (non-empty strings OR numbers != 0)
    Returns: download URL (url_for inside this module's blueprint)
    Requires reportlab to be installed.
    """
    if not REPORTLAB_AVAILABLE:
        raise RuntimeError("ReportLab not installed. Install with: pip install reportlab")

    # choose patient id / filename
    patient_id = data_dict.get("PatientID") or data_dict.get("patient_id") or f"anon_{int(time.time())}"
    filename = _timestamped_name(patient_id, "pdf")
    filepath = os.path.join(RECORDS_DIR, filename)

    # Create canvas
    c = canvas.Canvas(filepath, pagesize=A4)
    width, height = A4
    left = 18 * mm
    top = height - 18 * mm

    # Title + meta
    c.setFont("Helvetica-Bold", 18)
    c.drawString(left, top, title)
    c.setFont("Helvetica", 10)
    c.drawString(left, top - 18, f"Patient ID: {patient_id}")
    c.drawString(left + 240, top - 18, f"Generated: {time.ctime()}")

    c.line(left, top - 22, width - left, top - 22)

    y = top - 40
    c.setFont("Helvetica", 10)

    # Always show Stage, Advice, Prediction, Probability if present
    always_show = ["Stage", "Advice", "prediction", "probability"]
    for key in always_show:
        if key in data_dict and data_dict[key] not in (None, "", 0):
            label = key.capitalize() if key not in ("prediction", "probability") else key
            c.drawString(left, y, f"{label}: {data_dict[key]}")
            y -= 14

    # Now collect only user-provided fields:
    # - keep keys that are not metadata keys and have a non-empty / non-zero value
    metadata_keys = set(["PatientID", "patient_id", "timestamp", "Stage", "Advice", "prediction", "probability"])
    provided_items = []
    for k, v in data_dict.items():
        if k in metadata_keys:
            continue
        # treat numbers: include if not zero
        if isinstance(v, (int, float)):
            if v != 0:
                provided_items.append((k, v))
        else:
            # strings: include if not empty
            if str(v).strip() != "":
                provided_items.append((k, v))

    # If no provided items found, write a note
    if not provided_items:
        c.drawString(left, y, "No additional patient fields were provided.")
        y -= 14
    else:
        # sort items alpha for stable order, or keep as-is; here keep provided order
        # Print in two columns
        col_x = [left, left + 260]
        col = 0
        line_h = 12
        for k, v in provided_items:
            if y < 30 * mm:
                c.showPage()
                y = height - 30 * mm
                c.setFont("Helvetica", 10)
            text = f"{k}: {v}"
            c.drawString(col_x[col], y, text)
            col = (col + 1) % 2
            if col == 0:
                y -= line_h

    c.showPage()
    c.save()

    # return download url (uses url_for in this module — download blueprint)
    return url_for("download.download_record", filename=filename)

@download_bp.route("/download/<path:filename>")
def download_record(filename):
    fullpath = safe_join(RECORDS_DIR, filename)
    if not fullpath or not os.path.isfile(fullpath):
        abort(404)
    return send_from_directory(RECORDS_DIR, filename, as_attachment=True)
