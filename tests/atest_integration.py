import sys

sys.path.append("../")

from fastcrawler import BaseModel, Depends, FastCrawler, Process, Spider, XPATHField

from fastcrawler_ui import run

total_crawled = 0


class PersonData(BaseModel):
    name: str = XPATHField(query="//td[1]", extract="text")
    age: int = XPATHField(query="//td[2]", extract="text")


class PersonPage(BaseModel):
    person: list[PersonData] = XPATHField(query="//table//tr", many=True)


async def get_urls():
    return {f"http://localhost:8000/persons/{id}" for id in range(20)}


class MySpider(Spider):
    engine_request_limit = 10
    data_model = PersonPage
    start_url = Depends(get_urls)

    async def save(self, all_data: list[PersonPage]):
        assert all_data is not None
        assert len(all_data) == 10
        global total_crawled
        total_crawled += 1


crawler = app = FastCrawler(
    crawlers=(
        Process(
        spider=MySpider(),
        cond="every 1 minute",
        ),
        Process(
        spider=MySpider(),
        cond="every 3 minute",
        ),
        Process(
        spider=MySpider(),
        cond="every 5 minute",
        ),
    )
)

run(crawler=crawler, uvicorn_config={"port": 8001})
