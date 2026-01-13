import pytesseract
from PIL import Image
import io

# Ensure tesseract is in path or configured. 
# For windows, typical path: C:\Program Files\Tesseract-OCR\tesseract.exe
# We will try to find it or let user configure it via env.
import os

# Set tesseract cmd if needed specific to environment
# pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

def extract_text_from_image(image_bytes: bytes) -> str:
    try:
        image = Image.open(io.BytesIO(image_bytes))
        text = pytesseract.image_to_string(image)
        return text
    except Exception as e:
        print(f"OCR Error: {e}")
        return ""

import re

def parse_ledger_text(text: str) -> dict:
    lines = [line.strip() for line in text.split('\n') if line.strip()]
    structured_data = []
    
    # Regex patterns for common ledger elements
    # Date pattern (DD/MM/YY or DD-MM-YY)
    date_pattern = r'(\d{1,2}[/-]\d{1,2}[/-]\d{2,4})'
    # Amount pattern (numbers with opt commas and decimals)
    amount_pattern = r'(\d{1,3}(?:,\d{3})*(?:\.\d{2})?)'
    
    for line in lines:
        # Attempt to extract date
        date_match = re.search(date_pattern, line)
        date = date_match.group(0) if date_match else ""
        
        # Attempt to extract numbers
        # We look for the last number in the line as likely amount, or maybe two numbers (debit/credit)
        numbers = re.findall(amount_pattern, line)
        amount = 0.0
        if numbers:
            # Simple heuristic: take the largest number found as the transaction amount
            # Or the last one. Let's try to filter out date parts or line numbers.
            try:
                # Filter out numbers that look like dates (e.g. 2023) if possible, but hard.
                # Let's just take the last numeric sequence that is not the date.
                valid_amounts = [float(n.replace(',', '')) for n in numbers if len(n) > 1]
                if valid_amounts:
                    amount = valid_amounts[-1]
            except:
                pass

        # Description is everything else
        description = line
        if date:
            description = description.replace(date, '')
        if amount:
            # Remove the amount string from description roughly
            description = re.sub(amount_pattern, '', description)
        
        # Clean up description
        description = re.sub(r'[^\w\s]', '', description).strip()
        
        structured_data.append({
            "original": line,
            "date": date,
            "description": description,
            "amount": amount,
            "type": "Credit" # Default to Credit, user can change
        })

    return {
        "raw_text": text,
        "lines": lines,
        "structured_data": structured_data
    }
