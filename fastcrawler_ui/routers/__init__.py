from fastapi import APIRouter

from .spiders import spider_router
from .ws import router as ws_router
from .sse import router as sse_router

router = APIRouter()
router.include_router(ws_router)
router.include_router(spider_router)
router.include_router(sse_router)
