from typing import List
from fastapi import APIRouter, HTTPException
from sqlmodel import or_, select
from passlib.context import CryptContext
from sql.client import db
from sql.schema.user import User, UserBase, UserCreate, UserPublic


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
    results = db.exec(statement)
    return results


@router.post("/register", response_model=UserPublic)
def register_user(userParams: UserCreate):
    # 这里写注册逻辑...
    has_user = select(User).where(User.userName == userParams.userName)
    results = db.exec(has_user)
    print(results, "has_user")
    if results:
        return HTTPException(status_code=400, detail="注册失败：用户名或邮箱已存在")
    else:
        pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
        try:
            hashed_password = pwd_context.hash(userParams.password)
        except ValueError as e:
            raise HTTPException(status_code=400, detail="密码格式错误或过长")
        db_user = User.model_validate(userParams, update={"password": hashed_password})
        db.add(db_user)
    return {"msg": "注册成功", "username": userParams.userName}
