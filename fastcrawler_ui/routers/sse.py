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


async def generate_random_crawlers_data():
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



router = APIRouter()

@router.get("/{crawler_uuid}/chart")
async def crawler_chart(crawler_id: int):
    return StreamingResponse(content=generate_random_chart(),
                             media_type='application/x-ndjson')


@router.get("/{crawler_uuid}/logs")
async def crawler_logs(crawler_id: int):
    return StreamingResponse(content=generate_random_log(),
                             media_type='application/x-ndjson')


@router.get("/dashboard/chart")
async def dashboard_chart():
    return StreamingResponse(content=generate_random_chart(),
                             media_type='application/x-ndjson')

@router.get("/dashboard/crawlers")
async def dashboard_crawlers():
    return StreamingResponse(content=generate_random_crawlers_data(),
                             media_type='application/x-ndjson')

