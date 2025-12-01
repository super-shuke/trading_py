from sqlmodel import SQLModel, Field
from typing import Optional


# 只要写好这个类就行，不需要做任何 extra 动作
class User(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    userName: str = Field(index=True, unique=True, max_length=50, nullable=False)
    password: str = Field(
        min_items=8,
        max_length=255,
        description="存放经过哈希加密后的密码字符串",
    )
    email: Optional[str] = Field(default=None, max_length=100)
    status: int = Field(default=1, description="1=正常, 0=禁用")
