from typing import Any

from fastapi import APIRouter, Depends
from fastcrawler import FastCrawler
from fastcrawler.schedule.schema import Task
from pydantic import FieldValidationInfo, field_validator

from fastcrawler_ui.controllers.spider import CrawlerController
from fastcrawler_ui.core.fastapi.depends import get_crawler
from fastcrawler_ui.repository.spiders import CrawlerRepository

router = APIRouter()
crawler_repository = CrawlerRepository()


class TaskJson(Task):
    @field_validator("start_cond", "end_cond")
    @classmethod
    def check_alphanumeric(cls, v: Any, info: FieldValidationInfo) -> str:
        if v is not None:
            return str(v) if str(v).lower() != "false" else False


@router.get("/all", response_model=list[TaskJson])
async def clients(crawler: FastCrawler = Depends(get_crawler)):
    """
    clients endpoint for retrieves crawler tasks.

    \f
    :param items: list of Task.
    """
    items = await CrawlerController(crawler_repository).get_task(crawler)
    return items
