from __future__ import annotations
from langdetect import detect


def generate_explanation(records: list[dict], decision_output: dict, language: str = "en") -> str:
    summary = []
    for row in records:
        if row.get("labName"):
            summary.append(f"{row['labName']} is {row['labValue']} (normal range {row.get('normalRange') or 'not provided'}).")
        if row.get("medicine"):
            summary.append(f"Medicine noted: {row['medicine']} {row.get('dosage','')} {row.get('frequency','')}.")

    alerts = decision_output.get("abnormal_labs", []) + decision_output.get("drug_interactions", [])
    risk = decision_output.get("risk_score", 0)

    english = (
        "Here is your easy-to-read report summary: "
        + " ".join(summary)
        + f" Overall risk score is {risk}. "
        + ("Important alerts: " + "; ".join(alerts) if alerts else "No critical alerts detected.")
    )

    if language != "en":
        # Lightweight localization placeholder for Indian languages.
        return f"[{language}] {english}"

    try:
        if detect(english) != "en":
            return english
    except Exception:
        pass
    return english
