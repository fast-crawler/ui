from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .routers import get_routers


def get_application(router=get_routers(), base_app=FastAPI) -> FastAPI:
    app = base_app()
    origins = ["*"]
    app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    app.include_router(router)
    return app


app = get_application()
