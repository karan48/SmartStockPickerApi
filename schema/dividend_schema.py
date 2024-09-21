import uuid
from datetime import datetime, date
from uuid import UUID
from sqlmodel import SQLModel, Field


class DividendInput(SQLModel):
    symbol: str
    dividend_date: date
    dividend: float


class DividendOutput(DividendInput):
    id: UUID
    symbol: str
    dividend_date: date
    dividend: float
    last_updated: datetime


class Dividend(DividendInput, table=True):
    __tablename__ = "dividend"

    id: UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    symbol: str = Field(default=None)
    dividend_date: date = Field(default=None)
    dividend: float = Field(default=None)
    last_updated: datetime = Field(default_factory=datetime.utcnow)

