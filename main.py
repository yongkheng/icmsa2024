import fastapi
import uvicorn
from starlette.staticfiles import StaticFiles

# from api import form_submit, form_revise, form_rebuttal, submit_db, send_mail
from views import index, submit, admin
from api import utils, form_abstract, form_fullpaper, form_manuscript, form_registration

api = fastapi.FastAPI()


def configure():
    api.mount("/static", StaticFiles(directory="static"), name="static")

    api.include_router(index.router)
    api.include_router(submit.router)
    api.include_router(utils.router)
    api.include_router(form_abstract.router)
    api.include_router(form_fullpaper.router)
    api.include_router(form_manuscript.router)
    api.include_router(form_registration.router)
    api.include_router(admin.router)


if __name__ == "__main__":
    configure()
    uvicorn.run("main:api", port=8000, host="127.0.0.1", reload=True)
else:
    configure()
