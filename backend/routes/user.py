from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import List
from datetime import datetime
from backend.database.session import get_database
from backend.database.models import User
from backend.user.lock_management import unlock_account, lock_account
from backend.database.mongodb_async import history_collection
from backend.config import DEFAULT_ROOT_ACCOUNT_ID
import bcrypt

router = APIRouter()


class UserCreate(BaseModel):
    id: str
    password: str
    role: str
    authorizer: str


class UserCreateResponse(BaseModel):
    id: str
    role: str


class UserInfo(BaseModel):
    id: str
    role: str
    authorizer: str
    created_at: datetime


class LockedUserInfo(BaseModel):
    id: str
    role: str
    authorizer: str
    locked_at: datetime


class UserRequest(BaseModel):
    id: str


async def create_user_in_db(user_data: UserCreate, database: Session) -> User:
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(user_data.password.encode("utf-8"), salt)
    new_user = User(
        id=user_data.id,
        password=hashed_password.decode("utf-8"),
        salt=salt.decode("utf-8"),
        role=user_data.role,
        authorizer=user_data.authorizer,
    )
    database.add(new_user)
    database.commit()
    database.refresh(new_user)

    new_document = {"user_id": user_data.id, "histories": []}
    await history_collection.insert_one(new_document)
    return new_user


@router.post("/user", response_model=UserCreateResponse)
async def create_user(user_data: UserCreate, database: Session = Depends(get_database)):
    existing_user = database.query(User).filter(User.id == user_data.id).one_or_none()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User with this ID already exists.",
        )

    new_user = await create_user_in_db(user_data, database)
    return UserCreateResponse(id=new_user.id, role=new_user.role)


@router.delete("/user/{id}")
async def delete_user(id: str, database: Session = Depends(get_database)):
    user = database.query(User).filter(User.id == id).one_or_none()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found."
        )

    if user.id == DEFAULT_ROOT_ACCOUNT_ID:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Unable to delete root administrator account.",
        )

    database.delete(user)
    database.commit()
    
    await history_collection.delete_one({"user_id": id})

    return {"detail": f"User {id} has been deleted."}


@router.get("/user", response_model=List[UserInfo])
def get_users(role: str = "all", database: Session = Depends(get_database)):
    if role not in ["all", "admin", "user"]:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid role specified. Choose from 'all', 'admin', 'user'.",
        )
    query = database.query(User)

    if role == "admin":
        query = query.filter(User.role == "admin")
    elif role == "user":
        query = query.filter(User.role == "user")

    users = query.all()

    return [
        UserInfo(
            id=user.id,
            role=user.role,
            authorizer=user.authorizer,
            created_at=user.created_at,
        )
        for user in users
    ]


@router.get("/user/locked", response_model=List[LockedUserInfo])
def get_locked_users(database: Session = Depends(get_database)):
    locked_users = database.query(User).filter(User.is_locked == True).all()

    return [
        LockedUserInfo(
            id=locked_user.id,
            role=locked_user.role,
            authorizer=locked_user.authorizer,
            locked_at=locked_user.locked_at,
        )
        for locked_user in locked_users
    ]


@router.post("/user/{id}/unlock")
def unlock_user(id: str, database: Session = Depends(get_database)):
    if not unlock_account(id, database):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Failed to unlock the user account. Check if the user is locked.",
        )
    return {"detail": f"User {id} has been unlocked."}


@router.post("/user/{id}/lock")
def lock_user(id: str, database: Session = Depends(get_database)):

    if id == DEFAULT_ROOT_ACCOUNT_ID:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Unable to lock root administrator account.",
        )

    if not lock_account(id, database):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Failed to lock the user account. Check if the user is valid.",
        )
    return {"detail": f"User {id} has been locked."}
