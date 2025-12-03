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
    password: str = Field(
        max_length=255, nullable=False, description="加密后的密码Hash"
    )


class UserPublic(UserBase):
    id: int
