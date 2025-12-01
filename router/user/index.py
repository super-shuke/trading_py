from fastapi import APIRouter, HTTPException
from sqlmodel import or_, select
from passlib.context import CryptContext
from sql.client import db
from sql.schema.user import User


router = APIRouter(prefix="/api/v1/users", tags=["用户管理"])

statement = select(User)


@router.get("/")
def get_users_list(limit: int | None):
    results = db.get_list(User, limit=limit)
    return {"msg": "所有用户列表", "data": results, "code": 200}


@router.get("/search")
def get_search_user(userName: str | None, email: str | None):
    conditions = []
    if userName:
        conditions.append(User.userName.__contains__(userName))
    if email:
        conditions.append(User.email.__contains__(email))
    if conditions:
        statement = statement.where(or_(*conditions))
    else:
        return False
    results = db.exec(statement)
    return results


@router.post("/register")
def register_user(userParams: User):
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
        userParams.password = hashed_password
        db.add(userParams)
    return {"msg": "注册成功", "username": userParams.userName}
