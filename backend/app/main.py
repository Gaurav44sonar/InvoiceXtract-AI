from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import shutil
import os

from app.services.pdf_processor import PDFProcessor
from app.services.ai_extractor import AIExtractor

# -------------------------------------------------
# App initialization
# -------------------------------------------------
app = FastAPI(
    title="Invoice OCR System",
    description="Upload invoice PDFs and extract structured data using AI",
    version="1.0.0",
)

# -------------------------------------------------
# CORS (IMPORTANT for frontend connection)
# -------------------------------------------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
    "http://localhost:5173",
    "http://localhost:3000",
    "http://localhost:8080",   # ← ADD THIS
],

    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# -------------------------------------------------
# Services
# -------------------------------------------------
pdf_processor = PDFProcessor()
ai_extractor = AIExtractor()

# -------------------------------------------------
# Upload directory
# -------------------------------------------------
UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

# -------------------------------------------------
# Health check (optional but useful)
# -------------------------------------------------
@app.get("/")
def root():
    return {
        "status": "running",
        "message": "Invoice OCR Backend is running",
    }

# -------------------------------------------------
# Main endpoint: Upload & extract invoice
# -------------------------------------------------
@app.post("/extract-invoice")
async def extract_invoice(file: UploadFile = File(...)):
    # Validate file type
    if not file.filename.lower().endswith(".pdf"):
        raise HTTPException(
            status_code=400,
            detail="Only PDF files are supported",
        )

    # Save uploaded file
    pdf_path = os.path.join(UPLOAD_DIR, file.filename)
    with open(pdf_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    try:
        # 1️⃣ Extract text from PDF
        text = pdf_processor.extract_text(pdf_path)

        # 2️⃣ Extract tables from PDF
        tables = pdf_processor.extract_tables(pdf_path)

        # 3️⃣ AI extraction
        result = ai_extractor.extract_from_text(text, tables)

        return result

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=str(e),
        )
