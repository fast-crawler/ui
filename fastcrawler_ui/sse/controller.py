import asyncio
from sse_starlette.sse import EventSourceResponse
from mock_data import generate_random_log, generate_random_chart


async def logs(request):
    return EventSourceResponse(generate_random_log())

async def chart(request):
    return EventSourceResponse(generate_random_chart())

