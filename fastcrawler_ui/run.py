import asyncio

from fastcrawler import FastCrawler

from fastcrawler_ui.core.fastapi.app import app
from fastcrawler_ui.core.fastapi.server import UvicornConfig, UvicornServer
from fastcrawler_ui.core.fastapi.sync import sync_crawler_to_fastapi


async def run_async(
    crawler: FastCrawler,
    server: UvicornServer | None = None,
    uvicorn_config: UvicornConfig | dict | None = None,
    fastapi_app=app,
):
    if uvicorn_config is None:
        uvicorn_config = UvicornConfig(app=fastapi_app)
    if isinstance(uvicorn_config, dict):
        uvicorn_config = UvicornConfig(app=fastapi_app, **uvicorn_config)

    if server is None:
        server = UvicornServer(
            config=UvicornConfig(**uvicorn_config.model_dump()).generate_config(),
        )

    server.crawler = crawler
    sync_crawler_to_fastapi(fastapi_app, crawler)
    api_task = asyncio.create_task(server.serve())
    crawler_task = asyncio.create_task(crawler.run())
    await asyncio.wait([crawler_task, api_task])


def run(
    crawler: FastCrawler,
    server: UvicornServer | None = None,
    uvicorn_config: UvicornConfig | dict | None = None,
    fastapi_app=app,
):
    asyncio.run(
        run_async(
            crawler=crawler,
            server=server,
            uvicorn_config=uvicorn_config,
            fastapi_app=fastapi_app,
        )
    )
