from datetime import datetime, date

from sqlmodel import SQLModel, Field


class ShareholdingsPatternsInput(SQLModel):
    symbol: str
    promoter: str
    public: str
    employee_trusts: str
    nse_last_updated: date


class ShareholdingsPatternsOutput(ShareholdingsPatternsInput):
    id: int
    symbol: str
    promoter: str
    public: str
    employee_trusts: str
    nse_last_updated: date
    last_updated: datetime


class ShareholdingsPatterns(ShareholdingsPatternsInput, table=True):
    __tablename__ = "shareholdings_patterns"

    id: int | None = Field(primary_key=True, default=None)
    symbol: str = Field(default=None)
    promoter: str = Field(default=None)
    public: str = Field(default=None)
    employee_trusts: str = Field(default=None)
    nse_last_updated: date = Field(default=None)
    last_updated: datetime = Field(default_factory=datetime.utcnow)

