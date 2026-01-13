import pytesseract
from PIL import Image
import sys
import os

# Try to find tesseract - common windows path
possible_paths = [
    r'C:\Program Files\Tesseract-OCR\tesseract.exe',
    r'C:\Program Files (x86)\Tesseract-OCR\tesseract.exe',
    r'e:\balaji_industry\backend\Tesseract-OCR\tesseract.exe' # Just in case they bundled it
]

for path in possible_paths:
    if os.path.exists(path):
        print(f"Found tesseract at: {path}")
        pytesseract.pytesseract.tesseract_cmd = path
        break
else:
    print("Warning: Tesseract executable not found in common paths. Relying on PATH or default.")

image_path = r"C:/Users/iamka/.gemini/antigravity/brain/c32a0c69-edbf-42dd-afda-d089c1cdcedc/uploaded_image_1_1768227956729.jpg"

try:
    if not os.path.exists(image_path):
        print(f"Error: Image file not found at {image_path}")
        sys.exit(1)

    print(f"Reading image from: {image_path}")
    image = Image.open(image_path)
    text = pytesseract.image_to_string(image)
    print("--- Extracted Text ---")
    print(text)
    print("----------------------")
except Exception as e:
    print(f"Error: {e}")
