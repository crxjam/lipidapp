import csv
from pathlib import Path
from datetime import datetime
from typing import Dict, Any


DATA_DIR = Path("data")
UPLOAD_DIR = DATA_DIR / "uploads"
LABEL_FILE = DATA_DIR / "labels.csv"

UPLOAD_DIR.mkdir(parents=True, exist_ok=True)


def save_label(record: Dict[str, Any]) -> Dict[str, str]:
    LABEL_FILE.parent.mkdir(parents=True, exist_ok=True)

    fieldnames = [
        "timestamp",
        "filename",
        "suggested_classification",
        "confirmed_classification",
        "confidence",
        "comments",
        "origin_peak",
        "beta_increased",
        "prebeta_increased",
        "broad_beta",
        "lpx_suspected",
        "sample_quality_issue",
    ]

    file_exists = LABEL_FILE.exists()

    row = {key: record.get(key, "") for key in fieldnames}
    row["timestamp"] = datetime.utcnow().isoformat()

    with LABEL_FILE.open("a", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)

        if not file_exists:
            writer.writeheader()

        writer.writerow(row)

    return {"status": "saved", "file": str(LABEL_FILE)}
