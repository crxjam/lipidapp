from pathlib import Path
from typing import List

from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from app.rules_engine import classify_fredrickson
from app.training_data import save_label, UPLOAD_DIR


app = FastAPI(title="Lipid Electrophoresis Classifier")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class BiochemistryInput(BaseModel):
    filename: str = ""
    total_cholesterol: float
    triglycerides: float
    hdl: float
    ldl: float | None = None


@app.post("/classify-biochemistry")
def classify_biochemistry(values: BiochemistryInput):
    tc = values.total_cholesterol
    tg = values.triglycerides
    hdl = values.hdl
    ldl = values.ldl

    non_hdl = tc - hdl

    reasons = []

    if tg >= 10:
        classification = "Severe hypertriglyceridaemia pattern — correlate with chylomicrons/VLDL on electrophoresis"
        reasons.append("Triglycerides are severely increased.")
    elif ldl is not None and ldl >= 5 and tg < 2.3:
        classification = "Possible Type IIa pattern"
        reasons.append("LDL-C is markedly increased with triglycerides not markedly increased.")
    elif ldl is not None and ldl >= 5 and tg >= 2.3:
        classification = "Possible Type IIb pattern"
        reasons.append("LDL-C and triglycerides are both increased.")
    elif tg >= 2.3 and non_hdl > 4:
        classification = "Possible Type IV or Type IIb pattern"
        reasons.append("Triglycerides and non-HDL cholesterol are increased.")
    elif tg >= 2.3:
        classification = "Possible Type IV pattern"
        reasons.append("Triglycerides are increased, suggesting increased VLDL.")
    else:
        classification = "No clear biochemical Fredrickson pattern"
        reasons.append("Biochemistry alone does not show a clear major hyperlipoproteinaemia pattern.")

    return {
        "input": values.dict(),
        "calculated": {
            "non_hdl_cholesterol": round(non_hdl, 2)
        },
        "result": {
            "classification": classification,
            "confidence": "low to moderate",
            "reasons": reasons,
            "important_note": "Biochemistry alone should not replace electrophoresis pattern recognition. Final classification should use the gel/densitometry pattern."
        }
    }


class LabelRecord(ManualFeatures):
    suggested_classification: str = ""
    confirmed_classification: str
    confidence: str = ""
    comments: str = ""


@app.get("/")
def root():
    return {"message": "Lipid electrophoresis classifier backend running"}


@app.post("/classify-manual")
def classify_manual(features: ManualFeatures):
    result = classify_fredrickson(features.dict())
    return {
        "features": features.dict(),
        "result": result,
    }


@app.post("/upload-one")
async def upload_one(file: UploadFile = File(...)):
    destination = UPLOAD_DIR / file.filename

    with destination.open("wb") as f:
        f.write(await file.read())

    return {
        "status": "uploaded",
        "filename": file.filename,
        "next_step": "Manual feature classification now; automated curve extraction will be added next.",
    }


@app.post("/batch-upload")
async def batch_upload(files: List[UploadFile] = File(...)):
    saved = []

    for file in files:
        destination = UPLOAD_DIR / file.filename

        with destination.open("wb") as f:
            f.write(await file.read())

        saved.append(file.filename)

    return {
        "status": "uploaded",
        "count": len(saved),
        "files": saved,
    }


@app.post("/save-label")
def save_confirmed_label(record: LabelRecord):
    return save_label(record.dict())
