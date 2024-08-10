from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from backend.database.mongodb import contact_collection
from uuid import uuid4
from typing import List

router = APIRouter()


class ContactRequest(BaseModel):
    title: str
    email: str
    phone: str
    message: str
    is_read: bool = False


class ContactID(BaseModel):
    id: str


@router.post("/contact")
def send_inquiry(contact: ContactRequest):
    new_id = str(uuid4())
    contact_dict = contact.model_dump()
    contact_dict["_id"] = new_id

    result = contact_collection.insert_one(contact_dict)
    if not result.acknowledged:
        raise HTTPException(status_code=500, detail="Failed to insert inquiry")

    return {"message": "Inquiry successfully added"}


@router.get("/contact")
def get_customer_inquiries():
    cursor = contact_collection.find({"is_read": False})
    inquiries = []
    for inquiry in cursor:
        inquiry["_id"] = str(inquiry["_id"])
        inquiries.append(inquiry)

    return inquiries


@router.put("/contact/read")
def mark_as_read(update: ContactID):
    result = contact_collection.update_one(
        {"_id": update.id}, {"$set": {"is_read": True}}
    )

    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="Inquiry not found")

    if result.modified_count == 0:
        raise HTTPException(status_code=500, detail="Failed to update inquiry")

    return {"message": "Inquiry marked as read"}


@router.delete("/contact")
def delete_inquiry(delete_request: ContactID):
    result = contact_collection.delete_one({"_id": delete_request.id})

    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Inquiry not found")

    return {"message": "Inquiry successfully deleted"}
