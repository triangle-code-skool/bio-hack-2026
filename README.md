# UltraViab: AI-Powered Organ Viability Assessment

UltraViab is a multi-modal AI platform designed to assess organ viability for transplants using deep analysis of medical metadata and ultrasound metrics (stiffness, perfusion, resistive index).

## Project Architecture
- **Backend**: FastAPI server (`api/`) providing predictive inference.
- **Frontend**: Streamlit dashboard (`dashboard/`) with modern UI components and real-time visualizations.

---

## 🚀 Setup Instructions

### 1. Prerequisites
- Python 3.10 or higher
- Git

### 2. Clone the Repository
```bash
git clone https://github.com/triangle-code-skool/bio-hack-2026.git
cd bio-hack-2026
```

### 3. Environment Setup
It is recommended to use a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # Mac/Linux
# venv\Scripts\activate   # Windows
```

---

## 🛠 Running the Application

To run the full suite, you need to start both the **Backend API** and the **Frontend Dashboard**.

### Part A: Backend API
The API handles the viability scoring logic.
```bash
cd api
pip install -r requirements.txt
uvicorn app:app --host 0.0.0.0 --port 8000 --reload
```
*The API will be available at `http://localhost:8000`.*

### Part B: Frontend Dashboard
The dashboard provides the user interface for organ assessment.
```bash
# Open a new terminal tab, ensure venv is active
cd dashboard
pip install -r requirements.txt
streamlit run app.py
```
*The dashboard will be available at `http://localhost:8501`.*

---

## 📊 Features
- **Real-time Ultrasound Pulse**: Simulated live signal monitoring.
- **Detailed Analysis**: Radar charts and feature impact visualizations.
- **High-Contrast Dark Mode**: Optimized for medical professional environments.
- **Scenario Simulation**: Adjustable sliders for age, CIT, and tissue stiffness.

## 🤝 Contribution
This project was built during the BioHack 2026 hackathon.