from fastapi import APIRouter, BackgroundTasks
from pydantic import BaseModel
from typing import List
from backend.core.test import cveTest

class CVERequest(BaseModel):
    urlCVEList: List[str]
    id: str

router = APIRouter()


@router.post("/test")
async def test(cve_request: CVERequest, background_tasks: BackgroundTasks):
    urlCVEList = cve_request.urlCVEList

    cve_list = []

    for entry in urlCVEList:
        parts = entry.split(" ", 1)
        if len(parts) == 2:
            url, cve = parts
            cve_list.append((url, cve))

    background_tasks.add_task(cveTest, cve_list, cve_request.id)
        
    return {"status": "Test started"}