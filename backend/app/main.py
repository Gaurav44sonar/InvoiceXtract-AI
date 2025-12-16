# from fastapi import FastAPI, UploadFile, File, HTTPException
# from fastapi.responses import JSONResponse
# from pathlib import Path
# import shutil

# from app.services.ai_extractor import AIExtractor
# from app.services.pdf_processor import PDFProcessor

# app = FastAPI(
#     title="Invoice OCR System",
#     description="Automated invoice data extraction using OCR and AI",
#     version="1.0.0"
# )

# UPLOAD_DIR = Path("uploads")
# UPLOAD_DIR.mkdir(exist_ok=True)

# extractor = AIExtractor()
# pdf_processor = PDFProcessor()


# @app.get("/")
# def root():
#     return {
#         "message": "Welcome to Invoice OCR System 🚀",
#         "status": "Server is running",
#         "version": "1.0.0",
#         "endpoints": {
#             "docs": "/docs",
#             "health": "/health",
#             "test": "/test",
#             "extract": "/extract-invoice"
#         }
#     }


# @app.get("/health")
# def health():
#     return {"status": "ok"}


# @app.get("/test")
# def test():
#     return {"message": "Test endpoint working"}


# # 🔥 THIS IS THE MISSING ENDPOINT
# @app.post("/extract-invoice")
# async def extract_invoice(file: UploadFile = File(...)):
#     if not file.filename.lower().endswith(".pdf"):
#         raise HTTPException(status_code=400, detail="Only PDF files are supported")

#     pdf_path = UPLOAD_DIR / file.filename

#     with pdf_path.open("wb") as buffer:
#         shutil.copyfileobj(file.file, buffer)

#     try:
#         text, tables = pdf_processor.process(pdf_path)

#         combined_text = text
#         if tables:
#             combined_text += "\n\nTABLE DATA:\n"
#             for t in tables:
#                 combined_text += str(t) + "\n"

#         result = extractor.extract_from_text(combined_text)
#         return JSONResponse(content=result)

#     except Exception as e:
#         raise HTTPException(status_code=500, detail=str(e))


# app/main.py

from fastapi import FastAPI, UploadFile, File, HTTPException
import shutil
import os

from app.services.pdf_processor import PDFProcessor
from app.services.ai_extractor import AIExtractor

app = FastAPI(title="Invoice OCR System")

pdf_processor = PDFProcessor()
ai_extractor = AIExtractor()

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)


@app.post("/extract-invoice")
async def extract_invoice(file: UploadFile = File(...)):
    if not file.filename.lower().endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Only PDF files supported")

    pdf_path = os.path.join(UPLOAD_DIR, file.filename)

    with open(pdf_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    # 1️⃣ Extract text
    text = pdf_processor.extract_text(pdf_path)

    # 2️⃣ Extract tables
    tables = pdf_processor.extract_tables(pdf_path)

    # 3️⃣ AI extraction (FIX IS HERE)
    result = ai_extractor.extract_from_text(text, tables)

    return result
