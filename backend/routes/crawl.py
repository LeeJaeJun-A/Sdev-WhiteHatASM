from fastapi import APIRouter, BackgroundTasks, WebSocket
from pydantic import BaseModel
from backend.crawler.validate_url import validate_url
from backend.crawler.crawl import crawl_url
from backend.routes.websocket import manager

class URLRequest(BaseModel):
    url: str


class crawlRequest(BaseModel):
    url: str
    id: str

router = APIRouter()


@router.post("/validate-url")
async def validate_url_endpoint(request: URLRequest):
    url = request.url
    result = validate_url(url)

    return result


@router.post("/crawl")
async def crawling(request: crawlRequest, background_tasks: BackgroundTasks):
    background_tasks.add_task(crawl_url, request.url, request.id)