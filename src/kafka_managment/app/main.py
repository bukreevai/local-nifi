from fastapi import FastAPI

from .config import config
from .general_models import Status

app = FastAPI(
    title="Local NIFI Managment Service",
    debug=config.debug
)


@app.get('/')
def main_main_page() -> None:
    """
    Return main page for service
    """
    return "Hello, world"


@app.get("/status", response_model=Status)
async def status():
    """
    Healthcheck
    """
    return {"status": "ok"}
