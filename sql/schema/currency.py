from sqlmodel import SQLModel, Field


class Currency(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    symbol: str
    active: bool
