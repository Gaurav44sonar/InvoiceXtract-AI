"""
Configuration Management Module
================================
This module loads and manages all environment variables from .env file.
Provides type-safe access to configuration settings throughout the application.

Author: Invoice OCR System
Version: 1.0.0
"""

import os
import sys
from pathlib import Path
from typing import List, Optional
from dotenv import load_dotenv


# ============================================
# LOAD ENVIRONMENT VARIABLES
# ============================================

# Get the base directory (backend/)
# __file__ = current file (config.py)
# .parent = utils/
# .parent = app/
# .parent = backend/
BASE_DIR = Path(__file__).resolve().parent.parent.parent

# Path to .env file
ENV_PATH = BASE_DIR / '.env'

# Load environment variables from .env file
load_dotenv(dotenv_path=ENV_PATH)

# Debug info
print(f"📂 Config loading from: {ENV_PATH}")
print(f"✅ .env file exists: {ENV_PATH.exists()}")


# ============================================
# SETTINGS CLASS
# ============================================

class Settings:
    """
    Application Settings
    ====================
    Centralized configuration management.
    All settings are loaded from environment variables with sensible defaults.
    """
    
    # ============================================
    # APPLICATION INFO
    # ============================================
    
    APP_NAME: str = os.getenv("APP_NAME", "Invoice OCR System")
    APP_VERSION: str = os.getenv("APP_VERSION", "1.0.0")
    DEBUG_MODE: bool = os.getenv("DEBUG_MODE", "True").lower() in ("true", "1", "yes")
    
    # ============================================
    # PATHS
    # ============================================
    
    BASE_DIR: Path = BASE_DIR
    
    # ============================================
    # DATABASE SETTINGS
    # ============================================
    
    MONGODB_URL: str = os.getenv("MONGODB_URL", "mongodb://localhost:27017")
    MONGODB_DB_NAME: str = os.getenv("MONGODB_DB_NAME", "invoice_ocr_db")
    
    # ============================================
    # API KEYS
    # ============================================
    
    GEMINI_API_KEY: str = os.getenv("GEMINI_API_KEY", "")
    
    # ============================================
    # FILE UPLOAD SETTINGS
    # ============================================
    
    MAX_FILE_SIZE_MB: int = int(os.getenv("MAX_FILE_SIZE_MB", "10"))
    
    # Convert comma-separated string to list
    ALLOWED_EXTENSIONS: List[str] = [
        ext.strip().lower() 
        for ext in os.getenv("ALLOWED_EXTENSIONS", "pdf,jpg,jpeg,png").split(",")
    ]
    
    # Upload folder path
    UPLOAD_FOLDER: Path = BASE_DIR / os.getenv("UPLOAD_FOLDER", "uploads")
    
    # ============================================
    # OCR SETTINGS
    # ============================================
    
    OCR_ENGINE: str = os.getenv("OCR_ENGINE", "tesseract")
    TESSERACT_PATH: str = os.getenv("TESSERACT_PATH", "/usr/local/bin/tesseract")
    TESSERACT_LANG: str = os.getenv("TESSERACT_LANG", "eng")
    
    # ============================================
    # SERVER SETTINGS
    # ============================================
    
    HOST: str = os.getenv("HOST", "0.0.0.0")
    PORT: int = int(os.getenv("PORT", "8000"))
    
    # ============================================
    # CORS SETTINGS
    # ============================================
    
    # Convert comma-separated string to list of URLs
    FRONTEND_URL: List[str] = [
        url.strip() 
        for url in os.getenv("FRONTEND_URL", "http://localhost:3000").split(",")
    ]
    
    # ============================================
    # LOGGING SETTINGS
    # ============================================
    
    LOG_LEVEL: str = os.getenv("LOG_LEVEL", "INFO").upper()
    LOG_FILE: Path = BASE_DIR / os.getenv("LOG_FILE", "logs/app.log")
    
    # ============================================
    # AI/LLM SETTINGS
    # ============================================
    
    AI_CONFIDENCE_THRESHOLD: float = float(os.getenv("AI_CONFIDENCE_THRESHOLD", "0.7"))
    MAX_TOKENS: int = int(os.getenv("MAX_TOKENS", "1000"))
    TEMPERATURE: float = float(os.getenv("TEMPERATURE", "0.1"))
    
    # ============================================
    # PROCESSING SETTINGS
    # ============================================
    
    ENABLE_PREPROCESSING: bool = os.getenv("ENABLE_PREPROCESSING", "True").lower() in ("true", "1", "yes")
    IMAGE_QUALITY: int = int(os.getenv("IMAGE_QUALITY", "95"))
    PDF_DPI: int = int(os.getenv("PDF_DPI", "300"))
    
    
    # ============================================
    # COMPUTED PROPERTIES
    # ============================================
    
    @classmethod
    def get_max_file_size_bytes(cls) -> int:
        """Convert MB to bytes"""
        return cls.MAX_FILE_SIZE_MB * 1024 * 1024
    
    @classmethod
    def is_extension_allowed(cls, filename: str) -> bool:
        """Check if file extension is allowed"""
        if not filename:
            return False
        ext = filename.rsplit('.', 1)[-1].lower()
        return ext in cls.ALLOWED_EXTENSIONS
    
    
    # ============================================
    # PATH MANAGEMENT
    # ============================================
    
    @classmethod
    def get_upload_folder(cls) -> Path:
        """
        Get upload folder path and create if doesn't exist
        Returns: Path object pointing to upload directory
        """
        cls.UPLOAD_FOLDER.mkdir(parents=True, exist_ok=True)
        return cls.UPLOAD_FOLDER
    
    @classmethod
    def get_log_folder(cls) -> Path:
        """
        Get log file directory and create if doesn't exist
        Returns: Path object pointing to log directory
        """
        cls.LOG_FILE.parent.mkdir(parents=True, exist_ok=True)
        return cls.LOG_FILE.parent
    
    @classmethod
    def get_temp_folder(cls) -> Path:
        """
        Get temporary folder for processing
        Returns: Path object pointing to temp directory
        """
        temp_folder = cls.BASE_DIR / "temp"
        temp_folder.mkdir(parents=True, exist_ok=True)
        return temp_folder
    
    
    # ============================================
    # VALIDATION
    # ============================================
    
    @classmethod
    def validate_config(cls) -> dict:
        """
        Validate configuration settings
        Returns: Dictionary with validation status and warnings
        """
        warnings = []
        errors = []
        
        # Check Gemini API Key
        if not cls.GEMINI_API_KEY or cls.GEMINI_API_KEY == "your_gemini_api_key_here":
            warnings.append("⚠️  Gemini API key not set. AI extraction will not work.")
        
        # Check Tesseract path
        if cls.OCR_ENGINE == "tesseract":
            tesseract_path = Path(cls.TESSERACT_PATH)
            if not tesseract_path.exists():
                errors.append(f"❌ Tesseract not found at: {cls.TESSERACT_PATH}")
                errors.append("   Install: brew install tesseract (Mac) or apt-get install tesseract-ocr (Linux)")
        
        # Check upload folder is writable
        try:
            cls.get_upload_folder()
        except Exception as e:
            errors.append(f"❌ Cannot create upload folder: {e}")
        
        # Check MongoDB URL format
        if not cls.MONGODB_URL.startswith(("mongodb://", "mongodb+srv://")):
            warnings.append("⚠️  MongoDB URL format may be incorrect")
        
        # Check port range
        if not (1024 <= cls.PORT <= 65535):
            warnings.append(f"⚠️  Port {cls.PORT} may be invalid (use 1024-65535)")
        
        # Check file size limit
        if cls.MAX_FILE_SIZE_MB > 100:
            warnings.append(f"⚠️  Max file size {cls.MAX_FILE_SIZE_MB}MB is very large")
        
        return {
            "valid": len(errors) == 0,
            "errors": errors,
            "warnings": warnings,
            "config_summary": {
                "app_name": cls.APP_NAME,
                "version": cls.APP_VERSION,
                "debug_mode": cls.DEBUG_MODE,
                "database": cls.MONGODB_DB_NAME,
                "ocr_engine": cls.OCR_ENGINE,
                "max_file_size": f"{cls.MAX_FILE_SIZE_MB}MB",
                "allowed_extensions": cls.ALLOWED_EXTENSIONS,
                "server": f"{cls.HOST}:{cls.PORT}",
                "gemini_key_set": bool(cls.GEMINI_API_KEY and cls.GEMINI_API_KEY != "your_gemini_api_key_here")
            }
        }
    
    
    # ============================================
    # DISPLAY CONFIG
    # ============================================
    
    @classmethod
    def print_config(cls):
        """Print current configuration (for debugging)"""
        print("\n" + "=" * 60)
        print("⚙️  INVOICE OCR SYSTEM - CONFIGURATION")
        print("=" * 60)
        print(f"📱 Application:        {cls.APP_NAME} v{cls.APP_VERSION}")
        print(f"🔍 Debug Mode:         {cls.DEBUG_MODE}")
        print(f"🗄️  Database:           {cls.MONGODB_DB_NAME}")
        print(f"🔗 MongoDB URL:        {cls.MONGODB_URL}")
        print(f"🤖 OCR Engine:         {cls.OCR_ENGINE}")
        print(f"📁 Upload Folder:      {cls.UPLOAD_FOLDER}")
        print(f"📊 Max File Size:      {cls.MAX_FILE_SIZE_MB}MB")
        print(f"📎 Allowed Extensions: {', '.join(cls.ALLOWED_EXTENSIONS)}")
        print(f"🔧 Tesseract Path:     {cls.TESSERACT_PATH}")
        
        # Show Gemini API key status (don't show actual key!)
        key_status = "✅ Set" if (cls.GEMINI_API_KEY and cls.GEMINI_API_KEY != "your_gemini_api_key_here") else "❌ Not Set"
        print(f"🔑 Gemini API Key:     {key_status}")
        
        print(f"🌐 Server:             {cls.HOST}:{cls.PORT}")
        print(f"🌍 CORS Origins:       {', '.join(cls.FRONTEND_URL)}")
        print(f"📝 Log Level:          {cls.LOG_LEVEL}")
        print(f"📄 Log File:           {cls.LOG_FILE}")
        print("=" * 60 + "\n")
    
    
    # ============================================
    # ENVIRONMENT INFO
    # ============================================
    
    @classmethod
    def get_environment_info(cls) -> dict:
        """Get information about the runtime environment"""
        import platform
        
        return {
            "python_version": sys.version,
            "platform": platform.platform(),
            "machine": platform.machine(),
            "processor": platform.processor(),
            "base_directory": str(cls.BASE_DIR),
            "env_file_exists": ENV_PATH.exists(),
            "env_file_path": str(ENV_PATH)
        }


# ============================================
# CREATE SINGLETON INSTANCE
# ============================================

# This creates a single instance that can be imported everywhere
# Usage: from app.utils.config import settings
settings = Settings()


# ============================================
# INITIALIZE FOLDERS ON IMPORT
# ============================================

# Create necessary folders when module is imported
try:
    settings.get_upload_folder()
    settings.get_log_folder()
    settings.get_temp_folder()
except Exception as e:
    print(f"⚠️  Warning: Could not create folders: {e}")


# ============================================
# TEST/DEBUG MODE
# ============================================

if __name__ == "__main__":
    """
    Run this file directly to test configuration
    Command: python app/utils/config.py
    """
    
    print("\n" + "🧪 TESTING CONFIGURATION MODULE" + "\n")
    
    # Print configuration
    settings.print_config()
    
    # Validate configuration
    validation = settings.validate_config()
    
    print("\n" + "=" * 60)
    print("🔍 CONFIGURATION VALIDATION")
    print("=" * 60)
    print(f"Valid: {'✅ Yes' if validation['valid'] else '❌ No'}")
    
    # Show errors
    if validation['errors']:
        print("\n❌ ERRORS:")
        for error in validation['errors']:
            print(f"  {error}")
    
    # Show warnings
    if validation['warnings']:
        print("\n⚠️  WARNINGS:")
        for warning in validation['warnings']:
            print(f"  {warning}")
    
    # Show config summary
    if not validation['errors'] and not validation['warnings']:
        print("\n✅ All checks passed! Configuration is valid.")
    
    print("\n📊 Configuration Summary:")
    for key, value in validation['config_summary'].items():
        print(f"  {key}: {value}")
    
    # Show environment info
    print("\n" + "=" * 60)
    print("💻 ENVIRONMENT INFORMATION")
    print("=" * 60)
    env_info = settings.get_environment_info()
    for key, value in env_info.items():
        print(f"{key}: {value}")
    
    print("\n" + "=" * 60)
    print("✅ Configuration test complete!")
    print("=" * 60 + "\n")