from fastapi import APIRouter, UploadFile, File, HTTPException
from ..services import ocr
import shutil

router = APIRouter(
    prefix="/ocr",
    tags=["ocr"],
    responses={404: {"description": "Not found"}},
)

@router.post("/extract")
async def extract_text(file: UploadFile = File(...)):
    if not file.content_type.startswith('image/'):
        raise HTTPException(status_code=400, detail="File must be an image")
    
    contents = await file.read()
    
    # Process with OCR
    # Run synchronous OCR in a threadpool to avoid blocking event loop
    from fastapi.concurrency import run_in_threadpool
    text = await run_in_threadpool(ocr.extract_text_from_image, contents)
    parsed_data = ocr.parse_ledger_text(text)
    
    return {
        "filename": file.filename,
        "content_type": file.content_type,
        "extracted_text": text,
        "parsed_data": parsed_data
    }
