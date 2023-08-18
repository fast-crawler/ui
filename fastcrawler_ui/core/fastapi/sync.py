from fastapi import FastAPI
from fastcrawler import FastCrawler

from .depends import get_crawler


def sync_crawler_to_fastapi(fastapi: FastAPI, crawler: FastCrawler):
    fastapi.dependency_overrides[get_crawler] = lambda: crawler
