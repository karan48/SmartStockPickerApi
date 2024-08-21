import uuid
from datetime import datetime, date
from uuid import UUID
from sqlmodel import SQLModel, Field


class FinancialResultsInput(SQLModel):
    symbol: str
    from_date: date
    to_date: date
    expenditure: int
    income: int
    audited: str
    cumulative: str
    consolidated: str
    reDilEPS: int
    reProLossBefTax: int
    proLossAftTax: int
    re_broadcast_timestamp: datetime
    xbrl_attachment: str
    na_attachment: str
    last_updated: datetime


class FinancialResultsOutput(FinancialResultsInput):
    id: UUID
    symbol: str
    from_date: date
    to_date: date
    expenditure: int
    income: int
    audited: str
    cumulative: str
    consolidated: str
    reDilEPS: float
    reProLossBefTax: int
    proLossAftTax: int
    re_broadcast_timestamp: datetime
    xbrl_attachment: str
    na_attachment: str
    last_updated: datetime


class FinancialResults(FinancialResultsInput, table=True):
    __tablename__ = "financial_results"

    id: UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    symbol: str = Field(default=None)
    from_date: date = Field(default=None)
    to_date: date = Field(default=None)
    expenditure: int = Field(default=None)
    income: int = Field(default=None)
    audited: str = Field(default=None)
    cumulative: str = Field(default=None)
    consolidated: str = Field(default=None)
    reDilEPS: float = Field(default=None)
    reProLossBefTax: int = Field(default=None)
    proLossAftTax: int = Field(default=None)
    re_broadcast_timestamp: datetime = Field(default=None)
    xbrl_attachment: str = Field(default=None)
    na_attachment: str = Field(default=None)
    last_updated: datetime = Field(default_factory=datetime.utcnow)

