import uuid
from datetime import datetime, date
from uuid import UUID
from sqlmodel import SQLModel, Field


class FinancialResultsInput(SQLModel):
    symbol: str
    from_date: date | None
    to_date: date | None
    expenditure: int | None
    income: float | None
    audited: str | None
    cumulative: str | None
    consolidated: str | None
    reDilEPS: float | None
    reProLossBefTax: float | None
    proLossAftTax: float | None
    re_broadcast_timestamp: datetime | None
    xbrl_attachment: str | None
    na_attachment: str | None
    last_updated: datetime


class FinancialResultsOutput(FinancialResultsInput):
    id: UUID
    symbol: str
    from_date: date | None
    to_date: date | None
    expenditure: float | None
    income: float | None
    audited: str | None
    cumulative: str | None
    consolidated: str | None
    reDilEPS: float | None
    reProLossBefTax: float | None
    proLossAftTax: float | None
    re_broadcast_timestamp: datetime | None
    xbrl_attachment: str | None
    na_attachment: str | None
    last_updated: datetime


class FinancialResults(FinancialResultsInput, table=True):
    __tablename__ = "financial_results"

    id: UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    symbol: str = Field(default=None)
    from_date: date | None = Field(default=None)
    to_date: date | None = Field(default=None)
    expenditure: float | None = Field(default=None)
    income: float | None = Field(default=None)
    audited: str | None = Field(default=None)
    cumulative: str | None = Field(default=None)
    consolidated: str | None = Field(default=None)
    reDilEPS: float | None = Field(default=None)
    reProLossBefTax: float | None = Field(default=None)
    proLossAftTax: float | None = Field(default=None)
    re_broadcast_timestamp: datetime | None = Field(default=None)
    xbrl_attachment: str | None = Field(default=None)
    na_attachment: str | None = Field(default=None)
    last_updated: datetime = Field(default_factory=datetime.utcnow)

