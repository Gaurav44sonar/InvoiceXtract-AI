# """
# MODULE 4: Image Preprocessor
# =============================
# This module improves the quality of images before OCR.
# It uses an AUTO-MODE system:

# - If image is high quality → Simple preprocessing
# - If image is faint, noisy, low-contrast → Advanced preprocessing

# This dramatically improves Tesseract OCR accuracy.

# Author: Invoice OCR System
# Version: 1.0.0
# """

# import cv2
# import numpy as np
# from pathlib import Path
# from typing import Tuple
# from PIL import Image, ImageEnhance
# # from app.utils.config import settings
# from backend.app.utils.config import settings


# class ImagePreprocessor:
#     """
#     Hybrid Image Preprocessor
#     Automatically switches between simple and advanced modes.
#     """

#     def __init__(self):
#         self.enable_preprocessing = settings.ENABLE_PREPROCESSING
#         self.default_dpi = settings.PDF_DPI

#     # ==========================
#     # Utility Converters
#     # ==========================

#     @staticmethod
#     def pil_to_cv(img: Image.Image):
#         """Convert PIL → OpenCV"""
#         return cv2.cvtColor(np.array(img), cv2.COLOR_RGB2BGR)

#     @staticmethod
#     def cv_to_pil(img_cv):
#         """Convert OpenCV → PIL"""
#         img_rgb = cv2.cvtColor(img_cv, cv2.COLOR_BGR2RGB)
#         return Image.fromarray(img_rgb)

#     # ==========================
#     # SIMPLE MODE
#     # ==========================

#     def simple_preprocess(self, img: Image.Image) -> Image.Image:
#         """
#         Simple preprocessing for clean images.
#         Faster, lighter, and works well for high-quality invoices.
#         """
#         img = img.convert("L")  # grayscale

#         # Increase contrast slightly
#         enhancer = ImageEnhance.Contrast(img)
#         img = enhancer.enhance(1.5)

#         # Slightly sharpen
#         enhancer = ImageEnhance.Sharpness(img)
#         img = enhancer.enhance(1.2)

#         return img

#     # ==========================
#     # ADVANCED MODE
#     # ==========================

#     def advanced_preprocess(self, img: Image.Image) -> Image.Image:
#         """
#         Advanced preprocessing for low-quality, noisy, faint invoices.
#         Uses OpenCV for maximum OCR accuracy.
#         """
#         img_cv = self.pil_to_cv(img)

#         # Convert to grayscale
#         gray = cv2.cvtColor(img_cv, cv2.COLOR_BGR2GRAY)

#         # Remove noise using bilateral filter
#         denoised = cv2.bilateralFilter(gray, 9, 75, 75)

#         # Adaptive threshold
#         thresh = cv2.adaptiveThreshold(
#             denoised,
#             255,
#             cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
#             cv2.THRESH_BINARY,
#             35,
#             11
#         )

#         # Morphological operations to fix broken characters
#         kernel = np.ones((1, 1), np.uint8)
#         processed = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel)

#         return self.cv_to_pil(processed)

#     # ==========================
#     # AUTO MODE DECISION
#     # ==========================

#     def should_use_advanced(self, img: Image.Image) -> bool:
#         """
#         Decide whether to use advanced mode based on image quality.
#         Measures:
#         - brightness
#         - contrast
#         - noise level
#         """
#         img_cv = self.pil_to_cv(img)
#         gray = cv2.cvtColor(img_cv, cv2.COLOR_BGR2GRAY)

#         brightness = gray.mean()
#         contrast = gray.std()

#         # If image is faint/dark/low contrast → advanced mode
#         if brightness < 130 or contrast < 50:
#             return True
#         return False

#     # ==========================
#     # MAIN PUBLIC METHOD
#     # ==========================

#     def preprocess(self, img: Image.Image) -> Image.Image:
#         """
#         Preprocess an image in the best possible way.
#         """
#         if not self.enable_preprocessing:
#             return img

#         if self.should_use_advanced(img):
#             print("⚡ Using ADVANCED preprocessing")
#             return self.advanced_preprocess(img)

#         print("✨ Using SIMPLE preprocessing")
#         return self.simple_preprocess(img)


# # ==========================
# # TEST MODULE
# # ==========================

# if __name__ == "__main__":
#     import os

#     print("\n==============================")
#     print("🧪 TESTING IMAGE PREPROCESSOR")
#     print("==============================\n")

#     test_image_path = "C:/My Programs/Machine Learning Project/InvoiceXtract-AI/backend/app/services/test_invoice_page.jpg"

#     if not os.path.exists(test_image_path):
#         print(f"⚠️ No test image found: {test_image_path}")
#         print("Place an image named 'test_invoice_page.jpg' in this folder to test.")
#     else:
#         img = Image.open(test_image_path)

#         processor = ImagePreprocessor()
#         processed = processor.preprocess(img)

#         processed.save("processed_output.jpg")
#         print("✅ Preprocessing complete! Saved as processed_output.jpg")




"""
MODULE 4: Image Preprocessor
=============================
Improves image quality before OCR to increase text extraction accuracy.
Uses AUTO-MODE to choose between simple and advanced preprocessing.

Think of this like data normalization in ML - preparing inputs for better results!

Author: Invoice OCR System
Version: 1.0.0
"""

import cv2
import numpy as np
from pathlib import Path
from typing import Tuple, Optional
from PIL import Image, ImageEnhance

from app.utils.config import settings


class ImagePreprocessor:
    """
    Intelligent Image Preprocessor
    ==============================
    Automatically detects image quality and applies appropriate preprocessing:
    - High quality images → Simple preprocessing (faster)
    - Low quality/noisy images → Advanced preprocessing (better accuracy)
    """

    def __init__(self):
        """Initialize preprocessor with settings"""
        self.enable_preprocessing = settings.ENABLE_PREPROCESSING
        self.image_quality = settings.IMAGE_QUALITY
        self.default_dpi = settings.PDF_DPI

    # ============================================
    # UTILITY CONVERTERS
    # ============================================

    @staticmethod
    def pil_to_cv(img: Image.Image) -> np.ndarray:
        """
        Convert PIL Image to OpenCV format (BGR)
        
        Args:
            img: PIL Image
            
        Returns:
            OpenCV image (numpy array)
        """
        return cv2.cvtColor(np.array(img), cv2.COLOR_RGB2BGR)

    @staticmethod
    def cv_to_pil(img_cv: np.ndarray) -> Image.Image:
        """
        Convert OpenCV image to PIL format
        
        Args:
            img_cv: OpenCV image (numpy array)
            
        Returns:
            PIL Image
        """
        img_rgb = cv2.cvtColor(img_cv, cv2.COLOR_BGR2RGB)
        return Image.fromarray(img_rgb)

    # ============================================
    # IMAGE QUALITY ANALYSIS
    # ============================================

    def analyze_image_quality(self, img: Image.Image) -> dict:
        """
        Analyze image quality metrics
        
        Args:
            img: PIL Image
            
        Returns:
            Dictionary with quality metrics
        """
        img_cv = self.pil_to_cv(img)
        gray = cv2.cvtColor(img_cv, cv2.COLOR_BGR2GRAY)

        # Calculate metrics
        brightness = gray.mean()
        contrast = gray.std()
        
        # Calculate sharpness using Laplacian variance
        laplacian = cv2.Laplacian(gray, cv2.CV_64F)
        sharpness = laplacian.var()

        return {
            'brightness': float(brightness),
            'contrast': float(contrast),
            'sharpness': float(sharpness),
            'resolution': img.size
        }

    def should_use_advanced(self, img: Image.Image) -> Tuple[bool, str]:
        """
        Decide whether to use advanced preprocessing
        
        Args:
            img: PIL Image
            
        Returns:
            Tuple of (use_advanced: bool, reason: str)
        """
        metrics = self.analyze_image_quality(img)
        
        brightness = metrics['brightness']
        contrast = metrics['contrast']
        sharpness = metrics['sharpness']

        # Decision logic
        reasons = []
        
        if brightness < 100:
            reasons.append("too dark")
        elif brightness > 200:
            reasons.append("too bright")
        
        if contrast < 40:
            reasons.append("low contrast")
        
        if sharpness < 100:
            reasons.append("blurry")

        if reasons:
            return True, ", ".join(reasons)
        
        return False, "good quality"

    # ============================================
    # SIMPLE PREPROCESSING (Fast)
    # ============================================

    def simple_preprocess(self, img: Image.Image) -> Image.Image:
        """
        Simple preprocessing for clean, high-quality images.
        Fast and effective for well-scanned invoices.
        
        Steps:
        1. Convert to grayscale
        2. Enhance contrast slightly
        3. Sharpen edges
        
        Args:
            img: PIL Image
            
        Returns:
            Preprocessed PIL Image
        """
        # Convert to grayscale
        if img.mode != 'L':
            img = img.convert('L')

        # Increase contrast slightly
        enhancer = ImageEnhance.Contrast(img)
        img = enhancer.enhance(1.5)

        # Slightly sharpen for clearer text
        enhancer = ImageEnhance.Sharpness(img)
        img = enhancer.enhance(1.2)

        return img

    # ============================================
    # ADVANCED PREPROCESSING (Accurate)
    # ============================================

    def advanced_preprocess(self, img: Image.Image) -> Image.Image:
        """
        Advanced preprocessing for low-quality, noisy, or faint images.
        Uses OpenCV for maximum OCR accuracy.
        
        Steps:
        1. Convert to grayscale
        2. Remove noise (bilateral filter)
        3. Adaptive thresholding (handles varying lighting)
        4. Morphological operations (fix broken characters)
        
        Args:
            img: PIL Image
            
        Returns:
            Preprocessed PIL Image
        """
        # Convert to OpenCV format
        img_cv = self.pil_to_cv(img)

        # Convert to grayscale
        gray = cv2.cvtColor(img_cv, cv2.COLOR_BGR2GRAY)

        # Remove noise using bilateral filter
        # Preserves edges while removing noise
        denoised = cv2.bilateralFilter(gray, 9, 75, 75)

        # Apply adaptive thresholding
        # Works better than simple threshold for varying lighting
        thresh = cv2.adaptiveThreshold(
            denoised,
            255,
            cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
            cv2.THRESH_BINARY,
            35,  # Block size
            11   # Constant subtracted from mean
        )

        # Morphological operations to connect broken text
        kernel = np.ones((1, 1), np.uint8)
        processed = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel)

        # Convert back to PIL
        return self.cv_to_pil(processed)

    # ============================================
    # DESKEW (Remove Rotation)
    # ============================================

    def deskew(self, img: Image.Image) -> Image.Image:
        """
        Remove skew (rotation) from scanned images.
        Useful for images captured at an angle.
        
        Args:
            img: PIL Image
            
        Returns:
            Deskewed PIL Image
        """
        img_cv = self.pil_to_cv(img)
        gray = cv2.cvtColor(img_cv, cv2.COLOR_BGR2GRAY)
        
        # Detect edges
        edges = cv2.Canny(gray, 50, 150, apertureSize=3)
        
        # Detect lines using Hough transform
        lines = cv2.HoughLines(edges, 1, np.pi/180, 200)
        
        if lines is not None and len(lines) > 0:
            # Calculate average angle
            angles = []
            for rho, theta in lines[:, 0]:
                angle = (theta * 180 / np.pi) - 90
                angles.append(angle)
            
            median_angle = np.median(angles)
            
            # Only deskew if angle is significant
            if abs(median_angle) > 0.5:
                # Rotate image
                (h, w) = img_cv.shape[:2]
                center = (w // 2, h // 2)
                M = cv2.getRotationMatrix2D(center, median_angle, 1.0)
                rotated = cv2.warpAffine(
                    img_cv, M, (w, h),
                    flags=cv2.INTER_CUBIC,
                    borderMode=cv2.BORDER_REPLICATE
                )
                
                print(f"🔄 Deskewed image by {median_angle:.2f}°")
                return self.cv_to_pil(rotated)
        
        return img

    # ============================================
    # MAIN PUBLIC METHOD
    # ============================================

    def preprocess(
        self,
        img: Image.Image,
        force_mode: Optional[str] = None,
        apply_deskew: bool = False
    ) -> Image.Image:
        """
        Preprocess an image intelligently.
        
        Args:
            img: PIL Image to preprocess
            force_mode: Force 'simple' or 'advanced' mode (optional)
            apply_deskew: Whether to apply deskew correction
            
        Returns:
            Preprocessed PIL Image
        """
        # Skip if preprocessing disabled
        if not self.enable_preprocessing:
            print("⏭️  Preprocessing disabled in settings")
            return img

        # Apply deskew if requested
        if apply_deskew:
            img = self.deskew(img)

        # Decide mode
        if force_mode:
            use_advanced = (force_mode.lower() == 'advanced')
            reason = f"forced {force_mode}"
        else:
            use_advanced, reason = self.should_use_advanced(img)

        # Apply preprocessing
        if use_advanced:
            print(f"⚡ Using ADVANCED preprocessing ({reason})")
            return self.advanced_preprocess(img)
        else:
            print(f"✨ Using SIMPLE preprocessing ({reason})")
            return self.simple_preprocess(img)

    def preprocess_file(
        self,
        input_path: str,
        output_path: Optional[str] = None,
        **kwargs
    ) -> str:
        """
        Preprocess an image file and save result.
        
        Args:
            input_path: Path to input image
            output_path: Path to save preprocessed image (optional)
            **kwargs: Additional arguments for preprocess()
            
        Returns:
            Path to saved preprocessed image
        """
        # Load image
        img = Image.open(input_path)
        
        # Preprocess
        processed = self.preprocess(img, **kwargs)
        
        # Generate output path if not provided
        if output_path is None:
            input_path_obj = Path(input_path)
            output_path = str(
                input_path_obj.parent / 
                f"{input_path_obj.stem}_processed{input_path_obj.suffix}"
            )
        
        # Save
        processed.save(output_path, quality=self.image_quality)
        
        return output_path


# ============================================
# HELPER FUNCTION
# ============================================

def preprocess_image(
    img: Image.Image,
    mode: str = 'auto'
) -> Image.Image:
    """
    Convenience function to preprocess an image.
    
    Args:
        img: PIL Image
        mode: 'auto', 'simple', or 'advanced'
        
    Returns:
        Preprocessed PIL Image
    """
    processor = ImagePreprocessor()
    
    if mode == 'auto':
        return processor.preprocess(img)
    else:
        return processor.preprocess(img, force_mode=mode)


# ============================================
# TEST/DEBUG MODE
# ============================================

if __name__ == "__main__":
    """
    Test the image preprocessor
    Run: python app/services/image_preprocessor.py
    """
    
    print("\n" + "=" * 60)
    print("🧪 TESTING IMAGE PREPROCESSOR MODULE")
    print("=" * 60 + "\n")

    # Create preprocessor
    processor = ImagePreprocessor()

    # Test with converted PDF images from MODULE 3
    import os
    
    test_images = [
        r"C:\My Programs\Machine Learning Project\InvoiceXtract-AI\backend\temp\sampleinvoice_page_1.jpg",
        r"C:\My Programs\Machine Learning Project\InvoiceXtract-AI\backend\temp\sampleinvoice_page_2.jpg",
        r"C:\My Programs\Machine Learning Project\InvoiceXtract-AI\backend\temp\sampleinvoice_page_3.jpg"
    ]

    for test_image in test_images:
        if os.path.exists(test_image):
            print(f"\n📄 Testing: {Path(test_image).name}")
            
            # Load image
            img = Image.open(test_image)
            print(f"  Original size: {img.size}")
            
            # Analyze quality
            metrics = processor.analyze_image_quality(img)
            print(f"  Brightness: {metrics['brightness']:.1f}")
            print(f"  Contrast: {metrics['contrast']:.1f}")
            print(f"  Sharpness: {metrics['sharpness']:.1f}")
            
            # Preprocess
            print(f"\n  Processing...")
            processed = processor.preprocess(img)
            
            # Save processed image
            output_path = str(Path(test_image).parent / f"{Path(test_image).stem}_processed.jpg")
            processed.save(output_path, quality=95)
            print(f"  ✅ Saved: {Path(output_path).name}")
        else:
            print(f"\n⚠️  Image not found: {test_image}")
            print("  Run MODULE 3 first to generate test images!")

    print("\n" + "=" * 60)
    print("✅ Image Preprocessor test complete!")
    print("=" * 60 + "\n")
    
    print("💡 TIP: Check the 'temp' folder to see original vs processed images!")