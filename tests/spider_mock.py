from fastcrawler import Spider


class MockSpider(Spider):
    async def start(self, silent: bool = True):
        pass
