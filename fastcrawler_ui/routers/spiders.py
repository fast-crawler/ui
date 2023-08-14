from typing import Any, Type

from fastapi import APIRouter, Depends, status
from fastcrawler import FastCrawler
from fastcrawler.schedule.schema import Task
from pydantic import FieldValidationInfo, field_validator

from fastcrawler_ui.controllers.spider import SpiderController
from fastcrawler_ui.core.fastapi.depends import get_crawler
from fastcrawler_ui.repository.spiders import SpiderRepository, TaskSettings

spider_router = APIRouter()


def get_spider_repository():
    return SpiderRepository()


def spider_controller_cls() -> Type[SpiderController]:
    return SpiderController


class TaskJson(Task):
    @field_validator("start_cond", "end_cond")
    @classmethod
    def check_alphanumeric(cls, v: Any, info: FieldValidationInfo) -> bool | str | None:
        if v is not None:
            return str(v) if str(v).lower() != "false" else False
        return None


@spider_router.get("/all", response_model=list[TaskJson])
async def clients(
    crawler: FastCrawler = Depends(get_crawler),
    spider_repository: SpiderRepository = Depends(get_spider_repository),
    spider_controller: Type[SpiderController] = Depends(spider_controller_cls),
):
    """
    clients endpoint for retrieves crawler tasks.

    \f
    :param items: list of Task.
    """
    items = await spider_controller(spider_repository).get_tasks(crawler)
    return items


@spider_router.post("/stop_task", status_code=status.HTTP_204_NO_CONTENT)
async def stop_task(
    task_name: str,
    crawler: FastCrawler = Depends(get_crawler),
    spider_repository: SpiderRepository = Depends(get_spider_repository),
    spider_controller: Type[SpiderController] = Depends(spider_controller_cls),
):
    """
    stop_task endpoint for stops a crawler task.


    """
    await spider_controller(spider_repository).stop_task_by_name(crawler, task_name)


@spider_router.post("/start_task", status_code=status.HTTP_204_NO_CONTENT)
async def start_task(
    task_name: str,
    crawler: FastCrawler = Depends(get_crawler),
    spider_repository: SpiderRepository = Depends(get_spider_repository),
    spider_controller: Type[SpiderController] = Depends(spider_controller_cls),
):
    """
    start_task endpoint for starts a crawler task.


    """
    await spider_controller(spider_repository).start_task_by_name(crawler, task_name)


@spider_router.post("/toggle_task", status_code=status.HTTP_204_NO_CONTENT)
async def toggle_task(
    task_name: str,
    crawler: FastCrawler = Depends(get_crawler),
    spider_repository: SpiderRepository = Depends(get_spider_repository),
    spider_controller: Type[SpiderController] = Depends(spider_controller_cls),
):
    """
    toggle_task endpoint for toggle a crawler task (start/stop).


    """
    return await spider_controller(spider_repository).toggle_task_by_name(crawler, task_name)


@spider_router.post("/update_task", response_model=TaskJson, status_code=status.HTTP_200_OK)
async def update_task(
    task_name: str,
    task_settings: TaskSettings,
    crawler: FastCrawler = Depends(get_crawler),
    spider_repository: SpiderRepository = Depends(get_spider_repository),
    spider_controller: Type[SpiderController] = Depends(spider_controller_cls),
):
    """
    update_task endpoint for update a crawler task.


    """
    return await spider_controller(spider_repository).update_task_by_name(
        crawler, task_name, task_settings
    )
