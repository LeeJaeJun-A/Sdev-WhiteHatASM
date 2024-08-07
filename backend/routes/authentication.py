import logging
from fastapi import APIRouter, status, Request, Depends
from fastapi.responses import JSONResponse
from pydantic import BaseModel, ValidationError
from backend.authentication.token import verify_token, create_token
from backend.authentication.login import login
from backend.database.session import get_database
from backend.config import DEFAULT_ROOT_ACCOUNT_ID, JWT_ACCESS_TOKEN_EXPIRE_SECONDS
from sqlalchemy.orm import Session

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
console_handler = logging.StreamHandler() 
console_handler.setLevel(logging.INFO) 
formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
console_handler.setFormatter(formatter)
logger.addHandler(console_handler)

router = APIRouter()


class LoginRequest(BaseModel):
    id: str
    password: str


class TokenRefreshRequest(BaseModel):
    refresh_token: str


class TokenRefreshResponse(BaseModel):
    access_token: str
    token_type: str


class TokenResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str
    role: str


@router.post("/token", response_model=TokenResponse)
async def login_for_access_token(
    request: Request, database: Session = Depends(get_database)
):
    try:
        login_request = await request.json()
        login_data = LoginRequest(**login_request)
    except ValidationError as e:
        logger.error(f"Validation error: {e.errors()}")
        return JSONResponse(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            content={"detail": e.errors()},
        )
    except Exception as e:
        logger.error(f"Exception: {e}")
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={"detail": "Invalid request"},
        )

    result = login(login_data.id, login_data.password, database)

    if result is None:
        logger.warning("Login failed: No result returned")
        return JSONResponse(
            status_code=status.HTTP_401_UNAUTHORIZED,
            content={"detail": "Invalid Access"},
            headers={
                "WWW-Authenticate": "Bearer",
                "Cache-Control": "no-store",
                "Pragma": "no-cache",
            },
        )
    if result["status"] == "fail":
        if login_data.id == DEFAULT_ROOT_ACCOUNT_ID:
            logger.warning("Login failed for root account")
            return JSONResponse(
                status_code=status.HTTP_401_UNAUTHORIZED,
                content={"detail": "Invalid Access"},
                headers={
                    "WWW-Authenticate": "Bearer",
                    "Cache-Control": "no-store",
                    "Pragma": "no-cache",
                },
            )
        logger.warning(
            f"Login failed: {result.get('message', 'Login failed.')}, Remaining attempts: {result.get('remaining_attempts', 0)}"
        )
        return JSONResponse(
            status_code=status.HTTP_401_UNAUTHORIZED,
            content={
                "detail": result.get("message", "Login failed."),
                "remaining_attempts": int(result.get("remaining_attempts", 0)),
            },
            headers={
                "WWW-Authenticate": "Bearer",
                "Cache-Control": "no-store",
                "Pragma": "no-cache",
            },
        )
    logger.info(f"Login successful: {login_data.id}")
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={
            "access_token": result["access_token"],
            "refresh_token": result["refresh_token"],
            "token_type": result["token_type"],
            "role": result["role"],
        },
        headers={
            "Cache-Control": "no-store",
            "Pragma": "no-cache",
        },
    )


@router.post("/refresh", response_model=TokenRefreshResponse)
async def refresh_access_token(request: TokenRefreshRequest):
    logger.info(f"Received request to refresh token: {request.refresh_token}")
    payload = verify_token(request.refresh_token)

    if payload is None:
        logger.warning("Invalid refresh token provided")
        return JSONResponse(
            status_code=status.HTTP_401_UNAUTHORIZED,
            content={"detail": "Invalid refresh token"},
            headers={"WWW-Authenticate": "Bearer"},
        )
    logger.info(f"Received request to refresh token: {payload}")

    if "id" not in payload:
        logger.error("Payload does not contain 'id' key")
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={"detail": "Invalid payload structure"},
        )

    access_token = create_token(
        data={"id": payload["id"], "role": payload["role"]},
        expire_second=JWT_ACCESS_TOKEN_EXPIRE_SECONDS,
    )
    
    logger.info(f"Successfully created new access token for user: {payload['id']}")

    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={"access_token": access_token, "token_type": "bearer"},
    )


def get_user(request: Request):
    auth_header = request.headers.get("Authorization")
    if auth_header is None:
        logger.warning("Authorization header missing")
        return JSONResponse(
            status_code=status.HTTP_401_UNAUTHORIZED,
            content={"detail": "Authorization header missing"},
            headers={"WWW-Authenticate": "Bearer"},
        )
    token = auth_header.split(" ")[1]
    payload = verify_token(token)
    return payload


@router.get("/verify-token")
async def verify_token_api(current_user: dict = Depends(get_user)):
    return {"status": "Token is valid", "user": current_user}
