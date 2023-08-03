import pytest
from fastcrawler import FastCrawler


@pytest.mark.asyncio
async def test_started_task(started_crawler: FastCrawler):
    # started_crawler.crawlers[0].spider.save()
    started_crawler.crawlers[0].spider


@pytest.mark.asyncio
async def test_stopted_task(stopted_crawler: FastCrawler):
    # stopted_crawler.crawlers[0].spider.save()
    stopted_crawler
