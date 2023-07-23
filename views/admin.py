from starlette.requests import Request
from starlette.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from database.database import SessionLocal
from models import models


templates = Jinja2Templates("templates")

router = APIRouter()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get("/admin", response_class=HTMLResponse)
def query(request: Request):
    return templates.TemplateResponse("admin.html", {"request": request})


@router.get("/admin/summary", response_class=HTMLResponse)
def query(request: Request, db: Session = Depends(get_db)):
    responses = db.query(models.Submission).all()
    return templates.TemplateResponse(
        "submission_listing.html", {"request": request, "items": responses}
    )
