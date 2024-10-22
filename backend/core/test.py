from backend.routes.websocket import manager
from backend.core.report import gender_report, save_report, vuln_all
import json
import asyncio
import datetime

json_file_path = 'backend/core/json/cve.json'

async def send_status(user_id: str, message: str):
    await manager.send_message(user_id, message)

async def send_json(user_id: str, data: dict):
    await manager.send_message(user_id, json.dumps(data))

def load_cve_data(json_file_path):
    with open(json_file_path, 'rb') as file:
        cve_data = json.load(file)
    return cve_data

def transform_cve_to_vulnerabilities(cve_info, url, idx):
    target_keys = cve_info.get("endpoint", "unknown")
    if isinstance(target_keys, str):
        target_keys = [target_keys]

    vulnerability = {
        'number': idx,  # idx를 그대로 반영
        'vuln': cve_info["vuln"],
        'cve': cve_info["cve number"],  # cve도 반영
        'url': url,  # 해당 URL을 반영
        'target_keys': target_keys,
        'target_values': ["example_value"],  # 예시 값
        'cvss_score': f'{cve_info["cvss"]}/10',  # CVSS 점수
        'payload': cve_info["payloads"]  # cve_data에서 가져온 payload
    }
    return vulnerability

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
    vulnerabilities = []  # 최종적으로 vulnerabilities 리스트를 담을 곳
    idx = 1  # 각 취약점에 대한 번호를 추적할 idx

    for url, cve in urlCVEList:
        # 테스트를 시작할 때 메시지 전송
        await send_status(user_id, f"Testing for {cve} on {url} is starting.")
        
        # 현재 더미데이터로 보고서를 생성하고 있습니다. 추후 테스트 로직을 추가한 후 수정 바랍니다.
        filtered_cve_data = [cve_info for cve_info in cve_data['cve_list'] if cve_info["cve number"] == cve]
        
        if not filtered_cve_data:
            await send_status(user_id, f"No data found for {cve} on {url}.")
            continue
        
        for cve_info in filtered_cve_data:
            vulnerability = transform_cve_to_vulnerabilities(cve_info, url, idx)
            vulnerabilities.append(vulnerability)
            idx += 1  # 각 취약점마다 idx를 증가시킴

        # 여기에 실제 테스트 로직을 추가하세요.
        await asyncio.sleep(2)  # 예시로 2초 대기 (실제 테스트 코드로 대체)
        
        # 테스트 완료 후 메시지 전송
        await send_status(user_id, f"Testing for {cve} on {url} has been completed.")

    # 전체 테스트 완료 메시지
    issues_found = len(vulnerabilities)  # 예시로 vulnerabilities 개수를 사용
    no_issues = len(urlCVEList) - issues_found  # 예시 계산
    await send_status(user_id, f"All CVE tests are complete. Issues found in {issues_found} CVEs. {no_issues} CVEs showed no issues.")
    
    # 보고서 생성 시작
    await send_status(user_id, f"Initiating the report generation process.")
    
    date = datetime.datetime.now().strftime('%Y. %m. %d')
    structure = "대상 구조 설명"
    
    gender_report(urlCVEList[0][0], urlCVEList[0][0], date, structure)
    vuln_all(vulnerabilities)  # 모든 취약점을 vuln_all에 반영
    file_id = save_report()

    await send_status(user_id, f"The report '{file_id}' has been completed.")
    await send_status(user_id, f"Completing the test.")
