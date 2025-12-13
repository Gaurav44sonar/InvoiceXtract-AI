"""
MODULE 4: Image Preprocessor
=============================
This module improves the quality of images before OCR.
It uses an AUTO-MODE system:

- If image is high quality → Simple preprocessing
- If image is faint, noisy, low-contrast → Advanced preprocessing

This dramatically improves Tesseract OCR accuracy.

Author: Invoice OCR System
Version: 1.0.0
"""

import cv2
import numpy as np
from pathlib import Path
from typing import Tuple
from PIL import Image, ImageEnhance
# from app.utils.config import settings
from backend.app.utils.config import settings


class ImagePreprocessor:
    """
    Hybrid Image Preprocessor
    Automatically switches between simple and advanced modes.
    """

    def __init__(self):
        self.enable_preprocessing = settings.ENABLE_PREPROCESSING
        self.default_dpi = settings.PDF_DPI

    # ==========================
    # Utility Converters
    # ==========================

    @staticmethod
    def pil_to_cv(img: Image.Image):
        """Convert PIL → OpenCV"""
        return cv2.cvtColor(np.array(img), cv2.COLOR_RGB2BGR)

    @staticmethod
    def cv_to_pil(img_cv):
        """Convert OpenCV → PIL"""
        img_rgb = cv2.cvtColor(img_cv, cv2.COLOR_BGR2RGB)
        return Image.fromarray(img_rgb)

    # ==========================
    # SIMPLE MODE
    # ==========================

    def simple_preprocess(self, img: Image.Image) -> Image.Image:
        """
        Simple preprocessing for clean images.
        Faster, lighter, and works well for high-quality invoices.
        """
        img = img.convert("L")  # grayscale

        # Increase contrast slightly
        enhancer = ImageEnhance.Contrast(img)
        img = enhancer.enhance(1.5)

        # Slightly sharpen
        enhancer = ImageEnhance.Sharpness(img)
        img = enhancer.enhance(1.2)

        return img

    # ==========================
    # ADVANCED MODE
    # ==========================

    def advanced_preprocess(self, img: Image.Image) -> Image.Image:
        """
        Advanced preprocessing for low-quality, noisy, faint invoices.
        Uses OpenCV for maximum OCR accuracy.
        """
        img_cv = self.pil_to_cv(img)

        # Convert to grayscale
        gray = cv2.cvtColor(img_cv, cv2.COLOR_BGR2GRAY)

        # Remove noise using bilateral filter
        denoised = cv2.bilateralFilter(gray, 9, 75, 75)

        # Adaptive threshold
        thresh = cv2.adaptiveThreshold(
            denoised,
            255,
            cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
            cv2.THRESH_BINARY,
            35,
            11
        )

        # Morphological operations to fix broken characters
        kernel = np.ones((1, 1), np.uint8)
        processed = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel)

        return self.cv_to_pil(processed)

    # ==========================
    # AUTO MODE DECISION
    # ==========================

    def should_use_advanced(self, img: Image.Image) -> bool:
        """
        Decide whether to use advanced mode based on image quality.
        Measures:
        - brightness
        - contrast
        - noise level
        """
        img_cv = self.pil_to_cv(img)
        gray = cv2.cvtColor(img_cv, cv2.COLOR_BGR2GRAY)

        brightness = gray.mean()
        contrast = gray.std()

        # If image is faint/dark/low contrast → advanced mode
        if brightness < 130 or contrast < 50:
            return True
        return False

    # ==========================
    # MAIN PUBLIC METHOD
    # ==========================

    def preprocess(self, img: Image.Image) -> Image.Image:
        """
        Preprocess an image in the best possible way.
        """
        if not self.enable_preprocessing:
            return img

        if self.should_use_advanced(img):
            print("⚡ Using ADVANCED preprocessing")
            return self.advanced_preprocess(img)

        print("✨ Using SIMPLE preprocessing")
        return self.simple_preprocess(img)


# ==========================
# TEST MODULE
# ==========================

if __name__ == "__main__":
    import os

    print("\n==============================")
    print("🧪 TESTING IMAGE PREPROCESSOR")
    print("==============================\n")

    test_image_path = "C:/My Programs/Machine Learning Project/InvoiceXtract-AI/backend/app/services/test_invoice_page.jpg"

    if not os.path.exists(test_image_path):
        print(f"⚠️ No test image found: {test_image_path}")
        print("Place an image named 'test_invoice_page.jpg' in this folder to test.")
    else:
        img = Image.open(test_image_path)

        processor = ImagePreprocessor()
        processed = processor.preprocess(img)

        processed.save("processed_output.jpg")
        print("✅ Preprocessing complete! Saved as processed_output.jpg")
