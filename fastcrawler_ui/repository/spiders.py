import datetime
from typing import Any, Callable, Literal

from fastcrawler import BaseModel, Depends, FastCrawler
from fastcrawler.core import Process
from fastcrawler.schedule.schema import Task
from pydantic import Field


class Unset:
    """
    Unset Value class
    """

    pass


_UNSET = Unset()


class TaskSettings(BaseModel):
    name: str | Unset = Field(description="Name of the task. Must be unique", default=_UNSET)
    description: str | Unset = Field(
        description="Description of the task for documentation", default=_UNSET
    )
    logger_name: str | Unset = Field(
        description="Logger name to be used in logging the task record", default=_UNSET
    )
    execution: Literal["main", "async", "thread", "process"] | Unset = _UNSET
    priority: int | Unset = _UNSET
    disabled: bool | Unset = _UNSET
    force_run: bool | Unset = _UNSET
    status: Literal["run", "fail", "success", "terminate", "inaction", "crash"] | Unset = Field(
        description="Latest status of the task", default=_UNSET
    )
    timeout: datetime.timedelta | Unset = _UNSET
    start_cond: Any | Unset = _UNSET
    end_cond: Any | Unset = _UNSET

    model_config = {
        "arbitrary_types_allowed": True,
    }


class SpiderRepository:
    def __init__(self):
        """
        Initializes the SpiderRepository.
        """
        self.crawlers = set()

    def get_controller(self, crawler: FastCrawler):
        """Retrieves process controller from the crawler"""
        self.crawlers.add(crawler)
        assert crawler.controller is not None
        return crawler.controller

    async def get_tasks(self, crawler: FastCrawler):
        """Get all tasks from the crawler.

        Returns:
            list[Task]
        """
        controller = self.get_controller(crawler)
        return await controller.app.get_all_tasks()

    # async def add_task_to_crawler(self, crawler: FastCrawler, task_func: Callable, settings: Task):
    #     """Add a task to the crawler.

    #     Args:
    #         task_func (Callable): The task function
    #         settings (Task): The task settings

    #     Returns:
    #         None
    #     """
    #     controller = self.get_controller(crawler)
    #     await controller.add_task(task_func, settings)
    #     return None

    async def change_task_schedule_from_crawler(
        self, crawler: FastCrawler, task_name: str, schedule: str
    ) -> Task:
        """Change task schedule in the crawler.

        Args:
            task_name (str): The task name
            schedule (str): The task schedule string

        Returns:
            None
        """
        controller = self.get_controller(crawler)
        return await controller.change_task_schedule(task_name, schedule)

    async def toggle_task_from_crawler(self, crawler: FastCrawler, task_name: str) -> None:
        """Toggle task schedule in the crawler.

        Returns:
            None
        """
        controller = self.get_controller(crawler)
        await controller.toggle_task(task_name)
        return None

    async def update_task(
        self, crawler: FastCrawler, task_name: str, task_settings: TaskSettings
    ) -> Task | None:
        """Update a task by task name in the crawler.

        Args:
            task_name (str): The task name
            task_settings (TaskSettings): The task settings

        Returns:
            Task | None
        """
        self.get_controller(crawler)
        new_task_settings = task_settings.model_dump()
        result = await self.get_process_by_task_name(crawler, task_name)
        if result is not None:
            process, task = result
            for key, value in new_task_settings.items():
                if value is not _UNSET:
                    setattr(task, key, value)

            return task
        return None

    def get_tasks_in_processes(self, crawler: FastCrawler) -> dict[Process, Task]:
        """Get all tasks from the crawler.

        Returns:
            Dict[Process, Task]
        """
        controller = self.get_controller(crawler)
        session_tasks = controller.app.get_all_session_tasks()
        crawler_processes = crawler.crawlers

        processes = {
            process: task
            for process, task in zip(
                sorted(crawler_processes, key=lambda process: process.task.name),
                sorted(session_tasks, key=lambda task: task.name),
            )
        }
        return processes

    async def get_process_by_task_name(
        self, crawler: FastCrawler, task_name: str
    ) -> tuple[Process, Task] | None:
        """Get a process and task by task_name from the crawler.

        Returns:
            tuple[Process, Task] | None
        """
        self.crawlers.add(crawler)
        processes = self.get_tasks_in_processes(crawler=crawler)
        for process, task in processes.items():
            if task.name == task_name:
                return process, task
        return None
