from __future__ import annotations
from sklearn.linear_model import LogisticRegression
import numpy as np

DRUG_INTERACTIONS = {
    frozenset(["aspirin", "warfarin"]): "Increased bleeding risk.",
    frozenset(["atorvastatin", "clarithromycin"]): "Higher risk of statin toxicity.",
}


def find_interactions(medicines: list[str]) -> list[str]:
    normalized = [m.lower() for m in medicines if m]
    alerts = []
    for pair, msg in DRUG_INTERACTIONS.items():
        if pair.issubset(set(normalized)):
            alerts.append(msg)
    return alerts


def abnormal_labs(records: list[dict]) -> list[str]:
    alerts = []
    for row in records:
        if not row.get("labName") or not row.get("labValue"):
            continue
        try:
            value = float(str(row["labValue"]).split()[0])
        except ValueError:
            continue
        name = row["labName"].lower()
        if "cholesterol" in name and value > 200:
            alerts.append(f"{row['labName']} is high ({value}).")
        if "glucose" in name and value > 126:
            alerts.append(f"{row['labName']} indicates hyperglycemia ({value}).")
        if "systolic" in name and value > 140:
            alerts.append(f"Blood pressure systolic value elevated ({value}).")
    return alerts


def risk_score(records: list[dict]) -> float:
    X = np.array([
        [110, 170],
        [130, 220],
        [145, 260],
        [120, 180],
    ])
    y = np.array([0, 1, 1, 0])
    model = LogisticRegression().fit(X, y)

    glucose = 100.0
    chol = 170.0
    for row in records:
        if row.get("labName") and row.get("labValue"):
            v = float(str(row["labValue"]).split()[0])
            n = row["labName"].lower()
            if "glucose" in n:
                glucose = v
            if "cholesterol" in n:
                chol = v

    prob = model.predict_proba(np.array([[glucose, chol]]))[0][1]
    return round(float(prob), 3)


def evaluate(records: list[dict]) -> dict:
    meds = [r["medicine"] for r in records if r.get("medicine")]
    return {
        "drug_interactions": find_interactions(meds),
        "abnormal_labs": abnormal_labs(records),
        "risk_score": risk_score(records),
    }
