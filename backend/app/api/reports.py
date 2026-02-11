from fastapi import APIRouter, Depends, File, UploadFile, HTTPException
from sqlalchemy.orm import Session
from app.api.deps import get_current_user
from app.core.database import get_db
from app.models.models import Report, User
from app.services.storage import upload_file
from app.services.preprocess import preprocess_image
from app.services.ocr import extract_ocr_text, parse_structured
from app.services.decision_support import evaluate
from app.services.explainer import generate_explanation

router = APIRouter(prefix="/reports", tags=["reports"])


@router.post("/upload")
async def upload_report(
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
):
    if user.role != "doctor":
        raise HTTPException(status_code=403, detail="Only doctors can upload reports")

    blob = await file.read()
    storage_url = upload_file(blob, file.filename)
    processed_path = preprocess_image(storage_url) if file.filename.lower().endswith((".png", ".jpg", ".jpeg")) else storage_url

    ocr_text, conf = extract_ocr_text(processed_path)
    structured = parse_structured(ocr_text, conf)
    decision = evaluate(structured)
    explanation = generate_explanation(structured, decision)

    report = Report(
        owner_id=user.id,
        original_filename=file.filename,
        storage_url=storage_url,
        ocr_text=ocr_text,
        structured_data=structured,
        decision_support=decision,
        explanation=explanation,
    )
    db.add(report)
    db.commit()
    db.refresh(report)

    return {
        "report_id": report.id,
        "structured_data": structured,
        "decision_support": decision,
        "explanation": explanation,
    }


@router.get("/{report_id}")
def get_report(report_id: int, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    report = db.query(Report).filter(Report.id == report_id).first()
    if not report:
        raise HTTPException(status_code=404, detail="Not found")
    if user.role == "patient" and report.owner_id != user.id:
        raise HTTPException(status_code=403, detail="Access denied")

    return {
        "id": report.id,
        "original_filename": report.original_filename,
        "structured_data": report.structured_data,
        "decision_support": report.decision_support,
        "explanation": report.explanation,
    }


@router.get("/")
def list_reports(db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    query = db.query(Report)
    if user.role == "patient":
        query = query.filter(Report.owner_id == user.id)
    reports = query.order_by(Report.created_at.desc()).all()
    return [{"id": r.id, "filename": r.original_filename, "created_at": r.created_at} for r in reports]
