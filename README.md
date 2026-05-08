# 🧠 AI Brain Tumor Detection System

An AI-powered web application for detecting brain tumors from MRI images using YOLO (Ultralytics).  
The system includes doctor authentication, automated medical PDF reports, patient history storage, an admin panel, and a statistics dashboard.

---

## 🚀 Features

### 🔍 AI Tumor Detection
- Uses YOLO deep learning model
- Supports multiple MRI image uploads
- Displays detected tumor type with confidence score

### 👨‍⚕️ Doctor Login System
- Secure login panel
- Protected routes
- Session-based authentication

### 📄 Automated Medical PDF Report
- Generates professional hospital-style reports
- Includes:
  - Patient details
  - Tumor type
  - Confidence percentage
  - Detection image
  - Date and recommendation
- Downloadable as PDF

### 📊 Tumor Statistics Dashboard
- Tumor type distribution (Bar Chart)
- Gender distribution (Pie Chart)
- Generated dynamically from database

### 🗂 Admin Panel
- View all patient records
- Includes:
  - Name
  - Age
  - Gender
  - Tumor type
  - Confidence
  - Date

### 💾 Database Storage
- SQLite database
- Stores all patient detection records
- Automatically created on first run

### 🌐 Deployment Ready
- Configured for deployment on Render
- Includes `Procfile`
- Uses Gunicorn production server

---

## 🏗 Project Structure
```
BrainTumorDetection/
│
├── app.py
├── requirements.txt
├── Procfile
├── database.db
│
├── utils/
│ └── database.py
│
├── static/
│ ├── uploads/
│ ├── results/
│ ├── reports/
│ ├── charts/
│ └── logo.png
│
├── templates/
│ ├── login.html
│ ├── index.html
│ ├── results.html
│ ├── history.html
│ ├── dashboard.html
│ └── admin.html
```

---

## 🛠 Installation Guide

### 1️⃣ Clone the Repository

```bash
git clone https://github.com/your-username/BrainTumorDetection.git
cd BrainTumorDetection
2️⃣ Create Virtual Environment
python -m venv venv
venv\Scripts\activate   # Windows
3️⃣ Install Dependencies
pip install -r requirements.txt
4️⃣ Run the Application
python app.py
Visit:

http://127.0.0.1:5000



🔐 Default Login Credentials
Username: doctor
Password: 1234
You can change these inside app.py.





🧠 Future Improvements

Password hashing (bcrypt)

Cloud database (PostgreSQL)

User role management

Model accuracy monitoring

Real hospital-grade UI design

Cloud storage for images

REST API version


