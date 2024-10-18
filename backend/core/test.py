from backend.routes.websocket import manager
from backend.core.report import save_report
import json
import asyncio

async def send_status(user_id: str, message: str):
    await manager.send_message(user_id, message)


async def send_json(user_id: str, data: dict):
    await manager.send_message(user_id, json.dumps(data))


"""
    input: (url, cve종류) 쌍의 tuple을 가진 list
    ex)
    [
        ("https://www.youtube.com", "CVE-2024-3495"),
        ("https://section.cafe.naver.com/ca-fe/home", "CVE-2024-22024"),
        (
            "https://section.blog.naver.com/BlogHome.naver?directoryNo=0&currentPage=1&groupId=0",
            "CVE-2024-22024",
        ),
    ]
    output: x
    
    socket으로 메세지 보내는 것만 확실하게 해주고, 보고서 생성 후 db에 파일 저장해주면 됩니다.
    파일 업로드 후 생기는 파일 id를 기반으로 db에서 보고서를 요청 후 다운로드할 것입니다.

"""
async def cveTest(urlCVEList: list, user_id: str):
    for url, cve in urlCVEList:
        # 테스트를 시작할 때 항상 이 메세지를 보내고 시작하셔야 합니다.
        await send_status(user_id, f"Testing for {cve} on {url} is starting.")
        
        # 여기에 실제 테스트 로직을 추가하세요.
        await asyncio.sleep(2)  # 이 부분은 삭제하고 해당하는 테스트 함수를 실행하세요.
        
        # 테스트가 끝났을 때
        await send_status(user_id, f"Testing for {cve} on {url} has been completed.")
    
    # 전체 테스트가 끝났을 때
    issues_found = 3
    no_issues = 4
    await send_status(user_id, f"All CVE tests are complete. Issues found in {issues_found} CVEs. {no_issues} CVEs showed no issues.")
    
    # 보고서 생성 시작
    await send_status(user_id, f"Initiating the report generation process.")
    
    # 여기에 실제 보고서 생성 로직을 추가하세요.
    #save_report()
    file_id  = save_report()
    
    # 보고서 생성 완료
    await send_status(user_id, f"The report '{file_id}' has been completed.")
    await send_status(user_id, f"Completing the test.")
