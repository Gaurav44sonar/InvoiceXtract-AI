"""
Configuration Management Module
"""

import os
import sys
from pathlib import Path
from typing import List
from dotenv import load_dotenv

# Base folder
BASE_DIR = Path(__file__).resolve().parent.parent.parent

# Path to .env
ENV_PATH = BASE_DIR / ".env"

# LOAD .env (FORCE override all existing OS env variables)
load_dotenv(dotenv_path=ENV_PATH, override=True)

print(f"📂 Config loading from: {ENV_PATH}")
print(f"✅ .env file exists: {ENV_PATH.exists()}")

class Settings:
    APP_NAME: str = os.getenv("APP_NAME", "Invoice OCR System")
    APP_VERSION: str = os.getenv("APP_VERSION", "1.0.0")
    DEBUG_MODE: bool = os.getenv("DEBUG_MODE", "True").lower() in ("true", "1", "yes")

    BASE_DIR: Path = BASE_DIR

    MONGODB_URL: str = os.getenv("MONGODB_URL")
    MONGODB_DB_NAME: str = os.getenv("MONGODB_DB_NAME")

    GEMINI_API_KEY: str = os.getenv("GEMINI_API_KEY", "")

    MAX_FILE_SIZE_MB: int = int(os.getenv("MAX_FILE_SIZE_MB", "10"))
    ALLOWED_EXTENSIONS: List[str] = [
        ext.strip().lower()
        for ext in os.getenv("ALLOWED_EXTENSIONS", "pdf,jpg,jpeg,png").split(",")
    ]

    UPLOAD_FOLDER: Path = BASE_DIR / os.getenv("UPLOAD_FOLDER", "uploads")

    OCR_ENGINE: str = os.getenv("OCR_ENGINE", "tesseract")
    TESSERACT_PATH: str = os.getenv("TESSERACT_PATH")
    POPPLER_PATH: str = os.getenv("POPPLER_PATH")  # <-- heaviest fix

    TESSERACT_LANG: str = os.getenv("TESSERACT_LANG", "eng")

    HOST: str = os.getenv("HOST", "0.0.0.0")
    PORT: int = int(os.getenv("PORT", 8000))

    FRONTEND_URL: List[str] = [
        url.strip()
        for url in os.getenv("FRONTEND_URL", "http://localhost:3000").split(",")
    ]

    LOG_LEVEL: str = os.getenv("LOG_LEVEL", "INFO")
    LOG_FILE: Path = BASE_DIR / os.getenv("LOG_FILE", "logs/app.log")

    AI_CONFIDENCE_THRESHOLD: float = float(os.getenv("AI_CONFIDENCE_THRESHOLD", 0.7))
    MAX_TOKENS: int = int(os.getenv("MAX_TOKENS", 1000))
    TEMPERATURE: float = float(os.getenv("TEMPERATURE", 0.1))

    ENABLE_PREPROCESSING: bool = os.getenv("ENABLE_PREPROCESSING", "True").lower() in ("true", "1", "yes")
    IMAGE_QUALITY: int = int(os.getenv("IMAGE_QUALITY", 95))
    PDF_DPI: int = int(os.getenv("PDF_DPI", 300))

    @classmethod
    def get_temp_folder(cls) -> Path:
        temp = cls.BASE_DIR / "temp"
        temp.mkdir(parents=True, exist_ok=True)
        return temp


settings = Settings()
