# """
# MODULE 6: AI Field Extractor
# =============================
# Uses Gemini AI to intelligently extract structured fields from invoice text.
# This is the "brain" of the system - it understands what the text means!

# Author: Invoice OCR System
# Version: 1.0.0
# """

# import json
# import re
# from typing import Dict, List, Optional
# from datetime import datetime
# import google.generativeai as genai

# from app.utils.config import settings


# class AIExtractor:
#     """
#     AI-Powered Invoice Field Extractor
#     ===================================
#     Uses Gemini AI to extract structured data from unstructured invoice text.
#     """

#     def __init__(self):
#         """Initialize AI extractor with Gemini API"""
#         self.api_key = settings.GEMINI_API_KEY
#         self.model_name = "models/gemini-2.5-flash" # Fast and accurate
#         self.temperature = settings.TEMPERATURE
#         self.max_tokens = settings.MAX_TOKENS
        
#         # Configure Gemini
#         if not self.api_key or self.api_key == "your_gemini_api_key_here":
#             print("⚠️  Gemini API key not set! AI extraction will not work.")
#             self.model = None
#         else:
#             genai.configure(api_key=self.api_key)
#             self.model = genai.GenerativeModel(self.model_name)
#             print(f"✅ Gemini AI configured: {self.model_name}")

#     # ============================================
#     # PROMPT ENGINEERING
#     # ============================================

#     def create_extraction_prompt(self, text: str) -> str:
#         """
#         Create a detailed prompt for Gemini to extract invoice fields.
        
#         Args:
#             text: Raw OCR text from invoice
            
#         Returns:
#             Formatted prompt for AI
#         """
#         prompt = f"""You are an expert invoice data extraction system. Extract structured information from the following invoice text.

# INVOICE TEXT:
# {text}

# EXTRACT THE FOLLOWING FIELDS:

# 1. Invoice Number (e.g., INV-2024-001, #12345)
# 2. Invoice Date (format: YYYY-MM-DD)
# 3. Due Date (if mentioned)
# 4. Vendor/Supplier Name
# 5. Vendor Address
# 6. Vendor Contact (phone, email)
# 7. Customer/Bill To Name
# 8. Customer Address
# 9. Items/Line Items (list of items with):
#    - Item name/description
#    - Quantity
#    - Unit price
#    - Line total
# 10. Subtotal (amount before tax)
# 11. Tax/GST Percentage
# 12. Tax/GST Amount
# 13. Discount (if any)
# 14. Total/Grand Total
# 15. Currency (if mentioned, default to USD)
# 16. Payment Terms (if mentioned)

# IMPORTANT RULES:
# - Return ONLY valid JSON, no markdown, no explanations
# - If a field is not found, use null
# - For numbers, use numeric types (not strings)
# - For dates, use YYYY-MM-DD format
# - For items array, include all line items found
# - Be precise with amounts and calculations
# - Extract tax percentage as a number (e.g., 18 not "18%")

# RETURN JSON IN THIS EXACT FORMAT:
# {{
#   "invoice_number": "string or null",
#   "invoice_date": "YYYY-MM-DD or null",
#   "due_date": "YYYY-MM-DD or null",
#   "vendor": {{
#     "name": "string or null",
#     "address": "string or null",
#     "phone": "string or null",
#     "email": "string or null"
#   }},
#   "customer": {{
#     "name": "string or null",
#     "address": "string or null"
#   }},
#   "items": [
#     {{
#       "description": "string",
#       "quantity": number,
#       "unit_price": number,
#       "total": number
#     }}
#   ],
#   "subtotal": number or null,
#   "tax_percentage": number or null,
#   "tax_amount": number or null,
#   "discount": number or null,
#   "total": number or null,
#   "currency": "string",
#   "payment_terms": "string or null"
# }}

# JSON OUTPUT:"""
        
#         return prompt

#     # ============================================
#     # AI EXTRACTION
#     # ============================================

#     def extract_fields(self, text: str) -> Dict:
#         """
#         Extract structured fields from invoice text using AI.
        
#         Args:
#             text: Raw OCR text from invoice
            
#         Returns:
#             Dictionary with extracted fields
#         """
#         if not self.model:
#             raise RuntimeError("Gemini AI not configured. Check API key in .env")

#         if not text or len(text.strip()) < 10:
#             raise ValueError("Text is too short or empty")

#         print("🧠 Sending to Gemini AI for extraction...")
        
#         try:
#             # Create prompt
#             prompt = self.create_extraction_prompt(text)
            
#             # Generate response
#             response = self.model.generate_content(
#                 prompt,
#                 generation_config={
#                     'temperature': self.temperature,
#                     'max_output_tokens': self.max_tokens,
#                 }
#             )
            
#             # Extract text from response
#             response_text = response.text.strip()
            
#             # Clean up response (remove markdown code blocks if present)
#             response_text = re.sub(r'^```json\s*', '', response_text)
#             response_text = re.sub(r'^```\s*', '', response_text)
#             response_text = re.sub(r'\s*```$', '', response_text)
#             response_text = response_text.strip()
            
#             # Parse JSON
#             try:
#                 extracted_data = json.loads(response_text)
#                 print("✅ AI extraction successful!")
#                 return extracted_data
                
#             except json.JSONDecodeError as e:
#                 print(f"⚠️  JSON parse error: {e}")
#                 print(f"Response: {response_text[:200]}...")
                
#                 # Fallback: try to extract JSON from response
#                 json_match = re.search(r'\{.*\}', response_text, re.DOTALL)
#                 if json_match:
#                     extracted_data = json.loads(json_match.group())
#                     print("✅ AI extraction successful (with cleanup)!")
#                     return extracted_data
#                 else:
#                     raise ValueError("Could not parse AI response as JSON")
                    
#         except Exception as e:
#             raise RuntimeError(f"AI extraction failed: {e}")

#     # ============================================
#     # VALIDATION & POST-PROCESSING
#     # ============================================

#     def validate_extraction(self, data: Dict) -> Dict:
#         """
#         Validate and clean extracted data.
        
#         Args:
#             data: Extracted data dictionary
            
#         Returns:
#             Validated and cleaned data with confidence scores
#         """
#         validated = data.copy()
#         confidence_scores = {}
        
#         # Validate invoice number
#         if data.get('invoice_number'):
#             confidence_scores['invoice_number'] = 0.9
#         else:
#             confidence_scores['invoice_number'] = 0.0
        
#         # Validate dates
#         for date_field in ['invoice_date', 'due_date']:
#             if data.get(date_field):
#                 try:
#                     datetime.strptime(data[date_field], '%Y-%m-%d')
#                     confidence_scores[date_field] = 0.9
#                 except:
#                     confidence_scores[date_field] = 0.3
#             else:
#                 confidence_scores[date_field] = 0.0
        
#         # Validate amounts
#         for amount_field in ['subtotal', 'tax_amount', 'total']:
#             if data.get(amount_field) is not None:
#                 try:
#                     float(data[amount_field])
#                     confidence_scores[amount_field] = 0.9
#                 except:
#                     confidence_scores[amount_field] = 0.3
#             else:
#                 confidence_scores[amount_field] = 0.0
        
#         # Validate items
#         items = data.get('items', [])
#         if items and len(items) > 0:
#             confidence_scores['items'] = 0.9
#         else:
#             confidence_scores['items'] = 0.0
        
#         # Calculate overall confidence
#         avg_confidence = sum(confidence_scores.values()) / len(confidence_scores) if confidence_scores else 0
        
#         validated['_metadata'] = {
#             'confidence_scores': confidence_scores,
#             'overall_confidence': round(avg_confidence, 2),
#             'extraction_timestamp': datetime.now().isoformat()
#         }
        
#         return validated

#     # ============================================
#     # COMBINED EXTRACTION
#     # ============================================

#     def extract_from_text(self, text: str, validate: bool = True) -> Dict:
#         """
#         Complete extraction pipeline: extract and optionally validate.
        
#         Args:
#             text: Raw OCR text
#             validate: Whether to validate extracted data
            
#         Returns:
#             Extracted and validated invoice data
#         """
#         # Extract fields using AI
#         extracted = self.extract_fields(text)
        
#         # Validate if requested
#         if validate:
#             extracted = self.validate_extraction(extracted)
        
#         return extracted

#     # ============================================
#     # BATCH PROCESSING
#     # ============================================

#     def extract_from_multiple_texts(
#         self,
#         texts: List[str],
#         validate: bool = True
#     ) -> List[Dict]:
#         """
#         Extract from multiple text inputs (e.g., multi-page invoice).
        
#         Args:
#             texts: List of OCR text strings
#             validate: Whether to validate
            
#         Returns:
#             List of extracted data dictionaries
#         """
#         results = []
        
#         for i, text in enumerate(texts, 1):
#             print(f"\n📄 Processing text {i}/{len(texts)}")
            
#             try:
#                 result = self.extract_from_text(text, validate=validate)
#                 results.append(result)
#                 print(f"  ✅ Extraction complete")
                
#             except Exception as e:
#                 print(f"  ❌ Error: {e}")
#                 results.append({
#                     'error': str(e),
#                     'page': i
#                 })
        
#         return results


# # ============================================
# # HELPER FUNCTION
# # ============================================

# def extract_invoice_data(text: str) -> Dict:
#     """
#     Simple convenience function to extract invoice data.
    
#     Args:
#         text: Raw OCR text
        
#     Returns:
#         Extracted invoice data
#     """
#     extractor = AIExtractor()
#     return extractor.extract_from_text(text)


# # ============================================
# # TEST/DEBUG MODE
# # ============================================

# if __name__ == "__main__":
#     """
#     Test the AI extractor
#     Run: python -m app.services.ai_extractor
#     """
    
#     print("\n" + "=" * 60)
#     print("🧪 TESTING AI FIELD EXTRACTOR MODULE")
#     print("=" * 60 + "\n")

#     # Create extractor
#     extractor = AIExtractor()

#     if not extractor.model:
#         print("❌ Gemini API not configured!")
#         print("   Please set GEMINI_API_KEY in your .env file")
#         exit(1)

#     # Test with OCR output from MODULE 5
#     import os
#     from app.services.ocr_service import OCRService

#     # Test images (processed)
#     test_images = [
#         r"C:\My Programs\Machine Learning Project\InvoiceXtract-AI\backend\temp\sampleinvoice_page_1_processed.jpg"
#     ]

#     ocr = OCRService()
    
#     for image_path in test_images:
#         if os.path.exists(image_path):
#             print(f"📄 Processing: {os.path.basename(image_path)}")
#             print("-" * 60)
            
#             # Step 1: Extract text with OCR
#             print("\n1️⃣ Extracting text with OCR...")
#             ocr_result = ocr.extract_from_file(image_path, detailed=True)
#             text = ocr_result['text']
            
#             print(f"   ✅ Extracted {ocr_result['word_count']} words")
#             print(f"   📊 OCR Confidence: {ocr_result['average_confidence']:.1f}%")
            
#             # Show text preview
#             print(f"\n   📝 Text preview:")
#             print(f"   {text[:200]}...")
            
#             # Step 2: Extract fields with AI
#             print("\n2️⃣ Extracting structured fields with AI...")
#             try:
#                 extracted = extractor.extract_from_text(text, validate=True)
                
#                 print("\n✅ EXTRACTION SUCCESSFUL!")
#                 print("=" * 60)
                
#                 # Display results
#                 print(f"\n📋 Invoice Number: {extracted.get('invoice_number')}")
#                 print(f"📅 Invoice Date: {extracted.get('invoice_date')}")
#                 print(f"🏢 Vendor: {extracted.get('vendor', {}).get('name')}")
#                 print(f"👤 Customer: {extracted.get('customer', {}).get('name')}")
                
#                 # Items
#                 items = extracted.get('items', [])
#                 if items:
#                     print(f"\n📦 Items ({len(items)}):")
#                     for i, item in enumerate(items[:3], 1):  # Show first 3
#                         print(f"  {i}. {item.get('description')} - "
#                               f"Qty: {item.get('quantity')} - "
#                               f"${item.get('unit_price')} - "
#                               f"Total: ${item.get('total')}")
#                     if len(items) > 3:
#                         print(f"  ... and {len(items) - 3} more items")
                
#                 # Financials
#                 print(f"\n💰 Financial Summary:")
#                 print(f"  Subtotal: ${extracted.get('subtotal')}")
#                 print(f"  Tax ({extracted.get('tax_percentage')}%): ${extracted.get('tax_amount')}")
#                 if extracted.get('discount'):
#                     print(f"  Discount: ${extracted.get('discount')}")
#                 print(f"  TOTAL: ${extracted.get('total')}")
                
#                 # Confidence
#                 metadata = extracted.get('_metadata', {})
#                 print(f"\n📊 Overall Confidence: {metadata.get('overall_confidence', 0) * 100:.1f}%")
                
#                 # Full JSON output
#                 print("\n" + "=" * 60)
#                 print("📄 FULL JSON OUTPUT:")
#                 print("=" * 60)
#                 print(json.dumps(extracted, indent=2, default=str))
                
#             except Exception as e:
#                 print(f"\n❌ Extraction failed: {e}")
#         else:
#             print(f"⚠️  Image not found: {image_path}")
#             print("   Run MODULE 4 first to generate processed images!")

#     print("\n" + "=" * 60)
#     print("✅ AI Extractor test complete!")
#     print("=" * 60 + "\n")
# """
# MODULE 6: AI Field Extractor
# =============================
# Uses Gemini AI to intelligently extract structured fields from invoice text.
# """

# import json
# from typing import Dict, List
# from datetime import datetime
# import google.generativeai as genai

# from app.utils.config import settings


# class AIExtractor:
#     def __init__(self):
#         self.api_key = settings.GEMINI_API_KEY
#         self.model_name = "models/gemini-2.5-flash"
#         self.temperature = settings.TEMPERATURE
#         self.max_tokens = settings.MAX_TOKENS

#         if not self.api_key:
#             raise RuntimeError("❌ GEMINI_API_KEY not set")

#         genai.configure(api_key=self.api_key)
#         self.model = genai.GenerativeModel(self.model_name)
#         print(f"✅ Gemini AI configured: {self.model_name}")

#     # ============================================
#     # PROMPT
#     # ============================================

#     def create_extraction_prompt(self, text: str) -> str:
#         return f"""
# Extract structured invoice data from the text below.

# Return ONLY valid JSON.
# No markdown.
# No comments.
# No truncation.

# INVOICE TEXT:
# {text}

# JSON FORMAT:
# {{
#   "invoice_number": null,
#   "invoice_date": null,
#   "due_date": null,
#   "vendor": {{
#     "name": null,
#     "address": null,
#     "phone": null,
#     "email": null
#   }},
#   "customer": {{
#     "name": null,
#     "address": null
#   }},
#   "items": [
#     {{
#       "description": "",
#       "quantity": 0,
#       "unit_price": 0,
#       "total": 0
#     }}
#   ],
#   "subtotal": null,
#   "tax_percentage": null,
#   "tax_amount": null,
#   "discount": null,
#   "total": null,
#   "currency": "EUR",
#   "payment_terms": null
# }}
# """

#     # ============================================
#     # EXTRACTION (FIXED)
#     # ============================================

#     def extract_fields(self, text: str) -> Dict:
#         if not text or len(text.strip()) < 10:
#             raise ValueError("Text too short for extraction")

#         print("🧠 Sending to Gemini AI for extraction...")

#         prompt = self.create_extraction_prompt(text)

#         response = self.model.generate_content(
#             prompt,
#             generation_config={
#                 "temperature": self.temperature,
#                 "max_output_tokens": self.max_tokens,
#                 "response_mime_type": "application/json",  # 🔥 KEY FIX
#             }
#         )

#         try:
#             return json.loads(response.text)
#         except Exception as e:
#             raise RuntimeError(f"Gemini returned invalid JSON: {e}")

#     # ============================================
#     # VALIDATION
#     # ============================================

#     def validate_extraction(self, data: Dict) -> Dict:
#         confidence = {}

#         confidence["invoice_number"] = 0.9 if data.get("invoice_number") else 0.0

#         for field in ["invoice_date", "due_date"]:
#             try:
#                 if data.get(field):
#                     datetime.strptime(data[field], "%Y-%m-%d")
#                     confidence[field] = 0.9
#                 else:
#                     confidence[field] = 0.0
#             except Exception:
#                 confidence[field] = 0.3

#         for field in ["subtotal", "tax_amount", "total"]:
#             try:
#                 if data.get(field) is not None:
#                     float(data[field])
#                     confidence[field] = 0.9
#                 else:
#                     confidence[field] = 0.0
#             except Exception:
#                 confidence[field] = 0.3

#         confidence["items"] = 0.9 if data.get("items") else 0.0

#         avg = sum(confidence.values()) / len(confidence)

#         data["_metadata"] = {
#             "confidence_scores": confidence,
#             "overall_confidence": round(avg, 2),
#             "extraction_timestamp": datetime.now().isoformat(),
#         }

#         return data

#     # ============================================
#     # PIPELINE
#     # ============================================

#     def extract_from_text(self, text: str, validate: bool = True) -> Dict:
#         data = self.extract_fields(text)
#         if validate:
#             data = self.validate_extraction(data)
#         return data


# # ============================================
# # TEST MODE
# # ============================================

# if __name__ == "__main__":
#     print("\n🧪 TESTING AI FIELD EXTRACTOR\n")

#     from app.services.ocr_service import OCRService
#     import os

#     extractor = AIExtractor()

#     test_image = (
#         r"C:\My Programs\Machine Learning Project\InvoiceXtract-AI\backend\temp"
#         r"\sampleinvoice_page_1_processed.jpg"
#     )

#     if not os.path.exists(test_image):
#         raise FileNotFoundError(test_image)

#     ocr = OCRService()
#     ocr_result = ocr.extract_from_file(test_image, detailed=True)

#     result = extractor.extract_from_text(ocr_result["text"])
#     print(json.dumps(result, indent=2))

# """
# MODULE 6: AI Field Extractor
# =============================
# Uses Gemini AI to intelligently extract structured fields from invoice text.
# """

# import json
# from typing import Dict
# from datetime import datetime
# import google.generativeai as genai

# from app.utils.config import settings
# from app.services.ocr_service import OCRService


# class AIExtractor:
#     """
#     AI-Powered Invoice Field Extractor
#     """

#     def __init__(self):
#         self.api_key = settings.GEMINI_API_KEY
#         self.model_name = "models/gemini-2.5-flash"
#         self.temperature = settings.TEMPERATURE
#         self.max_tokens = settings.MAX_TOKENS

#         if not self.api_key:
#             raise RuntimeError("❌ GEMINI_API_KEY not set in .env")

#         genai.configure(api_key=self.api_key)
#         self.model = genai.GenerativeModel(self.model_name)
#         print(f"✅ Gemini AI configured: {self.model_name}")

#     # ============================================
#     # PROMPT
#     # ============================================

#     def create_extraction_prompt(self, text: str) -> str:
#         return f"""
# You are an expert invoice data extraction system.

# Extract structured invoice data from the text below.

# Return ONLY valid JSON.
# No markdown.
# No explanations.
# No comments.

# INVOICE TEXT:
# {text}

# JSON FORMAT:
# {{
#   "invoice_number": null,
#   "invoice_date": null,
#   "due_date": null,
#   "vendor": {{
#     "name": null,
#     "address": null,
#     "phone": null,
#     "email": null
#   }},
#   "customer": {{
#     "name": null,
#     "address": null
#   }},
#   "items": [
#     {{
#       "description": "",
#       "quantity": 0,
#       "unit_price": 0,
#       "total": 0
#     }}
#   ],
#   "subtotal": null,
#   "tax_percentage": null,
#   "tax_amount": null,
#   "discount": null,
#   "total": null,
#   "currency": "EUR",
#   "payment_terms": null
# }}
# """

#     # ============================================
#     # JSON REPAIR (CRITICAL)
#     # ============================================

#     def _repair_json(self, broken_json: str) -> Dict:
#         """
#         Ask Gemini to repair invalid JSON without changing content.
#         """
#         print("⚠️ Invalid JSON detected — attempting repair...")

#         repair_prompt = f"""
# You are a JSON repair engine.

# Fix the JSON below.
# Rules:
# - Return ONLY valid JSON
# - Do NOT add new fields
# - Do NOT remove fields
# - Close all objects and arrays properly
# - No explanations

# BROKEN JSON:
# {broken_json}
# """

#         response = self.model.generate_content(
#             repair_prompt,
#             generation_config={
#                 "temperature": 0,
#                 "max_output_tokens": self.max_tokens,
#                 "response_mime_type": "application/json",
#             }
#         )

#         return json.loads(response.text)

#     # ============================================
#     # CORE AI EXTRACTION (SAFE)
#     # ============================================

#     def extract_fields(self, text: str) -> Dict:
#         if not text or len(text.strip()) < 20:
#             raise ValueError("Text too short for AI extraction")

#         print("🧠 Sending to Gemini AI for extraction...")

#         prompt = self.create_extraction_prompt(text)

#         response = self.model.generate_content(
#             prompt,
#             generation_config={
#                 "temperature": self.temperature,
#                 "max_output_tokens": self.max_tokens,
#                 "response_mime_type": "application/json",
#             }
#         )

#         raw = response.text

#         try:
#             return json.loads(raw)
#         except json.JSONDecodeError:
#             # 🔥 automatic repair
#             try:
#                 return self._repair_json(raw)
#             except Exception as e:
#                 raise RuntimeError(
#                     f"Gemini returned invalid JSON even after repair attempt: {e}"
#                 )

#     # ============================================
#     # VALIDATION & CONFIDENCE
#     # ============================================

#     def validate_extraction(self, data: Dict) -> Dict:
#         confidence = {}

#         confidence["invoice_number"] = 0.9 if data.get("invoice_number") else 0.0

#         for field in ["invoice_date", "due_date"]:
#             try:
#                 if data.get(field):
#                     datetime.strptime(data[field], "%Y-%m-%d")
#                     confidence[field] = 0.9
#                 else:
#                     confidence[field] = 0.0
#             except Exception:
#                 confidence[field] = 0.3

#         for field in ["subtotal", "tax_amount", "total"]:
#             try:
#                 if data.get(field) is not None:
#                     float(data[field])
#                     confidence[field] = 0.9
#                 else:
#                     confidence[field] = 0.0
#             except Exception:
#                 confidence[field] = 0.3

#         confidence["items"] = 0.9 if data.get("items") else 0.0

#         overall = round(sum(confidence.values()) / len(confidence), 2)

#         data["_metadata"] = {
#             "confidence_scores": confidence,
#             "overall_confidence": overall,
#             "extraction_timestamp": datetime.now().isoformat(),
#         }

#         return data

#     # ============================================
#     # FULL PIPELINE (OCR + AI)
#     # ============================================

#     def extract_from_image(self, image_path: str, validate: bool = True) -> Dict:
#         """
#         Full pipeline:
#         - OCR normal text (header, vendor, totals)
#         - OCR table text (line items)
#         - Merge & send to Gemini
#         """

#         ocr = OCRService()

#         print("👁️ Running OCR (text mode)...")
#         text_ocr = ocr.extract_from_file(
#             image_path, detailed=False, mode="text"
#         )["text"]

#         print("📊 Running OCR (table mode)...")
#         table_ocr = ocr.extract_from_file(
#             image_path, detailed=False, mode="table"
#         )["text"]

#         combined_text = f"""
# ===== HEADER & METADATA =====
# {text_ocr}

# ===== LINE ITEMS TABLE =====
# {table_ocr}
# """

#         data = self.extract_fields(combined_text)

#         if validate:
#             data = self.validate_extraction(data)

#         return data

#     # ============================================
#     # TEXT-ONLY PIPELINE
#     # ============================================

#     def extract_from_text(self, text: str, validate: bool = True) -> Dict:
#         data = self.extract_fields(text)
#         if validate:
#             data = self.validate_extraction(data)
#         return data


# # ============================================
# # TEST MODE
# # ============================================

# if __name__ == "__main__":
#     print("\n🧪 TESTING AI FIELD EXTRACTOR\n")

#     import os

#     extractor = AIExtractor()

#     test_image = (
#         r"C:\My Programs\Machine Learning Project\InvoiceXtract-AI\backend\temp"
#         r"\sampleinvoice_page_1_processed.jpg"
#     )

#     if not os.path.exists(test_image):
#         raise FileNotFoundError(test_image)

#     result = extractor.extract_from_image(test_image, validate=True)

#     print("\n✅ EXTRACTION RESULT\n")
#     print(json.dumps(result, indent=2))


# """
# MODULE 6: AI Field Extractor (FINAL – NUMBER SAFE)
# =================================================
# - Digital PDF → pdfplumber + Camelot (exact numbers)
# - Scanned PDF/Image → OCR fallback
# - Gemini ONLY structures data (never guesses numbers)
# """

# import json
# from typing import Dict, List
# from datetime import datetime
# import google.generativeai as genai
# import pdfplumber
# import camelot
# import os

# from app.utils.config import settings
# from app.services.ocr_service import OCRService


# class AIExtractor:
#     def __init__(self):
#         if not settings.GEMINI_API_KEY:
#             raise RuntimeError("❌ GEMINI_API_KEY not set")

#         genai.configure(api_key=settings.GEMINI_API_KEY)
#         self.model = genai.GenerativeModel("models/gemini-2.5-flash")

#         print("✅ Gemini AI configured: models/gemini-2.5-flash")

#     # =========================================================
#     # PROMPT (STRICT – NO GUESSING)
#     # =========================================================
#     def _prompt(self, text: str, tables: List[Dict]) -> str:
#         return f"""
# You are a FINANCIAL INVOICE EXTRACTION ENGINE.

# RULES:
# - Use numbers ONLY from provided tables
# - Convert all dates to YYYY-MM-DD format.
# - DO NOT invent values
# - DO NOT calculate totals
# - If value missing → null
# - Output ONLY valid JSON

# TEXT:
# {text}

# TABLES:
# {json.dumps(tables, indent=2)}

# JSON FORMAT:
# {{
#   "invoice_number": null,
#   "invoice_date": null,
#   "vendor": {{ "name": null, "address": null }},
#   "customer": {{ "name": null }},
#   "items": [
#     {{
#       "description": "",
#       "quantity": 0,
#       "unit_price": 0,
#       "total": 0
#     }}
#   ],
#   "subtotal": null,
#   "tax_amount": null,
#   "total": null,
#   "currency": "EUR"
# }}
# """

#     # =========================================================
#     # DIGITAL PDF PIPELINE (BEST PATH)
#     # =========================================================
#     def extract_from_pdf(self, pdf_path: str) -> Dict:
#         if not os.path.exists(pdf_path):
#             raise FileNotFoundError(pdf_path)

#         print("📄 Digital PDF detected → Using pdfplumber + Camelot")

#         # ---------- TEXT ----------
#         full_text = ""
#         with pdfplumber.open(pdf_path) as pdf:
#             for page in pdf.pages:
#                 text = page.extract_text()
#                 if text:
#                     full_text += text + "\n"

#         # ---------- TABLES ----------
#         tables = camelot.read_pdf(
#             pdf_path,
#             pages="all",
#             flavor="lattice"
#         )

#         structured_tables = []

#         for table in tables:
#             df = table.df

#             # Clean headers
#             if len(df) > 1:
#                 df.columns = df.iloc[0]
#                 df = df.iloc[1:].reset_index(drop=True)

#             structured_tables.append(df.to_dict(orient="records"))

#         # ---------- GEMINI ----------
#         prompt = self._prompt(full_text, structured_tables)

#         response = self.model.generate_content(
#             prompt,
#             generation_config={
#                 "temperature": 0,
#                 "response_mime_type": "application/json"
#             }
#         )

#         data = json.loads(response.text)
#         return self._add_metadata(data)

#     # =========================================================
#     # SCANNED PDF / IMAGE PIPELINE (OCR FALLBACK)
#     # =========================================================
#     def extract_from_image(self, image_path: str) -> Dict:
#         print("🖼 Scanned document → OCR fallback")

#         ocr = OCRService()
#         text = ocr.extract_from_file(image_path)["text"]

#         prompt = self._prompt(text, [])

#         response = self.model.generate_content(
#             prompt,
#             generation_config={
#                 "temperature": 0,
#                 "response_mime_type": "application/json"
#             }
#         )

#         data = json.loads(response.text)
#         return self._add_metadata(data)

#     # =========================================================
#     # AUTO ROUTER
#     # =========================================================
#     def extract(self, path: str) -> Dict:
#         if path.lower().endswith(".pdf"):
#             try:
#                 # Try digital extraction
#                 return self.extract_from_pdf(path)
#             except Exception:
#                 print("⚠️ Falling back to OCR")
#                 return self.extract_from_image(path)

#         return self.extract_from_image(path)

#     # =========================================================
#     # METADATA
#     # =========================================================
#     def _add_metadata(self, data: Dict) -> Dict:
#         data["_metadata"] = {
#             "extraction_timestamp": datetime.now().isoformat(),
#             "confidence": "HIGH (digital)" if data.get("items") else "LOW (ocr)"
#         }
#         return data


# # =========================================================
# # TEST MODE
# # =========================================================
# if __name__ == "__main__":
#     extractor = AIExtractor()

#     # pdf = r"C:\My Programs\Machine Learning Project\InvoiceXtract-AI\backend\test_invoices\sampleinvoice.pdf"
#     pdf = r"C:\My Programs\Machine Learning Project\InvoiceXtract-AI\backend\temp\sampleinvoice_page_1_processed.jpg"
#     result = extractor.extract(pdf)
#     print(json.dumps(result, indent=2))

# app/services/ai_extractor.py

import json
from datetime import datetime
from typing import Dict, List

import google.generativeai as genai
from app.utils.config import settings


class AIExtractor:
    def __init__(self):
        if not settings.GEMINI_API_KEY:
            raise RuntimeError("❌ GEMINI_API_KEY not set in .env")

        genai.configure(api_key=settings.GEMINI_API_KEY)

        self.model = genai.GenerativeModel(
            model_name="models/gemini-2.5-flash"
        )

    # --------------------------------------------------
    # PROMPT
    # --------------------------------------------------

    def _prompt(self, text: str, tables: List[Dict]) -> str:
        return f"""
You are a STRICT invoice extraction engine.

RULES:
- Use ONLY values present in tables or text
- Convert all dates to YYYY-MM-DD format
- DO NOT calculate totals
- DO NOT guess numbers
- If missing → null
- Output ONLY valid JSON
- No explanations

TEXT:
{text}

TABLES:
{json.dumps(tables, indent=2)}

JSON FORMAT:
{{
  "invoice_number": null,
  "invoice_date": null,
  "vendor": {{
    "name": null,
    "address": null
  }},
  "customer": {{
    "name": null
  }},
  "items": [
    {{
      "description": "",
      "quantity": null,
      "unit_price": null,
      "total": null
    }}
  ],
  "subtotal": null,
  "tax_amount": null,
  "total": null,
  "currency": "EUR"
}}
"""

    # --------------------------------------------------
    # CORE EXTRACTION (PDF → TEXT + TABLES)
    # --------------------------------------------------

    def extract(self, text: str, tables: List[Dict]) -> Dict:
        response = self.model.generate_content(
            self._prompt(text, tables),
            generation_config={
                "temperature": 0,
                "response_mime_type": "application/json"
            }
        )

        data = json.loads(response.text)

        data["_metadata"] = {
            "extraction_timestamp": datetime.now().isoformat(),
            "confidence": "HIGH (digital pdf)"
        }

        return data

    # --------------------------------------------------
    # FASTAPI COMPATIBILITY METHOD (IMPORTANT)
    # --------------------------------------------------

    def extract_from_text(self, text: str, tables: List[Dict]) -> Dict:
        """
        Method called by FastAPI endpoint
        """
        return self.extract(text, tables)
