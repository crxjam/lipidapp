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


class ManualFeatures(BaseModel):
    filename: str = ""
    origin_peak: bool = False
    beta_increased: bool = False
    prebeta_increased: bool = False
    broad_beta: bool = False
    lpx_suspected: bool = False
    sample_quality_issue: bool = False
    alpha_visible: bool = True


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
