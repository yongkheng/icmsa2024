from database.config import get_settings
from models import models
from fastapi import Depends, APIRouter, Request, BackgroundTasks, Response, HTTPException
from fastapi.responses import HTMLResponse
from database.database import SessionLocal, engine
from sqlalchemy.orm import Session

router = APIRouter()
models.Base.metadata.create_all(bind=engine)
settings = get_settings()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get("/api/get_file")
async def get_file(
        fname, request: Request, background_tasks: BackgroundTasks, db: Session = Depends(get_db),
):
    # get record
    rec = (
        db.query(models.Submission)
        .filter(models.Submission.submission_filename == fname)
        .first()
    )

    # parse query types: abstract, full_paper, camera_ready or copy_right
    query_type = fname.split('_')[0]
    print(f"get_file(): {fname=} {query_type}")

    if query_type=="abstract":
        content = rec.abstract_content
    elif query_type=="full":
        content = "rec.fullpaper_content"
        print(rec.submission_id, rec.revision_version)
    else:
        message = f"File not found: {fname=}"
        raise HTTPException(status_code=400, detail=message)

    # Set the appropriate response headers for file download
    response = Response(content=content, media_type="application/octet-stream")
    response.headers["Content-Disposition"] = f"attachment; filename={fname}"

    return response

@router.get("/api/get_receipt")
async def get_receipt(
        fname, request: Request, background_tasks: BackgroundTasks, db: Session = Depends(get_db),
):
    rec = (
        db.query(models.Submission)
        .filter(models.Submission.submission_filename == fname)
        .first()
    )

    html = 'unknown'
    if rec.submission_type == "abstract":
        html = rec.abstract_receipt
    elif rec.submission_type == "full-paper":
        html = rec.fullpaper_receipt
    elif rec.submission_type == "camera_ready":
        html = rec.camera_ready_receipt

    return HTMLResponse(content=html, status_code=200)

@router.get("/api/get_payment_proof")
async def get_payment_proof(
        fname, request: Request, background_tasks: BackgroundTasks, db: Session = Depends(get_db),
):
    rec = (
        db.query(models.Registration)
        .filter(models.Registration.payment_proof_filename == fname)
        .first()
    )

    content = rec.payment_proof_content

    # Set the appropriate response headers for file download
    response = Response(content=content, media_type="application/octet-stream")
    response.headers["Content-Disposition"] = f"attachment; filename={fname}"

    return response

@router.get("/api/get_student_proof")
async def get_payment_proof(
        fname, request: Request, background_tasks: BackgroundTasks, db: Session = Depends(get_db),
):
    rec = (
        db.query(models.Registration)
        .filter(models.Registration.student_status_proof_filename == fname)
        .first()
    )

    content = rec.student_status_proof_content

    # Set the appropriate response headers for file download
    response = Response(content=content, media_type="application/octet-stream")
    response.headers["Content-Disposition"] = f"attachment; filename={fname}"

    return response
