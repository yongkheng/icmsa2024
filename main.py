import fastapi
import uvicorn
from starlette.staticfiles import StaticFiles

# from api import form_submit, form_revise, form_rebuttal, submit_db, send_mail
from views import index, submit, admin
from api import form_abstract

api = fastapi.FastAPI()


def configure():
    api.mount("/static", StaticFiles(directory="static"), name="static")

    # api.include_router(form_revise.router)
    # api.include_router(form_rebuttal.router)
    # api.include_router(submit_db.router)
    # api.include_router(send_mail.router)
    #
    api.include_router(index.router)
    api.include_router(submit.router)
    api.include_router(form_abstract.router)
    api.include_router(admin.router)

if __name__ == "__main__":
    configure()
    uvicorn.run("main:api", port=8000, host="127.0.0.1", reload=True)
else:
    configure()
