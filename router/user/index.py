from datetime import timedelta
from typing import List
from fastapi import APIRouter, HTTPException
from sqlmodel import or_, select
from passlib.context import CryptContext
from config.index import ACCESS_TOKEN_EXPIRE_MINUTES
from sql.client import db
from sql.schema.user import Login, TokenResponse, User, UserBase, UserCreate, UserPublic
from utils.security.index import create_access_token


router = APIRouter(prefix="/api/v1/users", tags=["用户管理"])


@router.get("/")
def get_users_list(limit: int | None):
    results = db.get_list(User, limit=limit)
    print(results, "---")
    safe_users = [UserPublic.model_validate(u) for u in results]

    return {"msg": "所有用户列表", "data": safe_users, "code": 200}


@router.get("/search", response_model=List[UserPublic])
def get_search_user(userName: str | None, email: str | None = None):
    conditions = []
    if userName:
        conditions.append(User.userName.contains(userName))
    if email:
        conditions.append(User.email.contains(email))
    if conditions:
        statement = select(User).where(or_(*conditions))
    else:
        return []
    results = db.execAll(statement)
    return results


@router.post("/register", response_model=UserPublic)
def register_user(userParams: UserCreate):
    # 这里写注册逻辑...
    has_user = select(User).where(User.userName == userParams.userName)
    results = db.execFirst(has_user)
    print(results, "has_user")
    if results:
        return HTTPException(status_code=400, detail="注册失败：用户名或邮箱已存在")
    else:
        db_user = User(**userParams.model_dump(exclude={"password"}))
        db_user.password = userParams.password
        db.add(db_user)
    return {"msg": "注册成功", "userName": userParams.userName}


@router.post("/sign", response_model=TokenResponse)
def login(login_data: Login):
    has_user = select(User).where(User.userName == login_data.userName)
    _user = db.execFirst(has_user)
    print(_user, "===xx")
    if not _user or not _user.verify_password(login_data.password):
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
