from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from bson import ObjectId
from datetime import datetime
import shutil
import os

from pymongo import MongoClient
from app.services.pdf_processor import PDFProcessor
from app.services.ai_extractor import AIExtractor

# -------------------------------------------------
# App Init
# -------------------------------------------------
app = FastAPI(
    title="InvoiceXtract AI",
    version="1.0.0"
)

# -------------------------------------------------
# CORS
# -------------------------------------------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:8080",
        "http://127.0.0.1:8080",
        "http://localhost:5173",
        "http://127.0.0.1:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
# -------------------------------------------------
# ENV + MongoDB
# -------------------------------------------------
MONGO_URI = os.getenv("MONGO_URI")
DB_NAME = os.getenv("MONGO_DB", "invoice_xtract")

if not MONGO_URI:
    raise RuntimeError("❌ MONGO_URI not set in .env")

mongo_client = MongoClient(MONGO_URI)
db = mongo_client[DB_NAME]
invoice_collection = db["invoices"]

# -------------------------------------------------
# Services
# -------------------------------------------------
pdf_processor = PDFProcessor()
ai_extractor = AIExtractor()

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

# -------------------------------------------------
# Health
# -------------------------------------------------
@app.get("/")
def root():
    return {"status": "Backend running"}

# -------------------------------------------------
# 1️⃣ Extract Invoice (NO SAVE)
# -------------------------------------------------
@app.post("/extract-invoice")
async def extract_invoice(file: UploadFile = File(...)):
    if not file.filename.lower().endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Only PDF allowed")

    pdf_path = os.path.join(UPLOAD_DIR, file.filename)
    with open(pdf_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    text = pdf_processor.extract_text(pdf_path)
    tables = pdf_processor.extract_tables(pdf_path)
    result = ai_extractor.extract_from_text(text, tables)

    return result

# -------------------------------------------------
# 2️⃣ Save Invoice to MongoDB
# -------------------------------------------------
@app.post("/save-invoice")
def save_invoice(payload: dict):
    try:
        doc = {
            "file_name": payload.get("file_name"),
            "invoice_number": payload.get("invoice_number"),
            "invoice_date": payload.get("invoice_date"),
            "vendor_name": payload.get("vendor", {}).get("name"),
            "subtotal": payload.get("subtotal"),
            "tax_amount": payload.get("tax_amount"),
            "total": payload.get("total"),
            "currency": payload.get("currency"),
            "items": payload.get("items", []),
            "created_at": datetime.utcnow()
        }

        res = invoice_collection.insert_one(doc)
        return {"success": True, "id": str(res.inserted_id)}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# -------------------------------------------------
# 3️⃣ Get Invoice History
# -------------------------------------------------
@app.get("/invoices")
def get_invoices():
    invoices = []

    for inv in invoice_collection.find().sort("created_at", -1):
        invoices.append({
            "id": str(inv["_id"]),
            "file_name": inv.get("file_name"),
            "upload_date": inv.get("created_at"),
            "status": "processed",
            "data": {
                "invoice_number": inv.get("invoice_number"),
                "invoice_date": inv.get("invoice_date"),
                "vendor_name": inv.get("vendor_name"),
                "gst_amount": inv.get("tax_amount"),
                "total_amount": inv.get("total"),
                "line_items": inv.get("items", [])
            }
        })

    return invoices


# -------------------------------------------------
# 4️⃣ Get Single Invoice
# -------------------------------------------------
@app.get("/invoices/{invoice_id}")
def get_invoice(invoice_id: str):
    inv = invoice_collection.find_one({"_id": ObjectId(invoice_id)})
    if not inv:
        raise HTTPException(status_code=404, detail="Not found")

    return {
        "id": str(inv["_id"]),
        "file_name": inv.get("file_name"),
        "upload_date": inv.get("created_at"),
        "status": "processed",
        "data": {
            "invoice_number": inv.get("invoice_number"),
            "invoice_date": inv.get("invoice_date"),
            "vendor_name": inv.get("vendor_name"),
            "gst_amount": inv.get("tax_amount"),
            "total_amount": inv.get("total"),
            "line_items": inv.get("items", [])
        }
    }
