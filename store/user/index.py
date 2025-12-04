from sqlmodel import or_, select
from sql.client import db
from sql.schema.user import Login, User, UserCreate, UserPublic

# user 业务


# 注册用户
def create_user(user_params: UserCreate):
    # 这里写注册逻辑...
    has_user = select(User).where(User.userName == user_params.userName)
    results = db.execFirst(has_user)
    print(results, "has_user")
    if results:
        return None
    else:
        db_user = User(**user_params.model_dump(exclude={"password"}))
        db_user.password = user_params.password
        db.add(db_user)
        return db_user


# 用户登录


def login_user(login_data: Login):
    has_user = select(User).where(User.userName == login_data.userName)
    _user = db.execFirst(has_user)
    print(_user, "===xx")
    if not _user or not _user.verify_password(login_data.password):
        return None

    return _user


# 获取用户列表
def get_users(limit: int | None = None):
    results = db.get_list(User, limit=limit)
    safe_users = [UserPublic.model_validate(u) for u in results]
    return safe_users


# 搜索用户
def search_users(userName: str | None, email: str | None = None):
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
