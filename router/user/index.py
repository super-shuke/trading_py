from datetime import timedelta
from typing import List
from fastapi import APIRouter, HTTPException
from config.index import ACCESS_TOKEN_EXPIRE_MINUTES
from sql.schema.user import Login, TokenResponse, UserCreate, UserPublic
from store.user.index import create_user, get_users, login_user, search_users
from utils.security.index import create_access_token


router = APIRouter(prefix="/api/v1/users", tags=["用户管理"])


@router.get("/")
def get_users_list(limit: int | None = None):
    safe_users = get_users(limit=limit)
    return {"msg": "所有用户列表", "data": safe_users, "code": 200}


@router.get("/search", response_model=List[UserPublic])
def get_search_user(userName: str | None, email: str | None = None):
    results = search_users(userName, email)
    return results


@router.post("/register", response_model=UserPublic)
def register_user(userParams: UserCreate):
    # 这里写注册逻辑...
    db_user = create_user(userParams)
    if db_user is None:
        raise HTTPException(status_code=400, detail="注册失败：用户名或邮箱已存在")

    return {"msg": "注册成功", "userName": userParams.userName}


@router.post("/sign", response_model=TokenResponse)
def login(login_data: Login):
    _user = login_user(login_data)
    if not _user:
        raise HTTPException(
            status_code=401,
            detail="用户名或密码错误",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    token = create_access_token(
        data={"sub": str(_user.id), "name": _user.userName},
        expires_delta=access_token_expires,
    )
    return {"access_token": token, "userName": _user.userName}
