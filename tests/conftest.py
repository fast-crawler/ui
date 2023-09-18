# pylint: skip-file
import asyncio
from typing import AsyncGenerator, Generator
from unittest.mock import AsyncMock

import pytest
import pytest_asyncio
from fastapi.testclient import TestClient
from fastcrawler import BaseModel, FastCrawler, Process, XPATHField

from fastcrawler_ui.core.fastapi.app import app
from fastcrawler_ui.core.fastapi.sync import sync_crawler_to_fastapi
from fastcrawler_ui.repository.ws import ConnectionRepository
from tests.shared.mock import MockSpider

started_crawler_flag = False

stopped_crawler_flag = 0

total_crawled = 0


@pytest.fixture(scope="session")
def event_loop():
    policy = asyncio.get_event_loop_policy()
    loop = policy.new_event_loop()
    yield loop
    loop.close()


class PersonData(BaseModel):
    name: str = XPATHField(query="//td[1]", extract="text")
    age: int = XPATHField(query="//td[2]", extract="text")


class PersonPage(BaseModel):
    person: list[PersonData] = XPATHField(query="//table//tr", many=True)


async def get_urls():
    return {f"http://localhost:8000/persons/{id}" for id in range(20)}


def get_fastcrawler() -> FastCrawler:
    crawler = FastCrawler(
        crawlers=[
            Process(
                spider=MockSpider(),
                cond="every 1 minute",
            ),
            Process(
                spider=MockSpider(),
                cond="every 3 minute",
            ),
            Process(
                spider=MockSpider(),
                cond="every 5 minute",
            ),
        ],
    )
    return crawler


@pytest_asyncio.fixture(scope="session", autouse=True)
async def client() -> AsyncGenerator[TestClient, None]:
    crawler = get_fastcrawler()
    sync_crawler_to_fastapi(app, crawler)
    client = TestClient(app)
    task = asyncio.create_task(crawler.run())
    yield client
    task.cancel()
    await asyncio.gather(task, return_exceptions=True)


@pytest.fixture(autouse=True)
def manager() -> Generator[ConnectionRepository, None, None]:
    yield ConnectionRepository()


@pytest.fixture(autouse=True)
def websocket() -> Generator[AsyncMock, None, None]:
    yield AsyncMock()
