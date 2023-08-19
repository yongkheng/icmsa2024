from datetime import datetime

from database.config import get_settings
from models import models
from fastapi import Depends, APIRouter, Request, BackgroundTasks, HTTPException
from database.database import SessionLocal, engine
from sqlalchemy.orm import Session

from views.receipts import submit_receipt

router = APIRouter()
models.Base.metadata.create_all(bind=engine)
settings = get_settings()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def make_local_copy(rec: models.Submission):
    with open(f"submit_db/files/{rec.fullpaper_filename}", "wb") as f_handle:
        f_handle.write(rec.fullpaper_content)
    with open(f"submit_db/files/{rec.fullpaper_filename}.receipt.html", 'wb') as f_handle:
        f_handle.write(rec.fullpaper_receipt)


@router.post("/api/form_manuscript")
async def form_manuscript(request: Request, background_tasks: BackgroundTasks, db: Session = Depends(get_db)):
    submission_type = "camera_ready"
    form = await request.form()
    form = dict(form)

    # retrieve record
    resp = (
        db.query(models.Submission)
        .filter(models.Submission.corresponding_email == form["corresponding_email"])
        .filter(models.Submission.submission_id == form["submission_id"])
    )

    # check if submission is valid
    if resp.all():
        # valid submission
        available_versions = [r.revision_version for r in resp.all()]
        latest_record = [r for r in resp.all() if r.revision_version == max(available_versions)][0]
        print(latest_record.submission_id, latest_record.corresponding_email, latest_record.revision_version)

        # update revision_version, timestamp, submission_filename
        revision_version = latest_record.revision_version + 1
        timestamp = datetime.now()
        ts1 = timestamp.strftime("%Y-%m-%d")
        file_ext = form["submission_pdf_file"].filename.split('.')[-1]
        submission_filename = f"{submission_type}_{ts1}_{latest_record.submission_id}_rev{revision_version}.{file_ext}"
        submission_license_filename =f"copyright__{ts1}_{latest_record.submission_id}_rev{revision_version}.pdf"
        # duplicate record
        new_rec = models.Submission(
            submission_id=latest_record.submission_id,
            revision_version=revision_version,
            timestamp=latest_record.timestamp,
            corresponding_name=latest_record.corresponding_name,
            corresponding_email=latest_record.corresponding_email,
            submission_title=latest_record.submission_title,
            submission_keywords=latest_record.submission_keywords,
            submission_type=submission_type,
            submission_filename=submission_filename,

            abstract_filename=latest_record.abstract_filename,
            abstract_content=latest_record.abstract_content,
            abstract_receipt=latest_record.abstract_receipt,
            in_proceedings=latest_record.in_proceedings,
            in_journal=latest_record.in_journal,

            fullpaper_filename=latest_record.fullpaper_filename,
            fullpaper_content=latest_record.fullpaper_content,
            fullpaper_receipt=latest_record.fullpaper_receipt,

            camera_ready_filename=submission_filename,
            camera_ready_content=form["submission_pdf_file"].file.read(),
            camera_ready_receipt=None,
            copy_right_filename=submission_license_filename,
            copy_right_content=form["submission_license_file"].file.read(),
            copy_right_receipt=None
        )


        # generate receipt
        html = submit_receipt(request, new_rec)
        with open("receipt.html", 'wb') as f:
            f.write(html.body)
        new_rec.camera_ready_receipt = html.body

        # save to database
        db.add(new_rec)
        db.commit()
        db.refresh(new_rec)

        # generate a local copy in case of corrupted database
        make_local_copy(new_rec)
        return html

    else:
        message = "Incorrect Submission ID or corresponding email. Please try again or contact: icmsa@utar.edu.my"
        raise HTTPException(status_code=400, detail=message)

