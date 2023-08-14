from fastapi import HTTPException, status
from fastcrawler import Depends, FastCrawler
from fastcrawler.schedule.schema import Task

from fastcrawler_ui.repository.spiders import SpiderRepository, TaskSettings


class SpiderController:
    def __init__(self, spider_repo: SpiderRepository = Depends(SpiderRepository)):
        self.spider_repo = spider_repo

    async def get_tasks(self, crawler: FastCrawler):
        results = await self.spider_repo.get_tasks(crawler)
        return [result.model_dump() for result in results]

    async def get_process_by_task(self, crawler: FastCrawler, task_name: str):
        results = await self.spider_repo.get_tasks_in_processes(crawler)
        for process, task in results.items():
            if task.name == task_name:
                return process
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Task {task_name!r} not found",
        )

    async def start_task_by_name(self, crawler: FastCrawler, task_name: str):
        process = await self.get_process_by_task(
            crawler=crawler,
            task_name=task_name,
        )
        await process.start()

    async def stop_task_by_name(self, crawler: FastCrawler, task_name: str):
        task = await self.get_process_by_task(
            crawler=crawler,
            task_name=task_name,
        )
        await task.stop()

    async def update_task_by_name(
        self, crawler: FastCrawler, task_name: str, settings: TaskSettings
    ) -> Task | None:
        return await self.spider_repo.update_task(
            crawler=crawler,
            task_name=task_name,
            task_settings=settings,
        )

    async def toggle_task_by_name(self, crawler: FastCrawler, task_name: str) -> Task | None:
        await self.spider_repo.toggle_task_from_crawler(
            crawler=crawler,
            task_name=task_name,
        )
        return None
