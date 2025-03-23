from fastapi import APIRouter, File, UploadFile, Form
from typing import List
import os
from main import main
from add_missing_data import interpolate_bounding_boxes
from pathlib import Path

router = APIRouter()

UPLOAD_DIR = Path("uploads")
UPLOAD_DIR.mkdir(exist_ok=True)


@router.post("/api/video-input/upload/")
def video_input_upload(video: UploadFile = File(...),
                       red_list_numbers: List[str] = Form(...)):
    file_path = UPLOAD_DIR / video.filename

    # Read & Write File Synchronously
    with file_path.open("wb") as buffer:
        buffer.write(video.file.read())
    main(UPLOAD_DIR, video)
    data = interpolate_bounding_boxes(red_list_numbers)
    

    return {'data': data}