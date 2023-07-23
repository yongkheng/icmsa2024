from pathlib import Path
from datetime import datetime
from secrets import choice
from database.config import get_settings
from models import models
from fastapi import Depends, APIRouter, Request, BackgroundTasks
from database.database import SessionLocal, engine
from sqlalchemy.orm import Session

from views.receipts import submit_receipt

router = APIRouter()
models.Base.metadata.create_all(bind=engine)
settings = get_settings()

def uploadfile(fname, upload_filename):
    bt = fname.file.read()
    with open(f"{upload_filename}", "wb") as nf:
        nf.write(bt)


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


@router.post("/api/form_abstract")
async def form_abstract(
    request: Request, background_tasks: BackgroundTasks, db: Session = Depends(get_db)
):
    submission_type = "abstract"
    form = await request.form()
    form = dict(form)

    timestamp = datetime.now()
    submission_id = gen_id(db)
    db_dir = Path("../submit_db")
    submit_path = db_dir.joinpath(
        f"{timestamp.strftime('%Y%m%d_%H%M%S')}_{submission_id}"
    )
    submit_path.mkdir(parents=True, exist_ok=False)
    # print(submit_path)

    ts = timestamp.strftime("%Y-%m-%d_%H:%M:%S")
    ts1 = timestamp.strftime("%Y-%m-%d")
    file_ext = form["submission_pdf_file"].filename.split('.')[-1]
    filename = f"{submission_type}_{ts1}_{submission_id}.{file_ext}"
    file_path = submit_path.joinpath(filename)
    uploadfile(form["submission_pdf_file"], file_path)

    submission_rec = models.Submission(
        submission_id=submission_id,
        revision_version=0,
        timestamp=timestamp,
        corresponding_name=form["corresponding_name"],
        corresponding_email=form["corresponding_email"],
        submission_title=form["submission_title"],
        submission_keywords=form["submission_keywords"],
        submission_type="abstract",
        submission_filename=filename,
        submission_file_path=str(file_path),
    )
    db.add(submission_rec)
    db.commit()
    db.refresh(submission_rec)

    rec = (
        db.query(models.Submission)
        .filter(models.Submission.submission_id == submission_id)
        .first()
    )

    html = submit_receipt(request, rec)
    html_fname = submit_path.joinpath("receipt.html")
    print(html_fname)
    with open(html_fname, "wb") as f:
        f.write(html.body)

    print(file_path)
    return html
