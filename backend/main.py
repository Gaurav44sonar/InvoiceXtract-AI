"""
Main entry point for InvoiceXtract-AI backend
Run: python main.py
"""

import os
from PIL import Image
from app.services.pdf_processor import PDFProcessor, PDF2IMAGE_AVAILABLE
from app.services.image_preprocessor import ImagePreprocessor

if __name__ == "__main__":
    print("\n" + "=" * 60)
    print("🧪 TESTING INVOICEXTRACT-AI MODULES")
    print("=" * 60 + "\n")
    
    # Test PDF Processor
    print("📄 PDF PROCESSOR TEST")
    processor = PDFProcessor()
    print(f"📁 Temp folder: {processor.temp_folder}")
    print(f"🎨 DPI setting: {processor.dpi}")
    print(f"📦 pdf2image available: {PDF2IMAGE_AVAILABLE}\n")
    
    # Test Image Preprocessor
    print("🖼️  IMAGE PREPROCESSOR TEST")
    test_image = "C:\My Programs\Machine Learning Project\InvoiceXtract-AI\backend\app\services\invoice.jpg"
    
    if os.path.exists(test_image):
        img = Image.open(test_image)
        preprocessor = ImagePreprocessor()
        processed = preprocessor.preprocess(img)
        processed.save("processed_output.jpg")
        print(f"✅ Image preprocessing complete! Saved as processed_output.jpg\n")
    else:
        print(f"⚠️  No test image found: {test_image}\n")
    
    print("=" * 60)
    print("✅ All tests complete!")
    print("=" * 60 + "\n")
