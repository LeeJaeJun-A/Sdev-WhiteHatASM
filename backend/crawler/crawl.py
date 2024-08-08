from backend.routes.websocket import manager
import json
import asyncio


async def send_status(user_id: str, message: str):
    await manager.send_message(user_id, message)


async def send_json(user_id: str, data: dict):
    await manager.send_message(user_id, json.dumps(data))


"""
    input: url
    return: 메인 도메인, 서브 도메인에 대해서 각각 어떤 cve함수가 가능한지 매핑한 json
    
    * return값 예시
    {
        "url": url,
        "cve": ["CVE-2024-4443", "CVE-2024-3495", "CVE-2022-1421"],
        "children": [
            {
                "url": "https://section.cafe.naver.com/ca-fe/home",
                "cve": ["CVE-2024-22024", "CVE-2024-30043"],
                "children": [],
            },
            {
                "url": "https://section.blog.naver.com/BlogHome.naver?directoryNo=0&currentPage=1&groupId=0",
                "cve": ["CVE-2024-22024", "CVE-2024-30043"],
                "children": [],
            },
            {
                "url": "https://map.naver.com/p/",
                "cve": ["CVE-2022-1175"],
                "children": [],
            },
        ],
    }
    
    필요한 함수들은 backend/crawler에 새로 만들거나 backend/crawler/crawl.py에 추가해서 crawl_url 함수만으로 작동가능하도록 해야합니다.
    
"""


async def crawl_url(url: str, user_id: str):
    result = {}  # 여기에 결과를 하나씩 담으세요.
    sub_urls = [
        "https://section.cafe.naver.com/ca-fe/home",
        "https://section.blog.naver.com/BlogHome.naver?directoryNo=0&currentPage=1&groupId=0",
        "https://map.naver.com/p/",
    ]  # 여기에 sub url을 하나씩 담으세요.

    # 메인 URL에 대해서 크롤링 시작
    await send_status(user_id, f"Starting crawl for {url}")

    # 여기에 실제 크롤링 로직을 추가하세요.
    await asyncio.sleep(2)  # 이 부분은 삭제하고 실제 크롤링을 하세요.

    # 메인 URL에 대해서 크롤링 끝
    await send_status(user_id, f"Crawling {url} completed")

    for sub_url in sub_urls:
        # sub url 크롤링 시작
        await send_status(user_id, f"Starting crawl for {sub_url}")

        # 여기에 실제 크롤링 로직을 추가하세요.
        await asyncio.sleep(2)  # 이 부분은 삭제하고 실제 크롤링을 하세요.

        # sub url 크롤링 끝
        await send_status(user_id, f"Crawling {url} completed")

    # 전체 크롤링이 끝난 후
    await send_status(user_id, f"Full crawling completed")

    # 예시 result입니다.
    result = {
        "url": url,
        "cve": ["CVE-2024-4443", "CVE-2024-3495", "CVE-2022-1421"],
        "children": [
            {
                "url": "https://section.cafe.naver.com/ca-fe/home",
                "cve": ["CVE-2024-22024", "CVE-2024-30043"],
                "children": [],
            },
            {
                "url": "https://section.blog.naver.com/BlogHome.naver?directoryNo=0&currentPage=1&groupId=0",
                "cve": ["CVE-2024-22024", "CVE-2024-30043"],
                "children": [],
            },
            {
                "url": "https://map.naver.com/p/",
                "cve": ["CVE-2022-1175"],
                "children": [],
            },
        ],
    }

    await send_json(user_id, result)
