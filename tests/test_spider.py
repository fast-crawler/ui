import os
import sys
import asyncio

import pytest
from fastapi.testclient import TestClient

sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from fastcrawler_ui.core.fastapi.app import app
from fastcrawler_ui.core.fastapi.sync import sync_crawler_to_fastapi
from .conftest import get_fastcrawler


crawler = get_fastcrawler()

sync_crawler_to_fastapi(app, crawler)

client = TestClient(app)

asyncio.run(crawler.run2())


def test_all():
    response = client.get("/all")
    print(response)
    content = response.json()
    assert response.status_code == 200
    assert len(content) == 1
    assert len(content[0]) == 11
    assert content[0]["name"].startswith("MySpider")
