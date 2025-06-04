# 🩺 Patient Health API

A RESTful API for managing patient data and health measurements using **FastAPI**, **SQLAlchemy** and **SQLite3**.

---

## 🚀 Setup Instructions

### 1. Clone the repository

```bash
git clone https://github.com/DavidGomezSancho/patient-health-api.git
cd patient-health-api
```

### 2. Create and activate virtual environment (python version 2.12)

```bash
python -m venv .venv
source .venv/bin/activate  # On Windows use `.venv\Scripts\activate`
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Run database init script

```bash
python -m database.init_db
```
### 5. Run ETL

```bash
python -m etl.main
```

### 6. Run Analytic job (remains in the background running every hour)

```bash
python -m analytic.main &
```

### 7. Start the API

```bash
uvicorn server.main:app --reload
```
It runs on port 8000

---

## 📘 API Documentation

FastAPI automatically generates documentation:

- Swagger UI: [http://localhost:8000/docs](http://localhost:8000/docs)
- ReDoc: [http://localhost:8000/redoc](http://localhost:8000/redoc)

### 🔹 Key Endpoints

| Method | Endpoint                               | Description                          |
|--------|----------------------------------------|--------------------------------------|
| GET    | `/patient`                             | Get list of patients                 |
| GET    | `/patient/{patient_id}/measure`        | Get patient biometric history        |
| POST   | `/patient/{patient_id}/measure`        | Upsert a patient biometric           |
| DELETE | `/measure/{measure_id}`                | Delete a patient biometric           |
| GET    | `/patient/{patient_id}/derivedmeasure` | Get List patient biometric analytics |



---

## 🧠 Key Design Decisions & Assumptions

- **UUIDs** are used as public identifiers for patients and measures.
- **Upsert behavior**: If `public_id` is provided in the payload and exists, the record is updated. Otherwise, a new one is created.
- **Data validation**: Uses `Pydantic` models and `Pandera` for runtime data validation.
- **Units and conversions**: Handled using `Enum` classes and a `Quantity` factory pattern for extensibility.

---

## 🗃️ Database Schema Overview

```text
Patient
├── id (PK) — Internal unique identifier
├── public_id (UUID, unique) — Public-facing identifier
├── name — Full name of the patient
├── dob — Date of birth
├── gender / sex — Gender identity and biological sex
├── address, email, phone — Contact information

MeasureHealth
├── id (PK) — Internal unique identifier
├── public_id (UUID, unique) — Public-facing identifier
├── id_patient (FK → Patient.id) — Reference to the patient
├── weight — Body weight (lb)
├── glucose — Blood glucose level (mg/dL)
├── press_syst / press_diast — Blood pressure (systolic/diastolic) (mmHg)
├── created_at — Timestamp of the measurement

DerivedMeasureHealth
├── id (PK) — Internal unique identifier
├── id_patient (FK → Patient.id) — Reference to the patient
├── max/min/av_weight — Weight stats
├── max/min/av_glucose — Glucose stats
├── max/min/av_press_syst — Systolic pressure stats
├── max/min/av_press_diast — Diastolic pressure stats
├── created_at — Timestamp of data aggregation
```

> Database is managed via **SQLAlchemy ORM** and **SQLite**.

---

## 🧱 Architecture

```text
The application follows a modular architecture. Each major component -ETL, analytics calculation, database and the FastAPI server- is implemented as an independent module. The only exception is the database module, which is shared and imported by the other components as a dependency.
```

---


## 📌 Future Improvements

- OAuth2 authentication
- Testing
- Trend Analysis
- Dagster for CronJobs
- Dockerization and CI/CD pipeline

---
