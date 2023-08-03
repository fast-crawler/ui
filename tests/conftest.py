# pylint: skip-file

import pytest_asyncio

from fastcrawler.engine.contracts import RequestCycle
from fastcrawler import BaseModel, Depends, FastCrawler, Process, Spider, XPATHField

from fastcrawler_ui import run_async

started_crawler_flag = False

stopted_crawler_flag = 0


class PersonData(BaseModel):
    name: str = XPATHField(query="//td[1]", extract="text")
    age: int = XPATHField(query="//td[2]", extract="text")


class PersonPage(BaseModel):
    person: list[PersonData] = XPATHField(query="//table//tr", many=True)


async def get_urls():
    return {f"http://localhost:8000/persons/{id}" for id in range(20)}


class MySpiderStarted(Spider):
    engine_request_limit = 10
    data_model = PersonPage
    start_url = Depends(get_urls)

    async def save_cycle(self, all_data: list[RequestCycle]) -> None:
        global started_crawler_flag
        started_crawler_flag = True
        return await super().save_cycle(all_data)

    async def save(self, all_data: list[PersonPage]):
        global started_crawler_flag
        assert all_data is not None
        assert len(all_data) == 10
        assert started_crawler_flag == True


class MySpiderStoped(Spider):
    engine_request_limit = 5
    data_model = PersonPage
    start_url = Depends(get_urls)

    async def save_cycle(self, all_data: list[RequestCycle]) -> None:
        global stopted_crawler_flag
        stopted_crawler_flag += 1
        return await super().save_cycle(all_data)

    async def save(self, all_data: list[PersonPage]):
        global stopted_crawler_flag
        assert all_data is not None
        assert len(all_data) == 10
        assert stopted_crawler_flag == 1


def get_started_fastcrawler():
    crawler = FastCrawler(
        crawlers=[
            Process(
                spider=MySpiderStarted(),
                cond="every 2 minute",
            ),
        ]
    )
    return crawler


def get_stopted_fastcrawler():
    crawler = FastCrawler(
        crawlers=[
            Process(
                spider=MySpiderStoped(),
                cond="every 5 minute",
            ),
        ]
    )
    return crawler


@pytest_asyncio.fixture(scope="function")
async def started_crawler():
    crawler = get_started_fastcrawler()
    # await run_async(crawler=crawler, uvicorn_config={"port": 8001})
    return crawler


@pytest_asyncio.fixture(scope="function")
async def stopted_crawler():
    crawler = get_stopted_fastcrawler()
    # await run_async(crawler=crawler, uvicorn_config={"port": 8001})
    for process in crawler.crawlers:
        await process.stop()
    return crawler
