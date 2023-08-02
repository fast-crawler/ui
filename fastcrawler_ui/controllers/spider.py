from fastcrawler import Depends, FastCrawler

from fastcrawler_ui.repository.spiders import SpiderRepository


class SpiderController:
    def __init__(self, crawler_repo: SpiderRepository = Depends(SpiderRepository)):
        self.crawler_repo = crawler_repo

    async def get_task(self, crawler: FastCrawler):
        results = await self.crawler_repo.get_tasks(crawler)
        return [result.model_dump() for result in results]
