from pathlib import Path

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from .routers import get_routers

dist_frontend = Path(__file__).parent.parent.parent.parent / "frontend" / "dist"

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
    app.mount("/", StaticFiles(directory=dist_frontend, html=True), name="static")
    return app


app = get_application()
