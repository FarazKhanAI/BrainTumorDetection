from flask import Flask, render_template, request, redirect, url_for, session
from ultralytics import YOLO
import os, cv2, uuid
from datetime import datetime
import pandas as pd
import matplotlib.pyplot as plt

# ------------------- PDF Imports -------------------
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import inch

# ------------------- Database -------------------
from utils.database import init_db, save_record, get_history, get_dashboard_data
init_db()

# ------------------- Flask Setup -------------------
app = Flask(__name__)
app.secret_key = "supersecretkey"

model = YOLO("runs/detect/brain_tumor_detection/weights/best.pt")

UPLOAD_FOLDER = "static/uploads"
RESULT_FOLDER = "static/results"
REPORT_FOLDER = "static/reports"
CHART_FOLDER = "static/charts"

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(RESULT_FOLDER, exist_ok=True)
os.makedirs(REPORT_FOLDER, exist_ok=True)
os.makedirs(CHART_FOLDER, exist_ok=True)

# ------------------- LOGIN -------------------
DOCTOR_USERNAME = "doctor"
DOCTOR_PASSWORD = "1234"

@app.route("/login", methods=["GET","POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        if username == DOCTOR_USERNAME and password == DOCTOR_PASSWORD:
            session["doctor"] = True
            return redirect("/")
        else:
            return render_template("login.html", error="Invalid Credentials")

    return render_template("login.html")

@app.route("/logout")
def logout():
    session.clear()
    return redirect("/login")

# ------------------- PDF Generator -------------------
def generate_pdf(filename, patient_name, age, gender, tumor, confidence):
    pdf_filename = filename.replace(".jpg", ".pdf")
    pdf_path = os.path.join(REPORT_FOLDER, pdf_filename)

    doc = SimpleDocTemplate(pdf_path, pagesize=A4)
    elements = []

    style = ParagraphStyle(name='NormalStyle', fontSize=12, spaceAfter=10)

    elements.append(Paragraph("<b>Hospital Brain Tumor Report</b>", style))
    elements.append(Spacer(1, 20))

    elements.append(Paragraph(f"Patient Name: {patient_name}", style))
    elements.append(Paragraph(f"Age: {age}", style))
    elements.append(Paragraph(f"Gender: {gender}", style))
    elements.append(Paragraph(f"Tumor Type: {tumor}", style))
    elements.append(Paragraph(f"Confidence: {confidence}%", style))
    elements.append(Paragraph(f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M')}", style))

    elements.append(Spacer(1, 20))

    img_path = os.path.join(RESULT_FOLDER, filename)
    elements.append(Image(img_path, width=4*inch, height=4*inch))

    elements.append(Spacer(1, 20))
    elements.append(Paragraph("<b>Recommendation:</b> Immediate neurologist consultation advised.", style))

    doc.build(elements)

    return pdf_filename

# ------------------- MAIN ROUTE -------------------
@app.route("/", methods=["GET","POST"])
def index():
    if "doctor" not in session:
        return redirect("/login")

    if request.method == "POST":
        files = request.files.getlist("file")
        patient_name = request.form.get("patient_name")
        age = request.form.get("age")
        gender = request.form.get("gender")

        results_data = []

        for file in files:
            filename = str(uuid.uuid4()) + ".jpg"
            upload_path = os.path.join(UPLOAD_FOLDER, filename)
            file.save(upload_path)

            results = model(upload_path)
            plotted_img = results[0].plot()

            result_path = os.path.join(RESULT_FOLDER, filename)
            cv2.imwrite(result_path, plotted_img)

            detections = []
            pdf_file = None

            for box in results[0].boxes:
                cls_id = int(box.cls[0])
                conf = float(box.conf[0])
                label = model.names[cls_id]
                confidence = round(conf * 100, 2)

                save_record(patient_name, age, gender, label, confidence)

                pdf_file = generate_pdf(
                    filename,
                    patient_name,
                    age,
                    gender,
                    label,
                    confidence
                )

                detections.append({
                    "label": label,
                    "confidence": confidence
                })

            results_data.append({
                "image": f"{RESULT_FOLDER}/{filename}",
                "detections": detections,
                "pdf": f"{REPORT_FOLDER}/{pdf_file}" if pdf_file else None
            })

        return render_template("results.html", results=results_data)

    return render_template("index.html")

# ------------------- HISTORY -------------------
@app.route("/history")
def history():
    if "doctor" not in session:
        return redirect("/login")
    records = get_history()
    return render_template("history.html", records=records)

# ------------------- DASHBOARD -------------------
@app.route("/dashboard")
def dashboard():
    if "doctor" not in session:
        return redirect("/login")

    data = get_dashboard_data()
    df = pd.DataFrame(data, columns=["tumor","gender"])

    tumor_counts = df["tumor"].value_counts()
    plt.figure()
    tumor_counts.plot(kind="bar")
    plt.title("Tumor Distribution")
    tumor_chart = os.path.join(CHART_FOLDER,"tumor_chart.png")
    plt.savefig(tumor_chart)
    plt.close()

    gender_counts = df["gender"].value_counts()
    plt.figure()
    gender_counts.plot(kind="pie", autopct="%1.1f%%")
    plt.title("Gender Distribution")
    gender_chart = os.path.join(CHART_FOLDER,"gender_chart.png")
    plt.savefig(gender_chart)
    plt.close()

    return render_template("dashboard.html",
                           tumor_chart=tumor_chart,
                           gender_chart=gender_chart)

# ------------------- ADMIN PANEL -------------------
@app.route("/admin")
def admin():
    if "doctor" not in session:
        return redirect("/login")
    records = get_history()
    return render_template("admin.html", records=records)

if __name__ == "__main__":
    app.run(debug=True)
