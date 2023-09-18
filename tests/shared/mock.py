from fastcrawler import BaseModel, Spider


class Something(BaseModel):
    ...


class MockSpider(Spider):
    data_model = Something

    async def start(self, silent: bool = True):
        pass
