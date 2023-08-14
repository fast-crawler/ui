from typing import Callable, Literal, Any
import datetime

from pydantic import Field
from fastcrawler import Depends, FastCrawler, BaseModel
from fastcrawler.schedule.schema import Task
from fastcrawler.core import Process


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
        return crawler.controller

    async def get_tasks(self, crawler: FastCrawler):
        """Get all tasks from the crawler.

        Returns:
            list[Task]
        """
        self.crawlers.add(crawler)
        return await crawler.controller.app.get_all_tasks()

    async def add_task_to_crawler(self, crawler: FastCrawler, task_func: Callable, settings: Task):
        """Add a task to the crawler.

        Args:
            task_func (Callable): The task function
            settings (Task): The task settings

        Returns:
            None
        """
        self.crawlers.add(crawler)
        await crawler.controller.add_task(task_func, settings)
        return None

    async def change_task_schedule_from_crawler(
        self, crawler: FastCrawler, task_name: str, schedule: str
    ) -> None:
        """Change task schedule in the crawler.

        Args:
            task_name (str): The task name
            schedule (str): The task schedule string

        Returns:
            None
        """
        self.crawlers.add(crawler)
        await crawler.controller.change_task_schedule(task_name, schedule)
        return None

    async def toggle_task_from_crawler(self, crawler: FastCrawler, task_name: str) -> None:
        """Toggle task schedule in the crawler.

        Returns:
            None
        """
        self.crawlers.add(crawler)
        await crawler.controller.toggle_task(task_name)
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
        self.crawlers.add(crawler)
        new_task_settings = task_settings.model_dump()
        task = await self.get_task_by_name(crawler, task_name)
        if task:
            new_task: Task = task
            for key, value in new_task_settings.items():
                if value is not _UNSET:
                    setattr(new_task, key, value)

            return new_task
        return None

    async def get_tasks_in_processes(self, crawler: FastCrawler) -> dict[Process, Task]:
        """Get all tasks from the crawler.

        Returns:
            Dict[Process, Task]
        """
        self.crawlers.add(crawler)
        processes = {process: process.task for process in crawler.crawlers}
        return processes

    async def get_task_by_name(self, crawler: FastCrawler, task_name: str) -> Task | None:
        """Get task by task_name from the crawler.

        Returns:
            Task | None
        """
        self.crawlers.add(crawler)
        tasks = [
            task
            for task in (await self.get_tasks_in_processes(crawler=crawler)).values()
            if task.name == task_name
        ]
        if len(tasks) > 0:
            assert len(tasks) == 1, f"There is more than one task by task_name: {task_name}"
            return tasks[0]
        return None
