import uvicorn
from starlette.applications import Starlette
from routers import routes

app = Starlette(debug=True, routes=routes)

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000, log_level='info')
