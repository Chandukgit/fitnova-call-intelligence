from fastapi import (
    APIRouter,
    Depends,
    File,
    Form,
    UploadFile,
    BackgroundTasks,
)
from sqlalchemy.orm import Session

from app.api.dependencies import get_db
from app.core.auth import get_current_user
from app.services.upload import upload_service
from app.services.call import call_service
from app.schemas.call import CallCreate

router = APIRouter(
    prefix="/upload",
    tags=["Upload"],
)


def run_pipeline_in_background(call_id: int, audio_path: str):
    from app.database.session import SessionLocal
    from app.ai.analysis.pipeline import analysis_pipeline
    db = SessionLocal()
    try:
        analysis_pipeline.process(
            db=db,
            call_id=call_id,
            audio_path=audio_path,
        )
    finally:
        db.close()


@router.post("/audio")
async def upload_audio(
    background_tasks: BackgroundTasks,
    advisor_id: int = Form(...),
    customer_id: int = Form(...),
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):

    upload_result = await upload_service.upload_audio(
        organization_id=1,
        file=file,
    )

    call = call_service.create_call(
        db=db,
        call_in=CallCreate(
            advisor_id=advisor_id,
            customer_id=customer_id,
            original_filename=file.filename,
            audio_path=upload_result["path"],
            mime_type=file.content_type,
            file_size=upload_result["size"],
        ),
    )

    background_tasks.add_task(
        run_pipeline_in_background,
        call_id=call.id,
        audio_path=call.audio_path,
    )

    return {
        "message": "Audio uploaded successfully.",
        "call_id": call.id,
        "status": call.call_status,
    }