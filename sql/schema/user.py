import bcrypt
from pydantic import BaseModel
from sqlmodel import SQLModel, Field
from typing import Optional


# 只要写好这个类就行，不需要做任何 extra 动作
class UserBase(SQLModel):
    userName: str = Field(
        index=True, unique=True, max_length=50, nullable=False, description="用户名"
    )

    email: Optional[str] = Field(default=None, max_length=100, description="邮箱")

    # 默认为1 (正常)
    status: int = Field(default=1, description="1=正常, 0=禁用")


class UserCreate(UserBase):
    password: str = Field(
        max_length=255, nullable=False, description="加密后的密码Hash"
    )


class User(UserBase, table=True):
    id: int | None = Field(default=None, primary_key=True)

    hashed_password: str = Field(
        max_length=255, nullable=False, description="加密后的密码Hash"
    )

    def verify_password(self, plain_password: str) -> bool:
        return bcrypt.checkpw(
            plain_password.encode("utf-8"), self.hashed_password.encode("utf-8")
        )

    @property
    def password(self):
        return AttributeError("fucking! go out!!")

    @password.setter
    def password(self, plain_password: str):
        # 生成盐并且加密
        hash_bytes = bcrypt.hashpw(plain_password.encode("utf-8"), bcrypt.gensalt())
        # 将 bytes 转为 str 存入数据库字段
        self.hashed_password = hash_bytes.decode("utf-8")


class UserPublic(UserBase):
    id: int


class Login(BaseModel):
    userName: str
    password: str


class TokenResponse(BaseModel):
    access_token: str
    userName: str
