from typing import Optional
from backend.database.models import User
from backend.user.lock_management import (
    increment_failed_attempts,
    check_account_locked,
)
from backend.authentication.token import create_token
from backend.config import (
    MAX_FAILURES,
    REHASH_COUNT_STANDARD,
    JWT_ACCESS_TOKEN_EXPIRE_SECONDS,
    JWT_REFRESH_TOKEN_EXPIRE_SECONDS,
)
from backend.authentication.rehash_password import rehash_password
import bcrypt
from sqlalchemy.orm import Session


def login(user_id: str, password: str, database: Session) -> Optional[dict]:
    if check_account_locked(user_id, database):
        return {
            "status": "fail",
            "message": "This account is locked. Contact an admin to unlock.",
            "remaining_attempts": 0,
        }

    user = database.query(User).filter(User.id == user_id).one_or_none()
    if user is None:
        return {
            "status": "fail",
            "message": "User not found",
            "remaining_attempts": 0,
        }

    if bcrypt.checkpw(password.encode("utf-8"), user.password.encode("utf-8")):
        user.request_success_count += 1
        if user.request_success_count % REHASH_COUNT_STANDARD == 0:
            rehash_password(user.id, user.password.encode("utf-8"), database)
        user.failed_attempts = 0
        database.commit()
        
        # Generate tokens
        access_token = create_token(
            data={"id": user.id, "role": user.role},
            expire_second=JWT_ACCESS_TOKEN_EXPIRE_SECONDS,
        )
        refresh_token = create_token(
            data={"id": user.id, "role": user.role},
            expire_second=JWT_REFRESH_TOKEN_EXPIRE_SECONDS,
        )
        
        return {
            "status": "success",
            "access_token": access_token,
            "refresh_token": refresh_token,
            "token_type": "bearer",
            "role": user.role,
        }
    else:
        increment_failed_attempts(user_id, database)
        remaining_attempts = MAX_FAILURES - user.failed_attempts
        return {
            "status": "fail",
            "message": "Incorrect ID or password",
            "remaining_attempts": remaining_attempts,
        }
