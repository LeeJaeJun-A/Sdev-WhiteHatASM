from backend.routes.websocket import manager
from backend.core.report import gender_report, save_report ,vuln_all
import json
import asyncio
import datetime

json_file_path = '/app/backend/core/json/cve.json'

async def send_status(user_id: str, message: str):
    await manager.send_message(user_id, message)


async def send_json(user_id: str, data: dict):
    await manager.send_message(user_id, json.dumps(data))

def load_cve_data(json_file_path):
    with open(json_file_path, 'r') as file:
        cve_data = json.load(file)
    return cve_data

def transform_cve_to_vulnerabilities(cve_data, urlCVEList):
    vulnerabilities = []
    for idx, cve_info in enumerate(cve_data['cve_list'], start=1):
        target_keys = cve_info.get("endpoint", "unknown")
        if isinstance(target_keys, str):
            target_keys = [target_keys]

        vulnerability = {
            'number': idx,
            'vuln': cve_info["vuln"],
            'cve': cve_info["cve number"],
            'url': urlCVEList[0][0],
            'target_keys': target_keys,
            'target_values': ["example_value"],  # Example values
            'cvss_score': f'{cve_info["cvss"]}/10',  # CVSS score
            'payload': cve_info["payloads"]  # Payload from cve_data
        }
        vulnerabilities.append(vulnerability)
    return vulnerabilities

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
    cve_data = load_cve_data(json_file_path)
    vulnerabilities = transform_cve_to_vulnerabilities(cve_data, urlCVEList)

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
    
    date = datetime.datetime.now().strftime('%Y. %m. %d')
    structure = "대상 구조 설명"
    
    gender_report(urlCVEList[0][0], urlCVEList[0][0], date, structure)
    vuln_all(vulnerabilities)
    file_id  = save_report()
    
    # 보고서 생성 완료
    await send_status(user_id, f"The report '{file_id}' has been completed.")
    await send_status(user_id, f"Completing the test.")
