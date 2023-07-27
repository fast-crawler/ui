from fastapi import APIRouter, Depends
from fastcrawler import FastCrawler

from fastcrawler_ui.core.fastapi.depends import get_crawler

router = APIRouter()


@router.get("/all")
async def clients(crawler: FastCrawler = Depends(get_crawler)):
    results = await crawler.controller.all()
    return [result.model_dump() for result in results]
