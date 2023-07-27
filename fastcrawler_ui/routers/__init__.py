from fastapi import APIRouter

from .spiders import router as spiders_router
from .ws import router as ws_router

router = APIRouter()
router.include_router(ws_router)
router.include_router(spiders_router)
