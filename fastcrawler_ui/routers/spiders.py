from fastapi import APIRouter, Depends
from fastcrawler import FastCrawler
from fastcrawler.schedule.schema import Task

from fastcrawler_ui.controllers.spider import CrawlerController
from fastcrawler_ui.core.fastapi.depends import get_crawler
from fastcrawler_ui.repository.spiders import CrawlerRepository

router = APIRouter()
crawler_repository = CrawlerRepository()

# @router.get("/all")
# async def clients(crawler: FastCrawler = Depends(get_crawler)):
#     results = await crawler.controller.all()
#     return [result.model_dump() for result in results]


@router.get("/all", response_model=list[Task])
async def clients(crawler: FastCrawler = Depends(get_crawler)):
    """
    clients endpoint for retrieves crawler tasks.

    \f
    :param items: list of Task.
    """
    items = await CrawlerController(crawler_repository).get_task(crawler)
    return items
