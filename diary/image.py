"""
Image processing and OCR capabilities
"""

from PIL import Image
import os
from typing import Optional

# Try to import pytesseract, but handle gracefully if not available
try:
    import pytesseract
    OCR_AVAILABLE = True
except ImportError:
    OCR_AVAILABLE = False


class ImageProcessor:
    """Service for processing images"""
    
    def __init__(self):
        self.use_ocr = OCR_AVAILABLE
    
    async def process_image(self, image_path: str) -> str:
        """
        Process image and extract text if applicable
        
        Args:
            image_path: Path to image file
            
        Returns:
            Extracted text or metadata
        """
        if not os.path.exists(image_path):
            raise FileNotFoundError(f"Image file not found: {image_path}")
        
        text = ""
        
        # Try OCR to extract text from image
        if self.use_ocr:
            try:
                image = Image.open(image_path)
                # Convert to RGB if necessary
                if image.mode != 'RGB':
                    image = image.convert('RGB')
                
                # Extract text using OCR
                text = pytesseract.image_to_string(image)
                text = text.strip()
                
            except Exception as e:
                print(f"OCR not available or failed: {e}")
                text = "[Image content]"
        else:
            text = "[Image content]"
        
        # Generate basic description if no text found
        if not text:
            try:
                image = Image.open(image_path)
                width, height = image.size
                text = f"[Image: {width}x{height} pixels]"
            except:
                text = "[Image]"
        
        return text
    
    async def extract_metadata(self, image_path: str) -> dict:
        """
        Extract metadata from image
        
        Returns:
            Dictionary with image metadata
        """
        if not os.path.exists(image_path):
            raise FileNotFoundError(f"Image file not found: {image_path}")
        
        try:
            image = Image.open(image_path)
            metadata = {
                "width": image.width,
                "height": image.height,
                "format": image.format,
                "mode": image.mode
            }
            
            # Extract EXIF data if available
            if hasattr(image, '_getexif') and image._getexif():
                exif = image._getexif()
                metadata["exif"] = str(exif)
            
            return metadata
        
        except Exception as e:
            print(f"Error extracting metadata: {e}")
            return {}
