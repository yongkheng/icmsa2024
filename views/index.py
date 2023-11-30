from fastapi import APIRouter
from starlette.requests import Request
from starlette.templating import Jinja2Templates

router = APIRouter()
templates = Jinja2Templates("templates")


@router.get("/")
def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@router.get("/committee")
def committee(request: Request):
    return templates.TemplateResponse("committee.html", {"request": request})


@router.get("/speakers")
def speakers(request: Request):
    return templates.TemplateResponse("speakers.html", {"request": request})


@router.get("/programme")
def programme(request: Request):
    return templates.TemplateResponse("programme.html", {"request": request})


@router.get("/registration")
def registration(request: Request):
    return templates.TemplateResponse("registration.html", {"request": request})

@router.get("/sponsors")
def sponsors(request: Request):
    return templates.TemplateResponse("sponsors.html", {"request": request})
