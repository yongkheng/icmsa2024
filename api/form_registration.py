from datetime import datetime

from database.config import get_settings
from models import models
from fastapi import Depends, APIRouter, Request, BackgroundTasks, HTTPException
from database.database import SessionLocal, engine
from sqlalchemy.orm import Session

from views.receipts import submit_registration_receipt

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
    with open(f"submit_db/files/{rec.payment_proof_filename}", "wb") as f_handle:
        f_handle.write(rec.payment_proof_content)
    with open(f"submit_db/files/{rec.student_status_proof_filename}.receipt.html", 'wb') as f_handle:
        f_handle.write(rec.student_status_proof_content)
    with open(f"submit_db/files/{rec.first_name}_{rec.last_name}_{rec.timestamp.date()}.receipt.html", 'wb') as f_handle:
        f_handle.write(rec.registration_receipt_content)


@router.post("/api/form_registration")
async def form_registration(request: Request, background_tasks: BackgroundTasks, db: Session = Depends(get_db)):
    form = await request.form()
    form = dict(form)

    # check submitted file types
    file_ext = form["submission_payment_file"].filename.split('.')[-1]
    if file_ext.lower() not in ['pdf']:
        message = "Please submit you proof of payment in pdf format only."
        raise HTTPException(status_code=400, detail=message)
    if form["submission_student_status_file"].filename:
        # check only if there is attachment
        file_ext = form["submission_student_status_file"].filename.split('.')[-1]
        if file_ext.lower() not in ['pdf']:
            message = "Please submit you proof of student status in pdf format only."
            raise HTTPException(status_code=400, detail=message)


    rec = models.Registration(
            timestamp=datetime.now(),
            first_name = form['first_name'],
            last_name = form['last_name'],
            affiliation = form['affiliation'],
            email = form['corresponding_email'],
            phone = form['phone'],
            submission_id=form['submission_id'],

            participant_type=form['participant_type'],
            join_dinner=form['join_dinner'],
            diet_allergic=form['diet_allergic'],
            additional_dinner_ticket=form['additional_dinner_ticket'],

            payment_proof_filename = form["submission_payment_file"].filename,
            payment_proof_content = form["submission_payment_file"].file.read(),

            student_status_proof_filename = form["submission_student_status_file"].filename,
            student_status_proof_content = form["submission_student_status_file"].file.read(),

            registration_receipt_content = None,
            )

    # generate receipt
    html = submit_registration_receipt(request, rec)
    with open("receipt.html", 'wb') as f:
        f.write(html.body)
    rec.registration_receipt_content = html.body

    # save to database
    db.add(rec)
    db.commit()
    db.refresh(rec)

    # generate a local copy in case of corrupted database
    make_local_copy(rec)

    return html
