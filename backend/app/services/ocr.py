from __future__ import annotations
import re
from rapidfuzz import process
import pytesseract
from PIL import Image

KNOWN_MEDS = ["paracetamol", "metformin", "atorvastatin", "amlodipine", "aspirin"]


def extract_ocr_text(path: str) -> tuple[str, float]:
    data = pytesseract.image_to_data(Image.open(path), output_type=pytesseract.Output.DICT)
    words = [w for w in data["text"] if w.strip()]
    confs = [float(c) for c in data["conf"] if c not in ("-1", -1)]
    avg_conf = round(sum(confs) / len(confs), 2) if confs else 0.0
    return " ".join(words), avg_conf


def fuzzy_medicine(name: str) -> tuple[str, float]:
    match = process.extractOne(name.lower(), KNOWN_MEDS)
    if not match:
        return name, 0.0
    return match[0], float(match[1]) / 100


def parse_structured(text: str, base_confidence: float) -> list[dict]:
    records: list[dict] = []
    med_pattern = re.compile(r"([A-Za-z]+)\s+(\d+\s*mg)\s*(OD|BD|TDS)?", re.IGNORECASE)
    lab_pattern = re.compile(r"([A-Za-z\s]+):?\s*(\d+\.?\d*)\s*(mg/dL|mmol/L|g/dL)?\s*(\(?\d+\-\d+\)?)?", re.IGNORECASE)

    for med, dose, freq in med_pattern.findall(text):
        best_med, fuzzy_conf = fuzzy_medicine(med)
        records.append(
            {
                "medicine": best_med,
                "dosage": dose,
                "frequency": freq or "",
                "labName": None,
                "labValue": None,
                "normalRange": None,
                "confidence": round((base_confidence / 100 + fuzzy_conf) / 2, 2),
            }
        )

    for lab, value, unit, normal in lab_pattern.findall(text):
        if any(ch.isdigit() for ch in lab.strip()):
            continue
        records.append(
            {
                "medicine": None,
                "dosage": None,
                "frequency": None,
                "labName": lab.strip(),
                "labValue": f"{value} {unit}".strip(),
                "normalRange": normal.strip("()") if normal else "",
                "confidence": round(base_confidence / 100, 2),
            }
        )

    return records
