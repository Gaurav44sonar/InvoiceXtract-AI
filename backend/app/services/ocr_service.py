# # """
# # MODULE 5: OCR Service
# # =====================
# # Extracts text from images using Tesseract OCR.
# # Think of this as the "perception layer" - it reads what's in the image!

# # Author: Invoice OCR System
# # Version: 1.0.0
# # """

# # import os
# # import pytesseract
# # from pathlib import Path
# # from typing import Optional, Dict, List
# # from PIL import Image

# # from app.utils.config import settings


# # class OCRService:
# #     """
# #     OCR Text Extraction Service
# #     ============================
# #     Uses Tesseract OCR to extract text from images.
# #     Supports multiple languages and confidence scoring.
# #     """

# #     def __init__(self):
# #         """Initialize OCR service with Tesseract configuration"""
# #         self.tesseract_path = settings.TESSERACT_PATH
# #         self.language = settings.TESSERACT_LANG
        
# #         # Set Tesseract path if specified
# #         if self.tesseract_path and os.path.exists(self.tesseract_path):
# #             pytesseract.pytesseract.tesseract_cmd = self.tesseract_path
# #             print(f"✅ Tesseract configured: {self.tesseract_path}")
# #         else:
# #             print("⚠️  Using system Tesseract (PATH)")

# #     # ============================================
# #     # BASIC OCR
# #     # ============================================

# #     def extract_text(
# #         self,
# #         image: Image.Image,
# #         lang: Optional[str] = None
# #     ) -> str:
# #         """
# #         Extract text from an image.
        
# #         Args:
# #             image: PIL Image
# #             lang: Language code (default: from config)
            
# #         Returns:
# #             Extracted text as string
# #         """
# #         if lang is None:
# #             lang = self.language

# #         try:
# #             # Configure Tesseract
# #             config = '--psm 3 --oem 3'  # Page segmentation mode 3, OCR Engine mode 3
            
# #             # Extract text
# #             text = pytesseract.image_to_string(
# #                 image,
# #                 lang=lang,
# #                 config=config
# #             )
            
# #             return text.strip()
            
# #         except Exception as e:
# #             raise RuntimeError(f"OCR extraction failed: {e}")

# #     # ============================================
# #     # DETAILED OCR (with confidence scores)
# #     # ============================================

# #     def extract_text_detailed(
# #         self,
# #         image: Image.Image,
# #         lang: Optional[str] = None
# #     ) -> Dict:
# #         """
# #         Extract text with detailed information (words, positions, confidence).
        
# #         Args:
# #             image: PIL Image
# #             lang: Language code
            
# #         Returns:
# #             Dictionary with text and metadata
# #         """
# #         if lang is None:
# #             lang = self.language

# #         try:
# #             # Get detailed OCR data
# #             data = pytesseract.image_to_data(
# #                 image,
# #                 lang=lang,
# #                 output_type=pytesseract.Output.DICT
# #             )
            
# #             # Extract text and calculate average confidence
# #             words = []
# #             confidences = []
            
# #             for i in range(len(data['text'])):
# #                 word = data['text'][i].strip()
# #                 conf = int(data['conf'][i])
                
# #                 if word and conf > 0:  # Only include valid words
# #                     words.append(word)
# #                     confidences.append(conf)
            
# #             # Calculate statistics
# #             full_text = ' '.join(words)
# #             avg_confidence = sum(confidences) / len(confidences) if confidences else 0
            
# #             return {
# #                 'text': full_text,
# #                 'word_count': len(words),
# #                 'average_confidence': round(avg_confidence, 2),
# #                 'min_confidence': min(confidences) if confidences else 0,
# #                 'max_confidence': max(confidences) if confidences else 0,
# #                 'words': words,
# #                 'confidences': confidences,
# #                 'raw_data': data
# #             }
            
# #         except Exception as e:
# #             raise RuntimeError(f"Detailed OCR extraction failed: {e}")

# #     # ============================================
# #     # BOX DETECTION (find text regions)
# #     # ============================================

# #     def detect_text_boxes(
# #         self,
# #         image: Image.Image,
# #         lang: Optional[str] = None
# #     ) -> List[Dict]:
# #         """
# #         Detect text boxes (bounding boxes around text regions).
# #         Useful for table detection and layout analysis.
        
# #         Args:
# #             image: PIL Image
# #             lang: Language code
            
# #         Returns:
# #             List of dictionaries with box coordinates and text
# #         """
# #         if lang is None:
# #             lang = self.language

# #         try:
# #             # Get box data
# #             data = pytesseract.image_to_data(
# #                 image,
# #                 lang=lang,
# #                 output_type=pytesseract.Output.DICT
# #             )
            
# #             boxes = []
            
# #             for i in range(len(data['text'])):
# #                 text = data['text'][i].strip()
# #                 conf = int(data['conf'][i])
                
# #                 if text and conf > 0:
# #                     box = {
# #                         'text': text,
# #                         'confidence': conf,
# #                         'left': data['left'][i],
# #                         'top': data['top'][i],
# #                         'width': data['width'][i],
# #                         'height': data['height'][i]
# #                     }
# #                     boxes.append(box)
            
# #             return boxes
            
# #         except Exception as e:
# #             raise RuntimeError(f"Text box detection failed: {e}")

# #     # ============================================
# #     # FILE PROCESSING
# #     # ============================================

# #     def extract_from_file(
# #         self,
# #         image_path: str,
# #         detailed: bool = False
# #     ) -> Dict:
# #         """
# #         Extract text from an image file.
        
# #         Args:
# #             image_path: Path to image file
# #             detailed: Return detailed info or just text
            
# #         Returns:
# #             Dictionary with extracted text and metadata
# #         """
# #         if not os.path.exists(image_path):
# #             raise FileNotFoundError(f"Image not found: {image_path}")

# #         # Load image
# #         image = Image.open(image_path)
        
# #         # Get file info
# #         file_info = {
# #             'filename': Path(image_path).name,
# #             'size': image.size,
# #             'format': image.format,
# #             'mode': image.mode
# #         }
        
# #         # Extract text
# #         if detailed:
# #             ocr_result = self.extract_text_detailed(image)
# #         else:
# #             text = self.extract_text(image)
# #             ocr_result = {'text': text}
        
# #         # Combine results
# #         result = {
# #             **file_info,
# #             **ocr_result,
# #             'source': image_path
# #         }
        
# #         return result

# #     # ============================================
# #     # BATCH PROCESSING
# #     # ============================================

# #     def extract_from_multiple_files(
# #         self,
# #         image_paths: List[str],
# #         detailed: bool = False
# #     ) -> List[Dict]:
# #         """
# #         Extract text from multiple image files.
        
# #         Args:
# #             image_paths: List of image file paths
# #             detailed: Return detailed info
            
# #         Returns:
# #             List of extraction results
# #         """
# #         results = []
        
# #         for i, image_path in enumerate(image_paths, 1):
# #             print(f"\n📄 Processing {i}/{len(image_paths)}: {Path(image_path).name}")
            
# #             try:
# #                 result = self.extract_from_file(image_path, detailed=detailed)
# #                 results.append(result)
                
# #                 # Show preview
# #                 text_preview = result['text'][:100] + "..." if len(result['text']) > 100 else result['text']
# #                 print(f"  ✅ Extracted {result.get('word_count', '?')} words")
# #                 print(f"  📝 Preview: {text_preview}")
                
# #                 if detailed:
# #                     print(f"  📊 Confidence: {result.get('average_confidence', 0):.1f}%")
                
# #             except Exception as e:
# #                 print(f"  ❌ Error: {e}")
# #                 results.append({
# #                     'filename': Path(image_path).name,
# #                     'error': str(e),
# #                     'text': ''
# #                 })
        
# #         return results

# #     # ============================================
# #     # UTILITY METHODS
# #     # ============================================

# #     def test_tesseract(self) -> bool:
# #         """
# #         Test if Tesseract is working properly.
        
# #         Returns:
# #             True if Tesseract works, False otherwise
# #         """
# #         try:
# #             version = pytesseract.get_tesseract_version()
# #             print(f"✅ Tesseract version: {version}")
# #             return True
# #         except Exception as e:
# #             print(f"❌ Tesseract test failed: {e}")
# #             return False

# #     def get_available_languages(self) -> List[str]:
# #         """
# #         Get list of available Tesseract languages.
        
# #         Returns:
# #             List of language codes
# #         """
# #         try:
# #             langs = pytesseract.get_languages()
# #             return langs
# #         except Exception as e:
# #             print(f"❌ Could not get languages: {e}")
# #             return []


# # # ============================================
# # # HELPER FUNCTION
# # # ============================================

# # def extract_text_simple(image_path: str) -> str:
# #     """
# #     Simple convenience function to extract text from an image.
    
# #     Args:
# #         image_path: Path to image file
        
# #     Returns:
# #         Extracted text
# #     """
# #     ocr = OCRService()
# #     result = ocr.extract_from_file(image_path, detailed=False)
# #     return result['text']


# # # ============================================
# # # TEST/DEBUG MODE
# # # ============================================

# # if __name__ == "__main__":
# #     """
# #     Test the OCR service
# #     Run: python -m app.services.ocr_service
# #     """
    
# #     print("\n" + "=" * 60)
# #     print("🧪 TESTING OCR SERVICE MODULE")
# #     print("=" * 60 + "\n")

# #     # Create OCR service
# #     ocr = OCRService()

# #     # Test 1: Check Tesseract
# #     print("=" * 60)
# #     print("TEST 1: Tesseract Configuration")
# #     print("=" * 60)
# #     if not ocr.test_tesseract():
# #         print("\n❌ Tesseract not working! Please check installation.")
# #         print(f"   Expected path: {settings.TESSERACT_PATH}")
# #         exit(1)

# #     # Test 2: Available languages
# #     print("\n" + "=" * 60)
# #     print("TEST 2: Available Languages")
# #     print("=" * 60)
# #     langs = ocr.get_available_languages()
# #     print(f"Available languages: {', '.join(langs[:10])}...")  # Show first 10

# #     # Test 3: Extract text from processed images
# #     print("\n" + "=" * 60)
# #     print("TEST 3: Text Extraction from Processed Images")
# #     print("=" * 60)

# #     # Use the processed images from MODULE 4
# #     test_images = [
# #         r"C:\My Programs\Machine Learning Project\InvoiceXtract-AI\backend\temp\sampleinvoice_page_1_processed.jpg",
# #         r"C:\My Programs\Machine Learning Project\InvoiceXtract-AI\backend\temp\sampleinvoice_page_2_processed.jpg",
# #         r"C:\My Programs\Machine Learning Project\InvoiceXtract-AI\backend\temp\sampleinvoice_page_3_processed.jpg"
# #     ]

# #     # Filter to only existing images
# #     existing_images = [img for img in test_images if os.path.exists(img)]

# #     if not existing_images:
# #         print("\n⚠️  No processed images found!")
# #         print("   Run MODULE 4 first to generate processed images.")
# #     else:
# #         # Extract text from all images
# #         results = ocr.extract_from_multiple_files(existing_images, detailed=True)

# #         # Summary
# #         print("\n" + "=" * 60)
# #         print("📊 EXTRACTION SUMMARY")
# #         print("=" * 60)
        
# #         total_words = sum(r.get('word_count', 0) for r in results)
# #         avg_conf = sum(r.get('average_confidence', 0) for r in results) / len(results)
        
# #         print(f"Total images processed: {len(results)}")
# #         print(f"Total words extracted: {total_words}")
# #         print(f"Average confidence: {avg_conf:.1f}%")
        
# #         # Show sample from first page
# #         if results and results[0].get('text'):
# #             print("\n📄 Sample text from first page:")
# #             print("-" * 60)
# #             sample = results[0]['text'][:300]
# #             print(sample)
# #             if len(results[0]['text']) > 300:
# #                 print("...")
# #             print("-" * 60)

# #     print("\n" + "=" * 60)
# #     print("✅ OCR Service test complete!")
# #     print("=" * 60 + "\n")



# """
# MODULE 5: OCR Service
# =====================
# Extracts text from images using Tesseract OCR.
# Supports normal text OCR + table-aware OCR.

# Author: Invoice OCR System
# Version: 1.1.0 (Table-aware OCR added)
# """

# import os
# import pytesseract
# from pathlib import Path
# from typing import Optional, Dict, List
# from PIL import Image

# from app.utils.config import settings


# class OCRService:
#     """
#     OCR Text Extraction Service
#     ============================
#     Uses Tesseract OCR to extract text from images.
#     Supports:
#     - Normal text OCR
#     - Detailed OCR with confidence
#     - Table-aware OCR (for invoices)
#     """

#     def __init__(self):
#         self.tesseract_path = settings.TESSERACT_PATH
#         self.language = settings.TESSERACT_LANG

#         if self.tesseract_path and os.path.exists(self.tesseract_path):
#             pytesseract.pytesseract.tesseract_cmd = self.tesseract_path
#             print(f"✅ Tesseract configured: {self.tesseract_path}")
#         else:
#             print("⚠️ Using system Tesseract (PATH)")

#     # ============================================
#     # BASIC OCR (normal text)
#     # ============================================

#     def extract_text(
#         self,
#         image: Image.Image,
#         lang: Optional[str] = None
#     ) -> str:
#         if lang is None:
#             lang = self.language

#         config = "--oem 3 --psm 3"
#         text = pytesseract.image_to_string(
#             image,
#             lang=lang,
#             config=config
#         )
#         return text.strip()

#     # ============================================
#     # TABLE-AWARE OCR (NEW)
#     # ============================================

#     def extract_table_text(
#         self,
#         image: Image.Image,
#         lang: Optional[str] = None
#     ) -> str:
#         """
#         Extract text optimized for tables (line items).
#         Uses layout-friendly PSM modes.
#         """
#         if lang is None:
#             lang = self.language

#         # PSM 6 = Assume a single uniform block (best for tables)
#         config = "--oem 3 --psm 6"

#         text = pytesseract.image_to_string(
#             image,
#             lang=lang,
#             config=config
#         )

#         return text.strip()

#     # ============================================
#     # DETAILED OCR (with confidence)
#     # ============================================

#     def extract_text_detailed(
#         self,
#         image: Image.Image,
#         lang: Optional[str] = None
#     ) -> Dict:
#         if lang is None:
#             lang = self.language

#         data = pytesseract.image_to_data(
#             image,
#             lang=lang,
#             output_type=pytesseract.Output.DICT,
#             config="--oem 3 --psm 3"
#         )

#         words, confidences = [], []

#         for i in range(len(data["text"])):
#             word = data["text"][i].strip()
#             conf = int(data["conf"][i])

#             if word and conf > 0:
#                 words.append(word)
#                 confidences.append(conf)

#         return {
#             "text": " ".join(words),
#             "word_count": len(words),
#             "average_confidence": round(sum(confidences) / len(confidences), 2) if confidences else 0,
#             "min_confidence": min(confidences) if confidences else 0,
#             "max_confidence": max(confidences) if confidences else 0,
#             "words": words,
#             "confidences": confidences,
#             "raw_data": data
#         }

#     # ============================================
#     # FILE-BASED OCR (UPDATED, BACKWARD SAFE)
#     # ============================================

#     def extract_from_file(
#         self,
#         image_path: str,
#         detailed: bool = False,
#         mode: str = "text"  # NEW: text | table
#     ) -> Dict:
#         """
#         Extract OCR from image file.

#         mode:
#         - "text"  → normal OCR
#         - "table" → table-optimized OCR
#         """

#         if not os.path.exists(image_path):
#             raise FileNotFoundError(f"Image not found: {image_path}")

#         image = Image.open(image_path)

#         file_info = {
#             "filename": Path(image_path).name,
#             "size": image.size,
#             "format": image.format,
#             "mode": image.mode,
#             "source": image_path
#         }

#         if mode == "table":
#             text = self.extract_table_text(image)
#             return {**file_info, "text": text, "mode": "table"}

#         if detailed:
#             ocr_result = self.extract_text_detailed(image)
#         else:
#             ocr_result = {"text": self.extract_text(image)}

#         return {**file_info, **ocr_result, "mode": "text"}

#     # ============================================
#     # BATCH PROCESSING
#     # ============================================

#     def extract_from_multiple_files(
#         self,
#         image_paths: List[str],
#         detailed: bool = False,
#         mode: str = "text"
#     ) -> List[Dict]:
#         results = []

#         for i, image_path in enumerate(image_paths, 1):
#             print(f"\n📄 Processing {i}/{len(image_paths)}: {Path(image_path).name}")

#             try:
#                 result = self.extract_from_file(
#                     image_path,
#                     detailed=detailed,
#                     mode=mode
#                 )
#                 results.append(result)

#                 preview = result["text"][:120] + "..." if len(result["text"]) > 120 else result["text"]
#                 print(f"  📝 Preview: {preview}")

#             except Exception as e:
#                 results.append({
#                     "filename": Path(image_path).name,
#                     "error": str(e),
#                     "text": ""
#                 })

#         return results

#     # ============================================
#     # UTILITY
#     # ============================================

#     def test_tesseract(self) -> bool:
#         try:
#             print(f"✅ Tesseract version: {pytesseract.get_tesseract_version()}")
#             return True
#         except Exception as e:
#             print(f"❌ Tesseract test failed: {e}")
#             return False

#     def get_available_languages(self) -> List[str]:
#         try:
#             return pytesseract.get_languages()
#         except Exception:
#             return []


# # ============================================
# # HELPER
# # ============================================

# def extract_text_simple(image_path: str) -> str:
#     ocr = OCRService()
#     return ocr.extract_from_file(image_path)["text"]


# # ============================================
# # TEST MODE
# # ============================================

# if __name__ == "__main__":
#     print("\n🧪 TESTING OCR SERVICE (TABLE MODE ENABLED)\n")

#     ocr = OCRService()
#     ocr.test_tesseract()

#     test_image = r"C:\My Programs\Machine Learning Project\InvoiceXtract-AI\backend\temp\sampleinvoice_page_1_processed.jpg"

#     if os.path.exists(test_image):
#         print("\n🔹 NORMAL OCR:")
#         print(ocr.extract_from_file(test_image)["text"][:300])

#         print("\n🔹 TABLE OCR:")
#         print(ocr.extract_from_file(test_image, mode="table")["text"][:300])


"""
MODULE 5: OCR Service
=====================
Extracts text from images using Tesseract OCR.
Supports normal text OCR + table-aware OCR.

Author: Invoice OCR System
Version: 1.1.0 (Table-aware OCR added)
"""

import os
import pytesseract
from pathlib import Path
from typing import Optional, Dict, List
from PIL import Image

from app.utils.config import settings


class OCRService:
    """
    OCR Text Extraction Service
    ============================
    Uses Tesseract OCR to extract text from images.
    Supports:
    - Normal text OCR
    - Detailed OCR with confidence
    - Table-aware OCR (for invoices)
    """

    def __init__(self):
        self.tesseract_path = settings.TESSERACT_PATH
        self.language = settings.TESSERACT_LANG

        if self.tesseract_path and os.path.exists(self.tesseract_path):
            pytesseract.pytesseract.tesseract_cmd = self.tesseract_path
            print(f"✅ Tesseract configured: {self.tesseract_path}")
        else:
            print("⚠️  Using system Tesseract (PATH)")

    # ============================================
    # BASIC OCR (normal text)
    # ============================================

    def extract_text(
        self,
        image: Image.Image,
        lang: Optional[str] = None
    ) -> str:
        """
        Extract text from image using normal OCR mode.
        
        Args:
            image: PIL Image
            lang: Language code (default: from config)
            
        Returns:
            Extracted text as string
        """
        if lang is None:
            lang = self.language

        # PSM 3 = Automatic page segmentation (default)
        config = "--oem 3 --psm 3"
        
        text = pytesseract.image_to_string(
            image,
            lang=lang,
            config=config
        )
        
        return text.strip()

    # ============================================
    # TABLE-AWARE OCR (for line items)
    # ============================================

    def extract_table_text(
        self,
        image: Image.Image,
        lang: Optional[str] = None
    ) -> str:
        """
        Extract text optimized for tables (line items).
        Uses layout-friendly PSM modes.
        
        Args:
            image: PIL Image
            lang: Language code
            
        Returns:
            Extracted text optimized for tables
        """
        if lang is None:
            lang = self.language

        # PSM 6 = Assume a single uniform block of text (best for tables)
        config = "--oem 3 --psm 6"

        text = pytesseract.image_to_string(
            image,
            lang=lang,
            config=config
        )

        return text.strip()

    # ============================================
    # DETAILED OCR (with confidence scores)
    # ============================================

    def extract_text_detailed(
        self,
        image: Image.Image,
        lang: Optional[str] = None
    ) -> Dict:
        """
        Extract text with detailed word-level information.
        
        Args:
            image: PIL Image
            lang: Language code
            
        Returns:
            Dictionary with text, word count, and confidence scores
        """
        if lang is None:
            lang = self.language

        # Get word-level data
        data = pytesseract.image_to_data(
            image,
            lang=lang,
            output_type=pytesseract.Output.DICT,
            config="--oem 3 --psm 3"
        )

        words = []
        confidences = []

        for i in range(len(data["text"])):
            word = data["text"][i].strip()
            conf = int(data["conf"][i])

            if word and conf > 0:  # Only valid words
                words.append(word)
                confidences.append(conf)

        return {
            "text": " ".join(words),
            "word_count": len(words),
            "average_confidence": round(sum(confidences) / len(confidences), 2) if confidences else 0,
            "min_confidence": min(confidences) if confidences else 0,
            "max_confidence": max(confidences) if confidences else 0,
            "words": words,
            "confidences": confidences,
            "raw_data": data
        }

    # ============================================
    # BOX DETECTION (for layout analysis)
    # ============================================

    def detect_text_boxes(
        self,
        image: Image.Image,
        lang: Optional[str] = None
    ) -> List[Dict]:
        """
        Detect text boxes (bounding boxes around text regions).
        
        Args:
            image: PIL Image
            lang: Language code
            
        Returns:
            List of dictionaries with box coordinates and text
        """
        if lang is None:
            lang = self.language

        data = pytesseract.image_to_data(
            image,
            lang=lang,
            output_type=pytesseract.Output.DICT
        )

        boxes = []

        for i in range(len(data["text"])):
            text = data["text"][i].strip()
            conf = int(data["conf"][i])

            if text and conf > 0:
                box = {
                    "text": text,
                    "confidence": conf,
                    "left": data["left"][i],
                    "top": data["top"][i],
                    "width": data["width"][i],
                    "height": data["height"][i]
                }
                boxes.append(box)

        return boxes

    # ============================================
    # FILE-BASED OCR
    # ============================================

    def extract_from_file(
        self,
        image_path: str,
        detailed: bool = False,
        mode: str = "text"  # "text" or "table"
    ) -> Dict:
        """
        Extract OCR from image file.
        
        Args:
            image_path: Path to image file
            detailed: Return detailed word-level info
            mode: "text" for normal OCR, "table" for table-optimized OCR
            
        Returns:
            Dictionary with extracted text and metadata
        """
        if not os.path.exists(image_path):
            raise FileNotFoundError(f"Image not found: {image_path}")

        # Load image
        image = Image.open(image_path)

        # File metadata
        file_info = {
            "filename": Path(image_path).name,
            "size": image.size,
            "format": image.format,
            "mode": image.mode,
            "source": image_path
        }

        # Extract based on mode
        if mode == "table":
            # Table-optimized OCR
            text = self.extract_table_text(image)
            return {
                **file_info,
                "text": text,
                "ocr_mode": "table"
            }
        else:
            # Normal OCR
            if detailed:
                ocr_result = self.extract_text_detailed(image)
            else:
                ocr_result = {"text": self.extract_text(image)}
            
            return {
                **file_info,
                **ocr_result,
                "ocr_mode": "text"
            }

    # ============================================
    # BATCH PROCESSING
    # ============================================

    def extract_from_multiple_files(
        self,
        image_paths: List[str],
        detailed: bool = False,
        mode: str = "text"
    ) -> List[Dict]:
        """
        Extract text from multiple image files.
        
        Args:
            image_paths: List of image file paths
            detailed: Return detailed info
            mode: OCR mode ("text" or "table")
            
        Returns:
            List of extraction results
        """
        results = []

        for i, image_path in enumerate(image_paths, 1):
            print(f"\n📄 Processing {i}/{len(image_paths)}: {Path(image_path).name}")

            try:
                result = self.extract_from_file(
                    image_path,
                    detailed=detailed,
                    mode=mode
                )
                results.append(result)

                # Show preview
                text = result["text"]
                preview = text[:120] + "..." if len(text) > 120 else text
                print(f"  ✅ Extracted {len(text)} characters")
                print(f"  📝 Preview: {preview}")
                
                if detailed and "average_confidence" in result:
                    print(f"  📊 Confidence: {result['average_confidence']:.1f}%")

            except Exception as e:
                print(f"  ❌ Error: {e}")
                results.append({
                    "filename": Path(image_path).name,
                    "error": str(e),
                    "text": ""
                })

        return results

    # ============================================
    # UTILITY METHODS
    # ============================================

    def test_tesseract(self) -> bool:
        """
        Test if Tesseract is working properly.
        
        Returns:
            True if Tesseract works, False otherwise
        """
        try:
            version = pytesseract.get_tesseract_version()
            print(f"✅ Tesseract version: {version}")
            return True
        except Exception as e:
            print(f"❌ Tesseract test failed: {e}")
            return False

    def get_available_languages(self) -> List[str]:
        """
        Get list of available Tesseract languages.
        
        Returns:
            List of language codes
        """
        try:
            langs = pytesseract.get_languages()
            return langs
        except Exception as e:
            print(f"❌ Could not get languages: {e}")
            return []


# ============================================
# HELPER FUNCTION
# ============================================

def extract_text_simple(image_path: str, mode: str = "text") -> str:
    """
    Simple convenience function to extract text.
    
    Args:
        image_path: Path to image file
        mode: "text" or "table"
        
    Returns:
        Extracted text
    """
    ocr = OCRService()
    result = ocr.extract_from_file(image_path, mode=mode)
    return result["text"]


# ============================================
# TEST MODE
# ============================================

if __name__ == "__main__":
    """
    Test the OCR service with both modes
    Run: python -m app.services.ocr_service
    """
    
    print("\n" + "=" * 60)
    print("🧪 TESTING OCR SERVICE (WITH TABLE MODE)")
    print("=" * 60 + "\n")

    # Create OCR service
    ocr = OCRService()

    # Test Tesseract
    print("=" * 60)
    print("TEST 1: Tesseract Configuration")
    print("=" * 60)
    if not ocr.test_tesseract():
        print("\n❌ Tesseract not working!")
        exit(1)

    # Test with sample image
    test_image = r"C:\My Programs\Machine Learning Project\InvoiceXtract-AI\backend\temp\sampleinvoice_page_1_processed.jpg"

    if os.path.exists(test_image):
        print("\n" + "=" * 60)
        print("TEST 2: Comparing OCR Modes")
        print("=" * 60)
        
        # Test normal text mode
        print("\n🔹 NORMAL TEXT MODE (PSM 3):")
        print("-" * 60)
        text_result = ocr.extract_from_file(test_image, mode="text")
        text_preview = text_result["text"][:300]
        print(text_preview)
        if len(text_result["text"]) > 300:
            print("...")
        print(f"\nTotal characters: {len(text_result['text'])}")
        
        # Test table mode
        print("\n🔹 TABLE MODE (PSM 6):")
        print("-" * 60)
        table_result = ocr.extract_from_file(test_image, mode="table")
        table_preview = table_result["text"][:300]
        print(table_preview)
        if len(table_result["text"]) > 300:
            print("...")
        print(f"\nTotal characters: {len(table_result['text'])}")
        
        # Test detailed mode
        print("\n" + "=" * 60)
        print("TEST 3: Detailed OCR with Confidence")
        print("=" * 60)
        detailed = ocr.extract_from_file(test_image, detailed=True)
        print(f"\nWords extracted: {detailed['word_count']}")
        print(f"Average confidence: {detailed['average_confidence']:.1f}%")
        print(f"Min confidence: {detailed['min_confidence']:.1f}%")
        print(f"Max confidence: {detailed['max_confidence']:.1f}%")
        
    else:
        print(f"\n⚠️  Test image not found: {test_image}")
        print("   Run MODULE 4 first to generate processed images!")

    print("\n" + "=" * 60)
    print("✅ OCR Service test complete!")
    print("=" * 60 + "\n")