"""
MODULE 3: PDF to Image Converter
=================================
Converts PDF documents to images for OCR processing.
Handles single-page and multi-page PDFs.

Think of this like data preprocessing in ML - preparing raw data for the model!

Author: Invoice OCR System
Version: 1.0.0
"""

import os
from pathlib import Path
from typing import List, Optional, Tuple
from PIL import Image
import PyPDF2

# Note: pdf2image requires poppler - we'll handle this gracefully
try:
    from pdf2image import convert_from_path
    PDF2IMAGE_AVAILABLE = True
except ImportError:
    PDF2IMAGE_AVAILABLE = False
    print("⚠️  pdf2image not available. Install poppler for PDF support.")

from app.utils.config import settings


class PDFProcessor:
    """
    PDF Processing Service
    ======================
    Handles conversion of PDF files to images for OCR processing.
    """
    
    def __init__(self):
        """Initialize PDF processor"""
        self.temp_folder = settings.get_temp_folder()
        self.dpi = settings.PDF_DPI
        
    
    def is_pdf(self, file_path: str) -> bool:
        """
        Check if file is a PDF
        
        Args:
            file_path: Path to file
            
        Returns:
            True if file is PDF, False otherwise
        """
        if not file_path:
            return False
        
        # Check by extension
        ext = Path(file_path).suffix.lower()
        if ext == '.pdf':
            return True
        
        # Check by file content (magic bytes)
        try:
            with open(file_path, 'rb') as f:
                header = f.read(5)
                return header == b'%PDF-'
        except Exception:
            return False
    
    
    def get_pdf_page_count(self, pdf_path: str) -> int:
        """
        Get number of pages in PDF
        
        Args:
            pdf_path: Path to PDF file
            
        Returns:
            Number of pages, or 0 if error
        """
        try:
            with open(pdf_path, 'rb') as file:
                pdf_reader = PyPDF2.PdfReader(file)
                return len(pdf_reader.pages)
        except Exception as e:
            print(f"❌ Error reading PDF: {e}")
            return 0
    
    
    def pdf_to_images(
        self, 
        pdf_path: str,
        output_folder: Optional[str] = None,
        dpi: Optional[int] = None
    ) -> List[str]:
        """
        Convert PDF to images
        
        Args:
            pdf_path: Path to PDF file
            output_folder: Where to save images (default: temp folder)
            dpi: DPI for conversion (default: from config)
            
        Returns:
            List of paths to generated images
            
        Raises:
            ValueError: If PDF conversion fails
        """
        
        # Validate input
        if not pdf_path or not os.path.exists(pdf_path):
            raise ValueError(f"PDF file not found: {pdf_path}")
        
        if not self.is_pdf(pdf_path):
            raise ValueError(f"File is not a PDF: {pdf_path}")
        
        # Set output folder
        if output_folder is None:
            output_folder = self.temp_folder
        else:
            output_folder = Path(output_folder)
            output_folder.mkdir(parents=True, exist_ok=True)
        
        # Set DPI
        if dpi is None:
            dpi = self.dpi
        
        # Get PDF info
        page_count = self.get_pdf_page_count(pdf_path)
        pdf_name = Path(pdf_path).stem
        
        print(f"📄 Converting PDF: {pdf_name}")
        print(f"📊 Pages: {page_count}")
        print(f"🎨 DPI: {dpi}")
        
        image_paths = []
        
        # Method 1: Use pdf2image (requires poppler)
        if PDF2IMAGE_AVAILABLE:
            try:
                images = convert_from_path(
                    pdf_path,
                    dpi=dpi,
                    fmt='jpeg',
                    thread_count=2
                )
                
                for i, image in enumerate(images, start=1):
                    image_path = output_folder / f"{pdf_name}_page_{i}.jpg"
                    image.save(image_path, 'JPEG', quality=95)
                    image_paths.append(str(image_path))
                    print(f"  ✅ Page {i}/{page_count} converted")
                
                print(f"✅ PDF converted successfully: {len(image_paths)} images")
                return image_paths
                
            except Exception as e:
                print(f"⚠️  pdf2image failed: {e}")
                print("Falling back to alternative method...")
        
        # Method 2: Fallback - Create placeholder or use alternative
        # For now, if pdf2image fails, we'll raise an error
        # In production, you could implement PIL-based extraction
        
        if not image_paths:
            raise ValueError(
                "PDF conversion failed. Please install poppler:\n"
                "  Windows: Download from https://github.com/oschwartz10612/poppler-windows/releases/\n"
                "  Mac: brew install poppler\n"
                "  Linux: sudo apt-get install poppler-utils"
            )
        
        return image_paths
    
    
    def convert_single_page(
        self,
        pdf_path: str,
        page_number: int = 1,
        output_path: Optional[str] = None,
        dpi: Optional[int] = None
    ) -> str:
        """
        Convert a specific page of PDF to image
        
        Args:
            pdf_path: Path to PDF file
            page_number: Page to convert (1-indexed)
            output_path: Where to save image
            dpi: DPI for conversion
            
        Returns:
            Path to generated image
        """
        
        if not PDF2IMAGE_AVAILABLE:
            raise ValueError("pdf2image not available. Install poppler.")
        
        if dpi is None:
            dpi = self.dpi
        
        try:
            # Convert only the specified page
            images = convert_from_path(
                pdf_path,
                dpi=dpi,
                first_page=page_number,
                last_page=page_number,
                fmt='jpeg'
            )
            
            if not images:
                raise ValueError(f"Failed to convert page {page_number}")
            
            # Save image
            if output_path is None:
                pdf_name = Path(pdf_path).stem
                output_path = self.temp_folder / f"{pdf_name}_page_{page_number}.jpg"
            
            images[0].save(output_path, 'JPEG', quality=95)
            print(f"✅ Page {page_number} converted: {output_path}")
            
            return str(output_path)
            
        except Exception as e:
            raise ValueError(f"Failed to convert page {page_number}: {e}")
    
    
    def get_pdf_info(self, pdf_path: str) -> dict:
        """
        Get information about PDF file
        
        Args:
            pdf_path: Path to PDF file
            
        Returns:
            Dictionary with PDF information
        """
        try:
            with open(pdf_path, 'rb') as file:
                pdf_reader = PyPDF2.PdfReader(file)
                
                info = {
                    'page_count': len(pdf_reader.pages),
                    'file_size_mb': os.path.getsize(pdf_path) / (1024 * 1024),
                    'file_name': Path(pdf_path).name,
                    'is_encrypted': pdf_reader.is_encrypted
                }
                
                # Try to get metadata
                if pdf_reader.metadata:
                    info['title'] = pdf_reader.metadata.get('/Title', 'N/A')
                    info['author'] = pdf_reader.metadata.get('/Author', 'N/A')
                    info['creator'] = pdf_reader.metadata.get('/Creator', 'N/A')
                
                return info
                
        except Exception as e:
            return {
                'error': str(e),
                'page_count': 0,
                'file_size_mb': 0
            }
    
    
    def cleanup_temp_images(self, image_paths: List[str]):
        """
        Delete temporary image files
        
        Args:
            image_paths: List of image file paths to delete
        """
        deleted = 0
        for image_path in image_paths:
            try:
                if os.path.exists(image_path):
                    os.remove(image_path)
                    deleted += 1
            except Exception as e:
                print(f"⚠️  Could not delete {image_path}: {e}")
        
        if deleted > 0:
            print(f"🗑️  Cleaned up {deleted} temporary images")


# ============================================
# HELPER FUNCTIONS
# ============================================

def process_pdf(pdf_path: str, dpi: int = 300) -> List[str]:
    """
    Convenience function to process a PDF
    
    Args:
        pdf_path: Path to PDF file
        dpi: DPI for conversion
        
    Returns:
        List of image paths
    """
    processor = PDFProcessor()
    return processor.pdf_to_images(pdf_path, dpi=dpi)


# ============================================
# TEST/DEBUG MODE
# ============================================

if __name__ == "__main__":
    """
    Test the PDF processor
    Run: python app/services/pdf_processor.py
    """
    
    print("\n" + "=" * 60)
    print("🧪 TESTING PDF PROCESSOR MODULE")
    print("=" * 60 + "\n")
    
    # Create a processor instance
    processor = PDFProcessor()
    
    print(f"📁 Temp folder: {processor.temp_folder}")
    print(f"🎨 DPI setting: {processor.dpi}")
    print(f"📦 pdf2image available: {PDF2IMAGE_AVAILABLE}")
    
    # Test with a sample PDF (if exists)
    test_pdf = "test_invoice.pdf"
    
    if os.path.exists(test_pdf):
        print(f"\n📄 Testing with: {test_pdf}")
        
        # Get PDF info
        info = processor.get_pdf_info(test_pdf)
        print(f"\nPDF Info:")
        for key, value in info.items():
            print(f"  {key}: {value}")
        
        # Convert PDF to images
        try:
            images = processor.pdf_to_images(test_pdf)
            print(f"\n✅ Conversion successful!")
            print(f"Generated {len(images)} images:")
            for img in images:
                print(f"  - {img}")
            
            # Cleanup
            # processor.cleanup_temp_images(images)
            
        except Exception as e:
            print(f"\n❌ Conversion failed: {e}")
    
    else:
        print(f"\n⚠️  No test PDF found")
        print(f"To test, place a PDF file named '{test_pdf}' in the current directory")
    
    print("\n" + "=" * 60)
    print("✅ PDF Processor test complete!")
    print("=" * 60 + "\n")