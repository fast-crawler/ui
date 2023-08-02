from fastcrawler import Depends, FastCrawler

from fastcrawler_ui.repository.spiders import CrawlerRepository


class CrawlerController:
    def __init__(self, crawler_repo: CrawlerRepository = Depends(CrawlerRepository)):
        self.crawler_repo = crawler_repo

    async def get_task(self, crawler: FastCrawler):
        results = await self.crawler_repo.get_tasks(crawler)
        return [result.model_dump() for result in results]


__all__ = [
    "CrawlerController",
]
