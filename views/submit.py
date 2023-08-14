from fastapi import APIRouter
from starlette.requests import Request
from starlette.templating import Jinja2Templates

router = APIRouter()
templates = Jinja2Templates("templates")


@router.get("/submission")
def submission(request: Request):
    return templates.TemplateResponse("submission.html", {"request": request})


@router.get("/submit_abstract")
def submit_abstract(request: Request):
    return templates.TemplateResponse("submit_abstract.html", {"request": request})


@router.get("/submit_fullpaper")
def submit_abstract(request: Request):
    return templates.TemplateResponse("submit_fullpaper.html", {"request": request})


@router.get("/submit_manuscript")
def submit_abstract(request: Request):
    return templates.TemplateResponse("submit_manuscript.html", {"request": request})


@router.get("/submit_registration")
def submit_abstract(request: Request):
    return templates.TemplateResponse("submit_registration.html", {"request": request})