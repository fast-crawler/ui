import asyncio
from typing import Any, Type

from fastapi import APIRouter, Body, Depends, status
from fastcrawler import FastCrawler
from fastcrawler.schedule.schema import Task
from pydantic import BaseModel, FieldValidationInfo, field_validator

from fastcrawler_ui.controllers.spider import SpiderController
from fastcrawler_ui.core.fastapi.depends import get_crawler
from fastcrawler_ui.repository.spiders import SpiderRepository, TaskSettings

spider_router = APIRouter()


def get_spider_repository():
    return SpiderRepository()


def spider_controller_cls() -> Type[SpiderController]:
    return SpiderController


class TaskInput(BaseModel):
    name: str


class TasksInput(BaseModel):
    names: list[str]


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
    The /all endpoint is used to retrieve crawler tasks.

    \f
    :param items: list of Task.
    """
    items = await spider_controller(spider_repository).get_tasks(crawler)
    return items


def manage_tasks(
    task_names: TasksInput,
    crawler: FastCrawler,
    spider_repository: SpiderRepository,
    spider_controller: Type[SpiderController],
    action: str,
):
    controller = spider_controller(spider_repository)
    action_call = getattr(controller, f"{action}_task_by_name")

    tasks = [action_call(crawler, task_name) for task_name in task_names.names]

    return asyncio.gather(*tasks)


@spider_router.post("/start_tasks", status_code=status.HTTP_204_NO_CONTENT)
async def start_tasks(
    task_names: TasksInput = Body(),
    crawler: FastCrawler = Depends(get_crawler),
    spider_repository: SpiderRepository = Depends(get_spider_repository),
    spider_controller: Type[SpiderController] = Depends(spider_controller_cls),
):
    """
    The /start_tasks endpoint is used to start a crawler task.
    """
    await manage_tasks(task_names, crawler, spider_repository, spider_controller, action="start")


@spider_router.post("/stop_tasks", status_code=status.HTTP_204_NO_CONTENT)
async def stop_tasks(
    task_names: TasksInput = Body(),
    crawler: FastCrawler = Depends(get_crawler),
    spider_repository: SpiderRepository = Depends(get_spider_repository),
    spider_controller: Type[SpiderController] = Depends(spider_controller_cls),
):
    """
    The /stop_tasks endpoint is used to stop a crawler task.
    """
    await manage_tasks(task_names, crawler, spider_repository, spider_controller, action="stop")


@spider_router.post("/toggle_task", status_code=status.HTTP_204_NO_CONTENT)
async def toggle_task(
    task: TaskInput = Body(),
    crawler: FastCrawler = Depends(get_crawler),
    spider_repository: SpiderRepository = Depends(get_spider_repository),
    spider_controller: Type[SpiderController] = Depends(spider_controller_cls),
):
    """
    The /toggle_task endpoint is used to toggle a crawler task (start/stop).


    """
    return await spider_controller(spider_repository).toggle_task_by_name(crawler, task.name)


class TaskSettingInput(BaseModel):
    settings: TaskSettings
    name: str


@spider_router.post("/update_task", response_model=TaskJson, status_code=status.HTTP_200_OK)
async def update_task(
    task: TaskSettingInput = Body(),
    crawler: FastCrawler = Depends(get_crawler),
    spider_repository: SpiderRepository = Depends(get_spider_repository),
    spider_controller: Type[SpiderController] = Depends(spider_controller_cls),
):
    """
    The /update_task endpoint is used to update a crawler task.


    """
    return await spider_controller(spider_repository).update_task_by_name(
        crawler, task.name, task.settings
    )


class TaskScheduleInput(BaseModel):
    name: str
    schedule: str


@spider_router.post("/change_task_schedule", status_code=status.HTTP_204_NO_CONTENT)
async def change_task_schedule(
    task: TaskScheduleInput = Body(),
    crawler: FastCrawler = Depends(get_crawler),
    spider_repository: SpiderRepository = Depends(get_spider_repository),
    spider_controller: Type[SpiderController] = Depends(spider_controller_cls),
):
    """
    The /change_task_schedule endpoint is used to change the schedule of a crawler task.


    """
    await spider_controller(spider_repository).change_task_schedule(
        crawler, task.name, task.schedule
    )
    await spider_controller(spider_repository).get_task(crawler, task_name=task.name)
