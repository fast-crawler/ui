from typing import Any

from fastcrawler import Depends, FastCrawler

from fastcrawler_ui.repository.spiders import CrawlerRepository
from rocketry.conditions.task import BaseComparable as TaskBase
from rocketry.core.condition import BaseCondition


class CrawlerController:
    def __init__(self, crawler_repo: CrawlerRepository = Depends(CrawlerRepository)):
        self.crawler_repo = crawler_repo

    @staticmethod
    def _serialize_task(task: dict[str, Any]):
        def rocketry_serializer(value):
            if isinstance(value, TaskBase):
                return str(value)
            if isinstance(value, BaseCondition):
                return value.observe()

        res = {
            k: (rocketry_serializer(v) if isinstance(v, (TaskBase, BaseCondition)) else v)
            for k, v in task.items()
        }

        return res

    async def get_task(self, crawler: FastCrawler):
        results = await self.crawler_repo.get_tasks(crawler)
        return [self._serialize_task(result.model_dump()) for result in results]


__all__ = [
    "CrawlerController",
]
