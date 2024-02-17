from pathlib import Path

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from .routers import get_routers


class ApplicationFactory:
    def __init__(self, router=get_routers(), base_app=FastAPI, dist_frontend=None):
        self.router = router
        self.base_app = base_app
        self.dist_frontend = (
            dist_frontend or Path(__file__).parent.parent.parent.parent / "frontend" / "dist"
        )

    def create_application(self) -> FastAPI:
        app = self.base_app()
        app.add_middleware(
            CORSMiddleware,
            allow_origins=["*"],
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        )
        app.include_router(self.router)
        app.mount("/", StaticFiles(directory=self.dist_frontend, html=True), name="static")
        return app


def create_app(factory=ApplicationFactory()) -> FastAPI:
    return factory.create_application()
