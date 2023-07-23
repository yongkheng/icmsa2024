from pathlib import Path
from datetime import datetime
from secrets import choice
from database.config import get_settings
from models import models
from fastapi import Depends, APIRouter, Request, BackgroundTasks, Response
from fastapi.responses import HTMLResponse
from database.database import SessionLocal, engine
from sqlalchemy.orm import Session

from views.receipts import submit_receipt

router = APIRouter()
models.Base.metadata.create_all(bind=engine)
settings = get_settings()


def gen_id(db):
    chars = "ABCDEFGHJKLMNPQRSTUVWXYZ23456789"
    uid = "".join(choice(chars) for _ in range(5))
    while True:
        rec = (
            db.query(models.Submission)
            .filter(models.Submission.submission_id == uid)
            .first()
        )
        if not rec:
            break
        else:
            uid = "".join(choice(chars) for _ in range(5))
    return uid


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def make_local_copy(rec: models.Submission):
    print(rec.abstract_filename)
    with open(f"submit_db/files/{rec.abstract_filename}", "wb") as f_handle:
        f_handle.write(rec.abstract_content)
    with open(f"submit_db/files/{rec.abstract_filename}.receipt.html", 'wb') as f_handle:
        f_handle.write(rec.abstract_receipt)


@router.post("/api/form_abstract")
async def form_abstract(request: Request, background_tasks: BackgroundTasks, db: Session = Depends(get_db)):
    submission_type = "abstract"
    form = await request.form()
    form = dict(form)

    timestamp = datetime.now()
    submission_id = gen_id(db)
    rev_no = 0

    ts1 = timestamp.strftime("%Y-%m-%d")
    file_ext = form["submission_pdf_file"].filename.split('.')[-1]
    filename = f"{submission_type}_{ts1}_{submission_id}_rev{rev_no}.{file_ext}"
    file_content = form["submission_pdf_file"].file.read()

    submission_rec = models.Submission(
        submission_id=submission_id,
        revision_version=rev_no,
        timestamp=timestamp,
        corresponding_name=form["corresponding_name"],
        corresponding_email=form["corresponding_email"],
        submission_title=form["submission_title"],
        submission_keywords=form["submission_keywords"],
        submission_type="abstract",
        submission_filename=filename,
        abstract_filename=filename,
        abstract_content=file_content,
        abstract_receipt=None,
        in_proceedings=form['in_proceedings'],
        in_journal=form['in_journal'],

        fullpaper_filename="",
        fullpaper_content=None,
        fullpaper_receipt=None,
        camera_ready_filename="",
        camera_ready_content=None,
        camera_ready_receipt=None
    )
    html = submit_receipt(request, submission_rec)
    print(type(html))
    with open("receipt.html",'wb') as f:
        f.write(html.body)
    submission_rec.abstract_receipt = html.body

    db.add(submission_rec)
    db.commit()
    db.refresh(submission_rec)

    make_local_copy(submission_rec)
    return html


@router.get("/api/get_file")
async def get_abstract_file(
        fname, request: Request, background_tasks: BackgroundTasks, db: Session = Depends(get_db),
):
    print(f"get_abstract_file(): {fname=}")
    rec = (
        db.query(models.Submission)
        .filter(models.Submission.submission_filename == fname)
        .first()
    )

    # Set the appropriate response headers for file download
    response = Response(content=rec.abstract_content, media_type="application/octet-stream")
    response.headers["Content-Disposition"] = f"attachment; filename={rec.abstract_filename}"

    return response


@router.get("/api/get_receipt")
async def get_abstract_file(
        fname, request: Request, background_tasks: BackgroundTasks, db: Session = Depends(get_db),
):
    print(f"get_abstract_file(): {fname=}")
    rec = (
        db.query(models.Submission)
        .filter(models.Submission.submission_filename == fname)
        .first()
    )

    html = 'unknown'
    if rec.submission_type == "abstract":
        html = rec.abstract_receipt

    return HTMLResponse(content=html, status_code=200)
#    return response