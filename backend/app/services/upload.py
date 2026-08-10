from pathlib import Path
from uuid import uuid4

from fastapi import UploadFile, HTTPException

from app.storage.local_storage import storage


class UploadService:

    ALLOWED_EXTENSIONS = {
        ".wav",
        ".mp3",
        ".m4a",
        ".mpeg",
    }

    MAX_FILE_SIZE = 50 * 1024 * 1024  # 50 MB

    async def upload_audio(
        self,
        organization_id: int,
        file: UploadFile,
    ):

        extension = Path(file.filename).suffix.lower()

        if extension not in self.ALLOWED_EXTENSIONS:
            raise HTTPException(
                status_code=400,
                detail="Unsupported audio format.",
            )

        file_bytes = await file.read()

        if len(file_bytes) > self.MAX_FILE_SIZE:
            raise HTTPException(
                status_code=400,
                detail="File size exceeds 50 MB.",
            )

        filename = f"{uuid4()}{extension}"

        relative_path = (
            f"organization_{organization_id}/"
            f"{filename}"
        )

        saved_path = storage.save_file(
            file_bytes=file_bytes,
            file_path=relative_path,
        )

        return {
            "filename": filename,
            "path": str(saved_path),
            "size": len(file_bytes),
        }


upload_service = UploadService()