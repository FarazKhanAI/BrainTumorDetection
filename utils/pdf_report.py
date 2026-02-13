from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas

def generate_report(patient, tumor, image_path, save_path):
    c = canvas.Canvas(save_path, pagesize=A4)
    c.setFont("Helvetica-Bold", 18)
    c.drawString(50, 800, "Brain Tumor Detection Report")

    c.setFont("Helvetica", 12)
    c.drawString(50, 760, f"Patient Name: {patient}")
    c.drawString(50, 740, f"Detected Tumor: {tumor}")

    c.drawImage(image_path, 50, 400, width=400, height=300)

    c.drawString(50, 360, "Note:")
    c.drawString(50, 340, "This report is AI-generated and for academic use only.")

    c.save()
