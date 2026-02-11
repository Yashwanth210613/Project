# AI-Powered Clinical Decision Support & Patient Report Explanation

A full-stack web app for doctor/patient workflows:
- Doctors upload prescriptions/lab reports.
- Backend runs preprocessing + OCR + structured extraction.
- Clinical rules detect abnormal values/interactions + risk score.
- Patients see simplified explanations and summaries.

---

## 1) Tech Stack
- **Frontend:** React + Vite + Tailwind
- **Backend:** FastAPI + SQLAlchemy + JWT auth
- **OCR/Pipeline:** OpenCV + Tesseract + RapidFuzz
- **Decision Support:** Rule-based checks + scikit-learn risk model
- **Storage:** AWS S3 (or local fallback)
- **DB:** SQLite by default (swap to PostgreSQL for production)

---

## 2) Project Structure
```text
backend/
  app/
    api/              # auth + reports endpoints
    core/             # config, db, security
    models/           # SQLAlchemy models
    schemas/          # Pydantic schemas
    services/         # storage, preprocess, OCR, CDS, explanations
frontend/
  src/
    pages/            # Login/Register/Doctor/Patient dashboards
    components/       # Report UI
infra/
  serverless.yml      # sample OCR/CDS serverless handlers
docker-compose.yml
```

---

## 3) Prerequisites (Local)
Install these first:
- Python 3.11+
- Node.js 18+ (or 20+)
- npm
- Tesseract OCR binary

### Install Tesseract
- Ubuntu/Debian:
  ```bash
  sudo apt-get update && sudo apt-get install -y tesseract-ocr
  ```
- macOS (Homebrew):
  ```bash
  brew install tesseract
  ```
- Windows: install from UB Mannheim/GitHub build and add to PATH.

---

## 4) Run Locally (Step-by-Step)

### A. Start Backend
```bash
cd backend
cp .env.example .env
python -m venv .venv
source .venv/bin/activate   # Windows: .venv\\Scripts\\activate
pip install -r requirements.txt
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

Verify backend:
- Open: `http://localhost:8000/`
- Expected JSON: `{"status":"ok", "service":"Clinical AI CDS API"}`

### B. Start Frontend (new terminal)
```bash
cd frontend
npm install
npm run dev -- --host 0.0.0.0 --port 5173
```

Open UI:
- `http://localhost:5173`

---

## 5) How to See Output (End-to-End Demo)

1. Open `http://localhost:5173`.
2. **Register doctor** account.
3. Login as doctor and go to **Doctor Dashboard**.
4. Upload a sample image report/prescription.
5. You will see:
   - extracted structured data,
   - abnormal alerts (if any),
   - generated explanation text.
6. Register a **patient** account and login.
7. Open **Patient Dashboard** to view interpreted reports and summaries.

### What output is displayed
- Structured fields: `medicine`, `dosage`, `frequency`, `labName`, `labValue`, `normalRange`, confidence.
- Clinical decisions:
  - drug interaction warnings,
  - abnormal lab detection,
  - risk score (0–1).
- Patient-friendly plain-English explanation.

---

## 6) API Endpoints (Manual Testing)

### Auth
- `POST /auth/register`
- `POST /auth/login`

### Reports
- `POST /reports/upload` (doctor only)
- `GET /reports/`
- `GET /reports/{report_id}`

### Example register/login via curl
```bash
curl -X POST http://localhost:8000/auth/register \
  -H "Content-Type: application/json" \
  -d '{"email":"doc@example.com","password":"secret123","role":"doctor"}'
```

```bash
curl -X POST http://localhost:8000/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"doc@example.com","password":"secret123"}'
```

Use returned `access_token` as Bearer token for report APIs.

---

## 7) Run with Docker
```bash
docker compose up --build
```
Then open:
- Frontend: `http://localhost:5173`
- Backend: `http://localhost:8000`

---

## 8) Environment Variables
In `backend/.env`:
- `JWT_SECRET=super-secret`
- `DATABASE_URL=sqlite:///./clinical.db`
- `AWS_ACCESS_KEY_ID=...`
- `AWS_SECRET_ACCESS_KEY=...`
- `AWS_REGION=us-east-1`
- `S3_BUCKET_NAME=...`

If S3 vars are missing, local file storage fallback is used.

---

## 9) Deployment Notes
- Backend:
  - deploy FastAPI container to AWS EC2/ECS, or
  - package as Lambda + API Gateway.
- Frontend:
  - deploy `frontend/` to Vercel or Netlify.
  - set `VITE_API_URL` to deployed backend URL.
- Serverless placeholders for OCR/CDS workers are in `infra/serverless.yml`.

---

## 10) Production Hardening Checklist
- Move from SQLite to PostgreSQL.
- Use strong JWT secret and token rotation.
- Add migrations (Alembic).
- Add object-level authorization between doctor/patient/report entities.
- Add proper PDF OCR pipeline (`pdf2image`/Textract/etc.).
- Add robust multilingual translation model/service.
- Add automated tests and monitoring.
