from typing import Callable

from fastcrawler import Depends, FastCrawler
from fastcrawler.schedule.schema import Task
from fastcrawler.core import Process


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

    async def add_task_to_crawler(
        self, crawler: FastCrawler, task_func: Callable, settings: Task
    ):
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

    async def toggle_task_from_crawler(
        self, crawler: FastCrawler, task_name: str
    ) -> None:
        """Toggle task schedule in the crawler.

        Returns:
            None
        """
        self.crawlers.add(crawler)
        await crawler.controller.toggle_task(task_name)
        return None

    async def get_tasks_in_processes(self, crawler: FastCrawler) -> dict[Process, Task]:
        """Get all tasks from the crawler.

        Returns:
            Dict[Process, Task]
        """
        self.crawlers.add(crawler)
        processes = {process: process.task for process in crawler.crawlers}
        return processes
