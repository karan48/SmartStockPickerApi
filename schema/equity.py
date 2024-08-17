from datetime import date

from sqlmodel import SQLModel, Field, Relationship, VARCHAR, Column


class EquityInput(SQLModel):
    date_of_listing: str
    face_value: int
    isin_number: str
    market_lot: int
    series: str
    company_name: str
    symbol: str
    paid_up_value: int


class EquityOutput(EquityInput):
    id: int
    date_of_listing: str
    face_value: int
    isin_number: str
    market_lot: int
    series: str
    company_name: str
    symbol: str
    paid_up_value: int


class Equity(EquityInput, table=True):
    id: int | None = Field(primary_key=True, default=None)
    date_of_listing: date = Field(default=None)
    face_value: int = Field(default=None)
    isin_number: str = Field(unique=True)
    market_lot: int = Field(default=None)
    series: str = Field(default=None)
    company_name: str = Field(default=None)
    symbol: str = Field(unique=True)
    paid_up_value: int = Field(default=None)
