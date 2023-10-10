from starlette.routing import Route
from controller import logs, chart


routes = [
    Route("/{crawler_id}/logs", endpoint=logs),
    Route("/{crawler_id}/chart", endpoint=chart),
]
