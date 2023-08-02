from typing import Any, Type

from fastapi import APIRouter, Depends
from fastcrawler import FastCrawler
from fastcrawler.schedule.schema import Task
from pydantic import FieldValidationInfo, field_validator

from fastcrawler_ui.controllers.spider import SpiderController
from fastcrawler_ui.core.fastapi.depends import get_crawler
from fastcrawler_ui.repository.spiders import SpiderRepository

router = APIRouter()


def get_spider_repository():
    return SpiderRepository()


def spider_controller_cls() -> Type[SpiderController]:
    return SpiderController


class TaskJson(Task):
    @field_validator("start_cond", "end_cond")
    @classmethod
    def check_alphanumeric(cls, v: Any, info: FieldValidationInfo) -> str:
        if v is not None:
            return str(v) if str(v).lower() != "false" else False


@router.get("/all", response_model=list[TaskJson])
async def clients(
    crawler: FastCrawler = Depends(get_crawler),
    spider_repository: SpiderRepository = Depends(get_spider_repository),
    controller: Type[SpiderController] = Depends(spider_controller_cls),
):
    """
    clients endpoint for retrieves crawler tasks.

    \f
    :param items: list of Task.
    """
    items = await controller(spider_repository).get_task(crawler)
    return items
