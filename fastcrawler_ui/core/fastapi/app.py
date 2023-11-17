from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from .routers import get_routers


def get_application(router=get_routers(), base_app=FastAPI) -> FastAPI:
    app = base_app()
    app.include_router(router)
    app.mount("/", StaticFiles(directory="frontend/dist", html=True), name="static")
    return app


app = get_application()
