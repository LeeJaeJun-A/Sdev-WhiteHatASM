from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import List
from datetime import datetime
from backend.database.session import get_database
from backend.database.models import User
from backend.user.lock_management import unlock_account, lock_account
from backend.database.mongodb import history_collection
from backend.config import DEFAULT_ROOT_ACCOUNT_ID
import bcrypt
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

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


def create_user_in_db(user_data: UserCreate, database: Session) -> User:
    try:
        # 비밀번호 해싱
        logger.info(f"Generating salt and hashing password for user: {user_data.id}")
        salt = bcrypt.gensalt()
        hashed_password = bcrypt.hashpw(user_data.password.encode("utf-8"), salt)

        # 새로운 유저 생성
        logger.info(f"Creating new user in database: {user_data.id}")
        new_user = User(
            id=user_data.id,
            password=hashed_password.decode("utf-8"),
            salt=salt.decode("utf-8"),
            role=user_data.role,
            authorizer=user_data.authorizer,
        )
        database.add(new_user)
        database.commit()
        logger.info(f"New user created and committed to database: {user_data.id}")

        # 유저 데이터 새로고침
        database.refresh(new_user)
        logger.info(f"User data refreshed from database: {user_data.id}")

        # MongoDB에 기록 추가
        new_document = {"user_id": user_data.id, "histories": []}
        logger.info(f"Inserting history document in MongoDB for user: {user_data.id}")
        history_collection.insert_one(new_document)
        logger.info(f"History document inserted in MongoDB for user: {user_data.id}")

        return new_user

    except Exception as e:
        logger.error(
            f"An error occurred while creating user {user_data.id}: {e}", exc_info=True
        )
        raise e


@router.post("/user", response_model=UserCreateResponse)
def create_user(user_data: UserCreate, database: Session = Depends(get_database)):
    existing_user = database.query(User).filter(User.id == user_data.id).one_or_none()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User with this ID already exists.",
        )

    new_user = create_user_in_db(user_data, database)
    return UserCreateResponse(id=new_user.id, role=new_user.role)


@router.delete("/user/{id}")
def delete_user(id: str, database: Session = Depends(get_database)):
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

    history_collection.delete_one({"user_id": id})

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
