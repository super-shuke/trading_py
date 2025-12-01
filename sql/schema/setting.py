from sqlmodel import SQLModel, Field


class Setting(SQLModel, table=True):
    # id: int | None = Field(default=None, primary_key=True)
    language: str
    theme: str
