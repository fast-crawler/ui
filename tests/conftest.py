# pylint: skip-file
import os
import sys
import asyncio
import pytest_asyncio

from fastcrawler.engine.contracts import RequestCycle
from fastcrawler import (
    BaseModel,
    Depends,
    FastCrawler as _FastCrawler,
    Process,
    Spider,
    XPATHField,
)


sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from fastapi.testclient import TestClient
from fastcrawler_ui.core.fastapi.app import app
from fastcrawler_ui.core.fastapi.sync import sync_crawler_to_fastapi

started_crawler_flag = False

stopped_crawler_flag = 0

total_crawled = 0


class FastCrawler(_FastCrawler):
    async def run2(self) -> None:
        """Prepare all crawlers in background explicitly with schedule without serving"""
        for crawler in self.crawlers:
            crawler.controller = self.controller
            await crawler.add_spiders()
        return None


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


class MySpiderStopped(Spider):
    engine_request_limit = 5
    data_model = PersonPage
    start_url = Depends(get_urls)

    async def save_cycle(self, all_data: list[RequestCycle]) -> None:
        global stopped_crawler_flag
        stopped_crawler_flag += 1
        return await super().save_cycle(all_data)

    async def save(self, all_data: list[PersonPage]):
        global stopped_crawler_flag
        assert all_data is not None
        assert len(all_data) == 10
        assert stopped_crawler_flag == 1


class MySpider(Spider):
    engine_request_limit = 10
    data_model = PersonPage
    start_url = Depends(get_urls)

    async def save(self, all_data: list[PersonPage]):
        assert all_data is not None
        assert len(all_data) == 10
        global total_crawled
        total_crawled += 1


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


def get_stopped_fastcrawler():
    crawler = FastCrawler(
        crawlers=[
            Process(
                spider=MySpiderStopped(),
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
async def stopped_crawler():
    crawler = get_stopped_fastcrawler()
    # await run_async(crawler=crawler, uvicorn_config={"port": 8001})
    for process in crawler.crawlers:
        await process.stop()
    return crawler


def get_fastcrawler():
    crawler = FastCrawler(
        crawlers=Process(
            spider=MySpider(),
            cond="every 1 minute",
        )
    )
    return crawler


@pytest_asyncio.fixture(scope="session")
def client():
    crawler = get_fastcrawler()
    sync_crawler_to_fastapi(app, crawler)
    client = TestClient(app)
    asyncio.run(crawler.run2())
    
    yield client
