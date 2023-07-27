from fastapi import FastAPI

from .routers import get_routers


def get_application(router=get_routers(), base_app=FastAPI) -> FastAPI:
    app = base_app()
    app.include_router(router)
    return app


app = get_application()
