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