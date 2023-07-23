from fastapi import APIRouter
from starlette.requests import Request
from starlette.templating import Jinja2Templates

router = APIRouter()
templates = Jinja2Templates("templates")


@router.get("/")
def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})
