from fastapi.responses import StreamingResponse
from fastapi import APIRouter

import datetime
import asyncio
import random
import json


async def generate_random_log():
    while True:
        timestamp = datetime.datetime.utcnow().isoformat()
        level = random.choice(("INFO", "ERROR", "WARNING"))
        message = 'Lorem ipsum dolor sit amet, consectetur adipiscing elit'
        crawler_id = random.randint(10000, 99999)
        status = random.choice(("running", "stopped", "paused"))

        log = {
            "timestamp": timestamp,
            "level": level,
            "message": message,
            "crawler_id": crawler_id,
            "status": status
        }

        yield json.dumps({'data': log})
        await asyncio.sleep(0.5)


async def generate_random_chart():
    while True:
        all_requests = random.randint(0, 99)
        failed_requests = random.randint(0, 50)
        success_requests = all_requests - failed_requests
        data = {
            'data': {
                'time': datetime.datetime.utcnow().isoformat(),
                'all_requests': all_requests,
                'successful_requests': success_requests,
                'failed_requests': failed_requests
                }
            }
        yield json.dumps(data)
        await asyncio.sleep(0.5)


async def generate_random_crawler_data():
    all_crawlers = random.randint(0, 99)
    active_crawlers = random.randint(0, 50)
    deactive_crawlers = all_crawlers - active_crawlers
    while True:
        data = {
            'data': {
                'time': datetime.datetime.utcnow().isoformat(),
                'all_crawlers': all_crawlers,
                'deactive_crawlers': deactive_crawlers,
                'active_crawlers': active_crawlers
                }
            }
        yield json.dumps(data)
        await asyncio.sleep(0.5)


async def generate_random_crawlers_data():
    names = ('Digikala', 'DevTo', 'Medium')
    started_at = tuple(datetime.datetime.utcnow().isoformat() for i in range(3))
    durations = ('12:23', '11:55', '03:19')
    states = ['Active', 'Pause', 'Finished']
    while True:
        iterator = zip(names, started_at, durations, states)
        data = {
            'data': [{
                'name': d1,
                'started_at': d2,
                'duration': d3,
                'state': d4
                } for d1, d2, d3, d4 in iterator]
            }
        yield json.dumps(data)
        await asyncio.sleep(0.5)



router = APIRouter()

@router.get("/{crawler_uuid}/chart")
async def crawler_chart(crawler_uuid: str):
    return StreamingResponse(content=generate_random_chart(),
                             media_type='application/x-ndjson')


@router.get("/{crawler_uuid}/logs")
async def crawler_logs(crawler_uuid: str):
    return StreamingResponse(content=generate_random_log(),
                             media_type='application/x-ndjson')


@router.get("/dashboard/chart")
async def dashboard_chart():
    return StreamingResponse(content=generate_random_chart(),
                             media_type='application/x-ndjson')

@router.get("/dashboard/crawlers")
async def dashboard_crawlers():
    return StreamingResponse(content=generate_random_crawler_data(),
                             media_type='application/x-ndjson')

@router.get("/crawler/list")
async def crawler_list():
    return StreamingResponse(content=generate_random_crawlers_data(),
                             media_type='application/x-ndjson')

