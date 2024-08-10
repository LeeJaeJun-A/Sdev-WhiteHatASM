from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from pymongo import DESCENDING
from typing import List, Optional
from backend.database.mongodb import history_collection
import uuid

router = APIRouter()


class HistoryItem(BaseModel):
    _id: str
    time: str
    main_url: str
    status: str
    file: Optional[str] = None


class CreateHistoryRequest(BaseModel):
    user_id: str
    history: HistoryItem


class UpdateHistoryRequest(BaseModel):
    status: Optional[str] = None
    file: Optional[str] = None


@router.get("/history/{user_id}")
def get_histories(user_id: str):
    user_history = history_collection.find_one(
        {"user_id": user_id}, {"_id": 0, "histories": 1}
    )
    if user_history is None:
        raise HTTPException(status_code=404, detail="History not found")
    return user_history.get("histories", [])


@router.get("/history/{user_id}/recent", response_model=List[str])
def get_recent_histories(user_id: str):
    cursor = (
        history_collection.find({"user_id": user_id}, {"_id": 0, "histories": 1})
        .sort("histories.time", DESCENDING)
        .limit(10)
    )

    user_history = list(cursor)

    if not user_history:
        raise HTTPException(status_code=404, detail="History not found")

    main_urls = []
    for entry in user_history:
        histories = entry.get("histories", [])
        for history in histories:
            main_url = history.get("main_url")
            if main_url:
                main_urls.append(main_url)

    return main_urls


@router.post("/history")
def create_history(request: CreateHistoryRequest):
    history = request.history.model_dump()
    history["_id"] = str(uuid.uuid4())  # Generate a new UUID and convert it to a string
    user_id = request.user_id

    user_history = history_collection.find_one({"user_id": user_id})

    if user_history:
        update_result = history_collection.update_one(
            {"user_id": user_id}, {"$push": {"histories": history}}
        )
        if update_result.matched_count == 0:
            raise HTTPException(status_code=404, detail="User not found")
        return {"status": "history added", "history_id": history["_id"]}
    else:
        raise HTTPException(status_code=404, detail="User not found")


@router.put("/history/{user_id}/{history_id}")
def update_history(user_id: str, history_id: str, request: UpdateHistoryRequest):
    update_fields = {}
    if request.status is not None:
        update_fields["status"] = request.status
    if request.file is not None:
        update_fields["file"] = request.file

    if not update_fields:
        raise HTTPException(status_code=400, detail="No fields to update")

    result = history_collection.update_one(
        {"user_id": user_id, "histories._id": history_id},
        {"$set": {f"histories.$.{key}": value for key, value in update_fields.items()}},
    )

    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="History not found")

    return {"status": "updated"}


@router.delete("/history/{user_id}/{history_id}")
def delete_history(user_id: str, history_id: str):
    result = history_collection.update_one(
        {"user_id": user_id}, {"$pull": {"histories": {"_id": history_id}}}
    )

    if result.modified_count == 0:
        raise HTTPException(status_code=404, detail="History not found")

    return {"status": "deleted"}
