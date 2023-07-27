from fastapi import APIRouter

from fastcrawler_ui.routers import router


def get_routers() -> APIRouter:
    return router
