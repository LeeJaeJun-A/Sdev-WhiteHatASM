# import sys
# import os

# sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))

from fastapi import WebSocket, WebSocketDisconnect
from backend.routes.websocket import ConnectionManager
import json
import asyncio
from backend.crawler.subdomain import SubdomainScanner
from backend.crawler.get_subdomains_directory import SubdomainDirectoryCrawler
from backend.crawler.version import AdvancedWebAnalyzer
from backend.crawler.myparser import Parser
from backend.database.mongodb import cve_collection
from typing import Dict, List, Any

manager = ConnectionManager()

async def check_connection(user_id: str):
    if user_id not in manager.active_connections:
        print(f"User {user_id} is not connected. Stopping the current task.")
        return False
    return True

async def send_status(user_id: str, message: str):
    await manager.send_message(user_id, message)


async def send_json(user_id: str, data: dict):
    await manager.send_message(user_id, json.dumps(data))


def get_cves(software_info: Dict[str, Any], directory_structure: Dict[str, Any]) -> List[str]:
    def check_endpoints(details: Dict[str, Any], cve: Dict[str, Any]) -> bool:
        if details is None:
            return False
        if 'input_tags' in details:
            for tag in details['input_tags']:
                if tag.get('type') == cve.get('endpoint') or tag.get('id') == cve.get('endpoint'):
                    return True
        return False

    def traverse_directory(directory: Dict[str, Any], cve: Dict[str, Any]) -> bool:
        details = directory.get('details')
        if details is not None and check_endpoints(details, cve):
            return True
        for child in directory.get('children', []):
            if traverse_directory(child, cve):
                return True
        return False

    matching_cves = set()

    if directory_structure is None:
        return list(matching_cves)

    os_value = software_info.get("os", "")
    technologies = software_info.get("technologies", [])
    frameworks = software_info.get("frameworks", [])

    print(f"OS: {os_value}")
    print(f"Technologies: {technologies}")
    print(f"Frameworks: {frameworks}")

    query = {
        "$or": [
            {"os": os_value.lower() if os_value else ""},
            {"technology": {"$in": [tech.lower() for tech in technologies if tech]}},
            {"framework": {"$in": [framework.lower() for framework in frameworks if framework]}}
        ]
    }

    for cve in cve_collection.find(query):
        if traverse_directory(directory_structure, cve):
            matching_cves.add(cve.get('cve number'))

    return list(matching_cves)


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


async def analyze_subdomain(user_id: str, subdomain: str):
    if not await check_connection(user_id):
        return None
    
    await send_status(user_id, f"Starting Analyzing for {subdomain}")

    if user_id not in manager.active_connections:
        print(
            f"User {user_id} is not connected. Skipping subdomain analysis for {subdomain}."
        )
        return None

    # 디렉토리 구조 크롤링과 소프트웨어 분석을 동시에 수행
    directory_crawler = SubdomainDirectoryCrawler(f"https://{subdomain}", max_depth=2)
    analyzer = AdvancedWebAnalyzer(f"https://{subdomain}")

    directory_task = asyncio.create_task(directory_crawler.run())
    analyzer_task = asyncio.create_task(analyzer.analyze())

    try:
        while not (directory_task.done() and analyzer_task.done()):
            if user_id not in manager.active_connections:
                print(
                    f"User {user_id} disconnected during analysis of {subdomain}. Canceling tasks."
                )
                directory_task.cancel()
                analyzer_task.cancel()
                raise asyncio.CancelledError("Subdomain analysis canceled.")
            await asyncio.sleep(1)  # 주기적으로 연결 상태 확인

        # 작업이 완료된 경우
        directory_structure, software_info = await asyncio.gather(
            directory_task, analyzer_task
        )

        cves = get_cves(software_info, directory_structure)

        # 결과 조합
        subdomain_result = {"url": f"https://{subdomain}", "cve": cves, "children": []}

        await send_status(
            user_id, f"Completed analysis of the subdomain list for {subdomain}"
        )
        return subdomain_result

    except asyncio.CancelledError:
        await send_status(user_id, f"Analysis for {subdomain} was canceled.")
        return None


async def crawl_url(url: str, user_id: str):
    if not await check_connection(user_id):
        return None
    
    # 서브 도메인 리스트 스캔
    await send_status(user_id, f"Starting analysis of the subdomain list for {url}")

    subdomain_scanner = SubdomainScanner(url)
    sub_urls = await subdomain_scanner.scan()
    
    if not await check_connection(user_id):
        return None
    
    main_analyzer = AdvancedWebAnalyzer(url)
    main_directory_crawler = SubdomainDirectoryCrawler(url, max_depth=2)

    if not await check_connection(user_id):
        return None
    
    # Todo. add cancel function in main_analyzer
    main_analyzer_task = asyncio.create_task(main_analyzer.analyze())
    main_directory_task = asyncio.create_task(main_directory_crawler.run())
    subdomain_tasks = [analyze_subdomain(user_id, subdomain) for subdomain in sub_urls]

    if not await check_connection(user_id):
        return None
    
    all_results = await asyncio.gather(main_analyzer_task, main_directory_task, *subdomain_tasks)

    main_software_info = all_results[0]
    main_directory_structure = all_results[1]
    subdomain_results = all_results[2:]

    if not await check_connection(user_id):
        return None
    
    result = {
        "url": url,
        "cve": get_cves(main_software_info, main_directory_structure),
        "children": subdomain_results
    }

    await send_status(user_id, f"Full crawling completed")
    await send_json(user_id, result)