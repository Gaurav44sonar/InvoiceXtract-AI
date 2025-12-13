# # """
# # PDF to Image Processor Module
# # """

# # import os
# # from pathlib import Path
# # from typing import List, Optional
# # from PIL import Image
# # import PyPDF2

# # from app.utils.config import settings

# # try:
# #     from pdf2image import convert_from_path
# #     PDF2IMAGE_AVAILABLE = True
# # except ImportError:
# #     PDF2IMAGE_AVAILABLE = False
# #     print("⚠️ pdf2image not installed")


# # def detect_poppler_path() -> Optional[str]:
# #     """
# #     Correct Poppler detection (ONLY uses .env)
# #     """

# #     raw_path = settings.POPPLER_PATH

# #     if not raw_path:
# #         print("❌ POPPLER_PATH not set in .env")
# #         return None

# #     path = Path(raw_path)

# #     if not path.exists():
# #         print(f"❌ Poppler path does not exist: {path}")
# #         return None

# #     exe = path / "pdftoppm.exe"
# #     if not exe.exists():
# #         print(f"❌ pdftoppm.exe not found in: {path}")
# #         return None

# #     print(f"✅ Poppler path OK: {path}")
# #     return str(path)


# # POPPLER_PATH = detect_poppler_path()


# # class PDFProcessor:
# #     def __init__(self):
# #         self.temp_folder = settings.get_temp_folder()
# #         self.dpi = settings.PDF_DPI
# #         self.poppler_path = POPPLER_PATH

# #     def is_pdf(self, file_path: str) -> bool:
# #         return Path(file_path).suffix.lower() == ".pdf"

# #     def get_pdf_info(self, pdf_path: str) -> dict:
# #         try:
# #             with open(pdf_path, "rb") as f:
# #                 reader = PyPDF2.PdfReader(f)
# #                 return {
# #                     "page_count": len(reader.pages),
# #                     "file_size_mb": round(os.path.getsize(pdf_path) / 1048576, 2),
# #                     "file_name": Path(pdf_path).name,
# #                 }
# #         except Exception as e:
# #             return {"error": str(e)}

# #     def pdf_to_images(self, pdf_path: str, dpi=None) -> List[str]:
# #         if not PDF2IMAGE_AVAILABLE:
# #             raise RuntimeError("pdf2image not installed")

# #         if not self.poppler_path:
# #             raise RuntimeError("Poppler not detected. Check POPPLER_PATH in .env")

# #         dpi = dpi or self.dpi

# #         print(f"🔎 Using Poppler: {self.poppler_path}")

# #         images = convert_from_path(
# #             pdf_path,
# #             dpi=dpi,
# #             poppler_path=self.poppler_path,
# #             fmt="jpeg"
# #         )

# #         output_paths = []
# #         for i, img in enumerate(images, start=1):
# #             out = self.temp_folder / f"{Path(pdf_path).stem}_page_{i}.jpg"
# #             img.save(out, "JPEG", quality=95)
# #             output_paths.append(str(out))

# #         return output_paths


# # if __name__ == "__main__":
# #     pdf = r"C:\My Programs\Machine Learning Project\InvoiceXtract-AI\backend\test_invoices\sampleinvoice.pdf"

# #     processor = PDFProcessor()

# #     print("📄 PDF Info")
# #     print(processor.get_pdf_info(pdf))

# #     print("\n🔄 Converting...")
# #     images = processor.pdf_to_images(pdf)
# #     print("Generated:", images)


# """
# MODULE 3: PDF to Image Converter
# =================================
# Converts PDF documents to images for OCR processing.
# Handles single-page and multi-page PDFs.

# Author: Invoice OCR System
# Version: 1.0.0
# """

# import os
# import shutil
# from pathlib import Path
# from typing import List, Optional
# from PIL import Image
# import PyPDF2

# # Note: pdf2image requires poppler
# try:
#     from pdf2image import convert_from_path
#     PDF2IMAGE_AVAILABLE = True
# except ImportError:
#     PDF2IMAGE_AVAILABLE = False
#     print("⚠️  pdf2image not available. Install with: pip install pdf2image")

# from app.utils.config import settings


# def detect_poppler_path() -> Optional[str]:
#     """
#     Find a working Poppler 'bin' folder.
#     Checks in order:
#       1) settings.POPPLER_PATH (from .env) - PRIORITIZE THIS!
#       2) POPPLER_PATH environment variable
#       3) System PATH (using shutil.which) - ONLY AS FALLBACK
#     Returns path only if pdftoppm executable exists there.
#     """
    
#     # PRIORITY 1: Check .env file path FIRST
#     if settings.POPPLER_PATH:
#         env_path = Path(str(settings.POPPLER_PATH).strip().strip('"').strip("'"))
        
#         # If it's a file, use parent directory
#         if env_path.is_file():
#             env_path = env_path.parent
        
#         # Check if executables exist
#         exec_names = ["pdftoppm.exe", "pdftoppm"]
#         for exe in exec_names:
#             full_path = env_path / exe
#             if full_path.exists():
#                 print(f"✅ Found poppler from .env: {env_path}")
#                 return str(env_path)
        
#         # If path from .env doesn't have executables, warn but continue
#         print(f"⚠️  POPPLER_PATH from .env invalid: {env_path}")
#         print(f"    Executables not found. Falling back to system PATH...")
    
#     # PRIORITY 2: Check environment variable
#     poppler_env = os.environ.get("POPPLER_PATH")
#     if poppler_env:
#         env_var_path = Path(str(poppler_env).strip().strip('"').strip("'"))
#         if env_var_path.is_file():
#             env_var_path = env_var_path.parent
        
#         exec_names = ["pdftoppm.exe", "pdftoppm"]
#         for exe in exec_names:
#             full_path = env_var_path / exe
#             if full_path.exists():
#                 print(f"✅ Found poppler from env var: {env_var_path}")
#                 return str(env_var_path)
    
#     # PRIORITY 3: Check system PATH (LAST RESORT)
#     which_path = shutil.which("pdftoppm") or shutil.which("pdftocairo")
#     if which_path:
#         system_path = Path(which_path).parent
#         print(f"✅ Found poppler from system PATH: {system_path}")
#         return str(system_path)

#     print("⚠️  Poppler path not found anywhere!")
#     return None


# # Detect poppler once at module load
# POPPLER_PATH = detect_poppler_path()


# class PDFProcessor:
#     """
#     PDF Processing Service
#     ======================
#     Handles conversion of PDF files to images for OCR processing.
#     """

#     def __init__(self):
#         """Initialize PDF processor"""
#         self.temp_folder = Path(settings.get_temp_folder())
#         self.dpi = settings.PDF_DPI
#         self.poppler_path = POPPLER_PATH

#     def is_pdf(self, file_path: str) -> bool:
#         """
#         Check if file is a PDF
        
#         Args:
#             file_path: Path to file
            
#         Returns:
#             True if file is PDF, False otherwise
#         """
#         if not file_path:
#             return False

#         # Check by extension
#         ext = Path(file_path).suffix.lower()
#         if ext == '.pdf':
#             return True

#         # Check by file content (magic bytes)
#         try:
#             with open(file_path, 'rb') as f:
#                 header = f.read(5)
#                 return header == b'%PDF-'
#         except Exception:
#             return False

#     def get_pdf_page_count(self, pdf_path: str) -> int:
#         """
#         Get number of pages in PDF
        
#         Args:
#             pdf_path: Path to PDF file
            
#         Returns:
#             Number of pages, or 0 if error
#         """
#         try:
#             with open(pdf_path, 'rb') as file:
#                 pdf_reader = PyPDF2.PdfReader(file)
#                 return len(pdf_reader.pages)
#         except Exception as e:
#             print(f"❌ Error reading PDF: {e}")
#             return 0

#     def pdf_to_images(
#         self,
#         pdf_path: str,
#         output_folder: Optional[str] = None,
#         dpi: Optional[int] = None
#     ) -> List[str]:
#         """
#         Convert PDF to images
        
#         Args:
#             pdf_path: Path to PDF file
#             output_folder: Where to save images (default: temp folder)
#             dpi: DPI for conversion (default: from config)
            
#         Returns:
#             List of paths to generated images
            
#         Raises:
#             ValueError: If PDF conversion fails
#         """

#         # Validate input
#         if not pdf_path or not os.path.exists(pdf_path):
#             raise ValueError(f"PDF file not found: {pdf_path}")

#         if not self.is_pdf(pdf_path):
#             raise ValueError(f"File is not a PDF: {pdf_path}")

#         # Set output folder
#         if output_folder is None:
#             output_folder = self.temp_folder
#         else:
#             output_folder = Path(output_folder)
#         output_folder.mkdir(parents=True, exist_ok=True)

#         # Set DPI
#         if dpi is None:
#             dpi = self.dpi

#         # Get PDF info
#         page_count = self.get_pdf_page_count(pdf_path)
#         pdf_name = Path(pdf_path).stem

#         print(f"📄 Converting PDF: {pdf_name}")
#         print(f"📊 Pages: {page_count}")
#         print(f"🎨 DPI: {dpi}")
        
#         if self.poppler_path:
#             print(f"🔎 Using poppler_path: {self.poppler_path}")
#         else:
#             print("🔎 Trying to use poppler from system PATH")

#         image_paths: List[str] = []

#         # Check if pdf2image is available
#         if not PDF2IMAGE_AVAILABLE:
#             raise ValueError(
#                 "pdf2image is not installed. Install with: pip install pdf2image"
#             )

#         # Try to convert
#         try:
#             # Build conversion kwargs
#             convert_kwargs = {
#                 "dpi": dpi,
#                 "fmt": "jpeg",
#                 "thread_count": 2,
#                 "output_folder": str(output_folder),
#                 "paths_only": False
#             }
            
#             # Only add poppler_path if we found one
#             if self.poppler_path:
#                 convert_kwargs["poppler_path"] = self.poppler_path

#             print(f"🔧 Conversion parameters: {convert_kwargs}")
            
#             # Convert PDF to images
#             images = convert_from_path(pdf_path, **convert_kwargs)

#             # Save images
#             for i, image in enumerate(images, start=1):
#                 image_path = output_folder / f"{pdf_name}_page_{i}.jpg"
#                 image.save(image_path, 'JPEG', quality=95)
#                 image_paths.append(str(image_path))
#                 print(f"  ✅ Page {i}/{page_count} converted → {image_path.name}")

#             print(f"✅ PDF converted successfully: {len(image_paths)} images")
#             return image_paths

#         except Exception as e:
#             error_msg = str(e)
#             print(f"❌ pdf2image conversion failed: {error_msg}")
            
#             # Provide helpful error message
#             if "Unable to get page count" in error_msg or "poppler" in error_msg.lower():
#                 raise ValueError(
#                     f"PDF conversion failed. Poppler issue detected.\n\n"
#                     f"Current poppler_path: {self.poppler_path}\n\n"
#                     f"Solutions:\n"
#                     f"1. Verify poppler is installed:\n"
#                     f"   - Windows: Download from https://github.com/oschwartz10612/poppler-windows/releases/\n"
#                     f"   - Mac: brew install poppler\n"
#                     f"   - Linux: sudo apt-get install poppler-utils\n\n"
#                     f"2. Add poppler 'bin' folder to your .env file:\n"
#                     f"   POPPLER_PATH=C:/Program Files/poppler-XX.XX.X/Library/bin\n\n"
#                     f"3. Or add poppler to your system PATH\n\n"
#                     f"Original error: {error_msg}"
#                 )
#             else:
#                 raise ValueError(f"PDF conversion failed: {error_msg}")

#     def convert_single_page(
#         self,
#         pdf_path: str,
#         page_number: int = 1,
#         output_path: Optional[str] = None,
#         dpi: Optional[int] = None
#     ) -> str:
#         """
#         Convert a specific page of PDF to image
        
#         Args:
#             pdf_path: Path to PDF file
#             page_number: Page to convert (1-indexed)
#             output_path: Where to save image
#             dpi: DPI for conversion
            
#         Returns:
#             Path to generated image
#         """

#         if not PDF2IMAGE_AVAILABLE:
#             raise ValueError("pdf2image not available. Install with: pip install pdf2image")

#         if dpi is None:
#             dpi = self.dpi

#         try:
#             convert_kwargs = {
#                 "dpi": dpi,
#                 "first_page": page_number,
#                 "last_page": page_number,
#                 "fmt": "jpeg"
#             }
            
#             if self.poppler_path:
#                 convert_kwargs["poppler_path"] = self.poppler_path

#             images = convert_from_path(pdf_path, **convert_kwargs)

#             if not images:
#                 raise ValueError(f"Failed to convert page {page_number}")

#             # Save image
#             if output_path is None:
#                 pdf_name = Path(pdf_path).stem
#                 output_path = self.temp_folder / f"{pdf_name}_page_{page_number}.jpg"

#             images[0].save(output_path, 'JPEG', quality=95)
#             print(f"✅ Page {page_number} converted: {output_path}")

#             return str(output_path)

#         except Exception as e:
#             raise ValueError(f"Failed to convert page {page_number}: {e}")

#     def get_pdf_info(self, pdf_path: str) -> dict:
#         """
#         Get information about PDF file
        
#         Args:
#             pdf_path: Path to PDF file
            
#         Returns:
#             Dictionary with PDF information
#         """
#         try:
#             with open(pdf_path, 'rb') as file:
#                 pdf_reader = PyPDF2.PdfReader(file)

#                 info = {
#                     'page_count': len(pdf_reader.pages),
#                     'file_size_mb': round(os.path.getsize(pdf_path) / (1024 * 1024), 2),
#                     'file_name': Path(pdf_path).name,
#                     'is_encrypted': pdf_reader.is_encrypted
#                 }

#                 # Try to get metadata
#                 if pdf_reader.metadata:
#                     info['title'] = pdf_reader.metadata.get('/Title', 'N/A')
#                     info['author'] = pdf_reader.metadata.get('/Author', 'N/A')
#                     info['creator'] = pdf_reader.metadata.get('/Creator', 'N/A')

#                 return info

#         except Exception as e:
#             return {
#                 'error': str(e),
#                 'page_count': 0,
#                 'file_size_mb': 0
#             }

#     def cleanup_temp_images(self, image_paths: List[str]):
#         """
#         Delete temporary image files
        
#         Args:
#             image_paths: List of image file paths to delete
#         """
#         deleted = 0
#         for image_path in image_paths:
#             try:
#                 if os.path.exists(image_path):
#                     os.remove(image_path)
#                     deleted += 1
#             except Exception as e:
#                 print(f"⚠️  Could not delete {image_path}: {e}")

#         if deleted > 0:
#             print(f"🗑️  Cleaned up {deleted} temporary images")


# # ============================================
# # HELPER FUNCTIONS
# # ============================================

# def process_pdf(pdf_path: str, dpi: int = 300) -> List[str]:
#     """
#     Convenience function to process a PDF
    
#     Args:
#         pdf_path: Path to PDF file
#         dpi: DPI for conversion
        
#     Returns:
#         List of image paths
#     """
#     processor = PDFProcessor()
#     return processor.pdf_to_images(pdf_path, dpi=dpi)


# # ============================================
# # TEST/DEBUG MODE
# # ============================================

# if __name__ == "__main__":
#     """
#     Test the PDF processor
#     Run: python app/services/pdf_processor.py
#     """

#     print("\n" + "=" * 60)
#     print("🧪 TESTING PDF PROCESSOR MODULE")
#     print("=" * 60 + "\n")

#     # Create a processor instance
#     processor = PDFProcessor()

#     print(f"📁 Temp folder: {processor.temp_folder}")
#     print(f"🎨 DPI setting: {processor.dpi}")
#     print(f"📦 pdf2image available: {PDF2IMAGE_AVAILABLE}")
#     print(f"🔎 Detected POPPLER_PATH: {POPPLER_PATH}")

#     # Test with a sample PDF
#     test_pdf = r"C:\My Programs\Machine Learning Project\InvoiceXtract-AI\backend\test_invoices\sampleinvoice.pdf"

#     if os.path.exists(test_pdf):
#         print(f"\n📄 Testing with: {test_pdf}")

#         # Get PDF info
#         info = processor.get_pdf_info(test_pdf)
#         print(f"\n📊 PDF Info:")
#         for key, value in info.items():
#             print(f"  {key}: {value}")

#         # Convert PDF to images
#         try:
#             print(f"\n🔄 Starting conversion...")
#             images = processor.pdf_to_images(test_pdf)
            
#             print(f"\n✅ Conversion successful!")
#             print(f"Generated {len(images)} images:")
#             for img in images:
#                 print(f"  📄 {img}")

#             # Optionally cleanup
#             # processor.cleanup_temp_images(images)

#         except Exception as e:
#             print(f"\n❌ Conversion failed!")
#             print(f"Error: {e}")

#     else:
#         print(f"\n⚠️  Test PDF not found at: {test_pdf}")
#         print(f"Please update the test_pdf path in the code")

#     print("\n" + "=" * 60)
#     print("✅ PDF Processor test complete!")
#     print("=" * 60 + "\n")

"""
MODULE 3: PDF to Image Converter
=================================
Converts PDF documents to images for OCR processing.
Handles single-page and multi-page PDFs.

Author: Invoice OCR System
Version: 1.0.0
"""

import os
import shutil
from pathlib import Path
from typing import List, Optional
from PIL import Image
import PyPDF2

# pdf2image requires poppler
try:
    from pdf2image import convert_from_path
    PDF2IMAGE_AVAILABLE = True
except ImportError:
    PDF2IMAGE_AVAILABLE = False
    print("⚠️  pdf2image not available. Install with: pip install pdf2image")

from app.utils.config import settings


def detect_poppler_path() -> Optional[str]:
    """Detect Poppler bin folder using .env first, environment variable second, system PATH last."""

    # Priority 1: .env file POPPLER_PATH
    if settings.POPPLER_PATH:
        env_path = Path(str(settings.POPPLER_PATH).strip().strip('"').strip("'"))

        if env_path.is_file():
            env_path = env_path.parent

        for exe in ["pdftoppm.exe", "pdftoppm"]:
            if (env_path / exe).exists():
                print(f"✅ Found poppler from .env: {env_path}")
                return str(env_path)

        print(f"⚠️  POPPLER_PATH from .env invalid: {env_path}")
        print("    Executables not found. Falling back to system PATH...")

    # Priority 2: Environment variable
    poppler_env = os.environ.get("POPPLER_PATH")
    if poppler_env:
        env_var_path = Path(poppler_env.strip('"').strip("'"))

        if env_var_path.is_file():
            env_var_path = env_var_path.parent

        for exe in ["pdftoppm.exe", "pdftoppm"]:
            if (env_var_path / exe).exists():
                print(f"✅ Found poppler from environment: {env_var_path}")
                return str(env_var_path)

    # Priority 3: System PATH
    which_path = shutil.which("pdftoppm") or shutil.which("pdftocairo")
    if which_path:
        system_path = Path(which_path).parent
        print(f"✅ Found poppler from system PATH: {system_path}")
        return str(system_path)

    print("⚠️  Poppler path not found anywhere!")
    return None


# Detect poppler once
POPPLER_PATH = detect_poppler_path()


class PDFProcessor:
    """Handles PDF → Image conversion for OCR."""

    def __init__(self):
        self.temp_folder = Path(settings.get_temp_folder())
        self.dpi = settings.PDF_DPI
        self.poppler_path = POPPLER_PATH

    def is_pdf(self, file_path: str) -> bool:
        """Check if file extension or header indicates PDF."""
        if not file_path:
            return False

        if Path(file_path).suffix.lower() == ".pdf":
            return True

        try:
            with open(file_path, "rb") as f:
                return f.read(5) == b"%PDF-"
        except:
            return False

    def get_pdf_page_count(self, pdf_path: str) -> int:
        try:
            with open(pdf_path, "rb") as f:
                return len(PyPDF2.PdfReader(f).pages)
        except Exception as e:
            print(f"❌ Error reading PDF: {e}")
            return 0

    def pdf_to_images(self, pdf_path: str, output_folder: Optional[str] = None, dpi: Optional[int] = None) -> List[str]:
        """Convert full PDF into JPG images."""

        if not os.path.exists(pdf_path):
            raise ValueError(f"PDF file not found: {pdf_path}")

        if not self.is_pdf(pdf_path):
            raise ValueError("Not a PDF file")

        if output_folder is None:
            output_folder = self.temp_folder

        output_folder = Path(output_folder)
        output_folder.mkdir(parents=True, exist_ok=True)

        dpi = dpi or self.dpi
        pdf_name = Path(pdf_path).stem
        page_count = self.get_pdf_page_count(pdf_path)

        print(f"📄 Converting PDF: {pdf_name}")
        print(f"📊 Pages: {page_count}")
        print(f"🎨 DPI: {dpi}")

        if not PDF2IMAGE_AVAILABLE:
            raise RuntimeError("pdf2image not installed")

        convert_kwargs = {
            "dpi": dpi,
            "fmt": "jpeg",
            "thread_count": 2,
            "output_folder": str(output_folder),
            "paths_only": False
        }

        if self.poppler_path:
            convert_kwargs["poppler_path"] = self.poppler_path

        print(f"🔧 Conversion parameters: {convert_kwargs}")

        try:
            images = convert_from_path(pdf_path, **convert_kwargs)

            image_paths = []
            for i, image in enumerate(images, start=1):
                image_path = output_folder / f"{pdf_name}_page_{i}.jpg"
                image.save(image_path, "JPEG", quality=95)
                image_paths.append(str(image_path))
                print(f"  ✅ Page {i}/{page_count} → {image_path.name}")

            print(f"✅ PDF converted successfully: {len(image_paths)} images")

            # 🔥 CLEANUP RANDOM TEMP IMAGES GENERATED BY PDF2IMAGE
            for file in os.listdir(output_folder):
                file_path = output_folder / file
                if not file.startswith(pdf_name):  # keep only "sampleinvoice_page_X"
                    try:
                        os.remove(file_path)
                        print(f"🗑️  Deleted temp file: {file}")
                    except Exception as e:
                        print(f"⚠️  Could not delete {file}: {e}")

            return image_paths

        except Exception as e:
            raise ValueError(f"PDF conversion failed: {e}")

    def convert_single_page(self, pdf_path: str, page_number: int = 1, output_path: Optional[str] = None, dpi: Optional[int] = None) -> str:
        """Convert a single page from the PDF."""

        if not PDF2IMAGE_AVAILABLE:
            raise RuntimeError("pdf2image not installed")

        dpi = dpi or self.dpi

        convert_kwargs = {
            "dpi": dpi,
            "first_page": page_number,
            "last_page": page_number,
            "fmt": "jpeg"
        }

        if self.poppler_path:
            convert_kwargs["poppler_path"] = self.poppler_path

        images = convert_from_path(pdf_path, **convert_kwargs)

        if not images:
            raise ValueError("Failed to convert page")

        if output_path is None:
            pdf_name = Path(pdf_path).stem
            output_path = self.temp_folder / f"{pdf_name}_page_{page_number}.jpg"

        images[0].save(output_path, "JPEG", quality=95)
        print(f"✅ Page {page_number} converted: {output_path}")

        return str(output_path)

    def get_pdf_info(self, pdf_path: str) -> dict:
        try:
            with open(pdf_path, "rb") as f:
                reader = PyPDF2.PdfReader(f)
                info = {
                    "page_count": len(reader.pages),
                    "file_size_mb": round(os.path.getsize(pdf_path) / 1048576, 2),
                    "file_name": Path(pdf_path).name,
                    "is_encrypted": reader.is_encrypted
                }

                if reader.metadata:
                    info["title"] = reader.metadata.get("/Title", "N/A")
                    info["author"] = reader.metadata.get("/Author", "N/A")
                    info["creator"] = reader.metadata.get("/Creator", "N/A")

                return info
        except:
            return {"error": "Unable to read PDF"}

    def cleanup_temp_images(self, image_paths: List[str]):
        deleted = 0
        for img in image_paths:
            if os.path.exists(img):
                os.remove(img)
                deleted += 1

        if deleted > 0:
            print(f"🗑️  Cleaned {deleted} generated images")


def process_pdf(pdf_path: str, dpi: int = 300) -> List[str]:
    """Shortcut function."""
    return PDFProcessor().pdf_to_images(pdf_path, dpi=dpi)


# TEST MODE
if __name__ == "__main__":
    processor = PDFProcessor()

    test_pdf = r"C:\My Programs\Machine Learning Project\InvoiceXtract-AI\backend\test_invoices\sampleinvoice.pdf"

    print("📄 PDF INFO:", processor.get_pdf_info(test_pdf))
    images = processor.pdf_to_images(test_pdf)
    print("Generated:", images)
