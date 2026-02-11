# AI-Powered Clinical Decision Support & Patient Report Explanation

Complete full-stack project with FastAPI backend + React frontend for doctor/patient workflows, OCR processing, structured extraction, decision support, and patient-friendly explanations.

## Features
- JWT authentication with doctor/patient roles.
- Doctor dashboard for uploading prescriptions/lab reports.
- Patient dashboard for interpreted reports and summaries.
- File storage via AWS S3 (or local fallback).
- OpenCV preprocessing + Tesseract OCR.
- Confidence scoring + fuzzy medicine matching.
- Structured JSON extraction (`medicine`, `dosage`, `frequency`, `labName`, `labValue`, `normalRange`).
- Rule-based clinical decision support + risk score model (scikit-learn).
- NLP explanation generation with optional language prefix fallback.
- Deployable via Docker, AWS Lambda hooks, Vercel/Netlify friendly frontend.

## Folder Structure
```
backend/
  app/
    api/
    core/
    models/
    schemas/
    services/
frontend/
  src/
infra/
  serverless.yml
```

## Local Run
### Backend
```bash
cd backend
cp .env.example .env
pip install -r requirements.txt
uvicorn app.main:app --reload
```

### Frontend
```bash
cd frontend
npm install
npm run dev
```

## Docker Run
```bash
docker compose up --build
```

## API Endpoints
- `POST /auth/register`
- `POST /auth/login`
- `POST /reports/upload`
- `GET /reports/`
- `GET /reports/{report_id}`

## Deployment
- Backend: deploy container to AWS EC2/ECS, or package FastAPI for Lambda with API Gateway.
- Frontend: deploy `frontend` to Vercel/Netlify (`VITE_API_URL` env var).
- OCR/CDS serverless hooks are scaffolded in `infra/serverless.yml`.

## Notes
- For production, replace SQLite with PostgreSQL and configure strong JWT secret.
- To support PDFs, integrate `pdf2image` or external OCR service in `services/ocr.py`.
- To add true multilingual output, integrate translation model/API in `services/explainer.py`.
