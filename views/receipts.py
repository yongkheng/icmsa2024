from starlette.requests import Request
from starlette.templating import Jinja2Templates
from models.models import Submission, Registration

templates = Jinja2Templates("templates")


def submit_receipt(request: Request, rec: Submission):
    return templates.TemplateResponse(
        "submit_receipt.html", {"request": request, "rec": rec}
    )


def submit_registration_receipt(request: Request, rec: Registration):
    return templates.TemplateResponse(
        "submit_registration_receipt.html", {"request": request, "rec": rec}
    )
