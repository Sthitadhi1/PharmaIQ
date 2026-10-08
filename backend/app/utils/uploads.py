import os
from pathlib import PureWindowsPath

from fastapi import HTTPException, UploadFile, status

from app.database.config import ALLOWED_UPLOAD_EXTENSIONS, MAX_UPLOAD_BYTES, UPLOAD_DIR


def safe_filename(filename: str) -> str:
    """Strip any directory component so uploads cannot escape UPLOAD_DIR.

    PureWindowsPath splits on both '/' and '\\', so '../x' and '..\\x' are both caught.
    """
    name = PureWindowsPath(filename or '').name.strip()
    if not name or name in {'.', '..'}:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='A valid file name is required.')
    extension = os.path.splitext(name)[1].lower()
    if extension not in ALLOWED_UPLOAD_EXTENSIONS:
        allowed = ', '.join(sorted(ALLOWED_UPLOAD_EXTENSIONS))
        raise HTTPException(
            status_code=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE,
            detail=f'Unsupported file type "{extension or "none"}". Allowed: {allowed}.'
        )
    return name


async def save_upload(upload_file: UploadFile) -> str:
    name = safe_filename(upload_file.filename)
    try:
        contents = await upload_file.read(MAX_UPLOAD_BYTES + 1)
    finally:
        await upload_file.close()
    if len(contents) > MAX_UPLOAD_BYTES:
        raise HTTPException(
            status_code=status.HTTP_413_CONTENT_TOO_LARGE,
            detail=f'File exceeds the {MAX_UPLOAD_BYTES // (1024 * 1024)} MB limit.'
        )
    if not contents:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Uploaded file is empty.')

    os.makedirs(UPLOAD_DIR, exist_ok=True)
    target_path = os.path.join(UPLOAD_DIR, name)
    with open(target_path, 'wb') as buffer:
        buffer.write(contents)
    return target_path
