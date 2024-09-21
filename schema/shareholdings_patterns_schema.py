from datetime import datetime, date
import uuid
from uuid import UUID
from sqlmodel import SQLModel, Field


class ShareholdingsPatternsInput(SQLModel):
    symbol: str
    promoter: str | None
    public: str | None
    employee_trusts: str | None
    nse_last_updated: date | None


class ShareholdingsPatternsOutput(ShareholdingsPatternsInput):
    id: int
    symbol: str | None
    promoter: str | None
    public: str | None
    employee_trusts: str | None
    nse_last_updated: date | None


class ShareholdingsPatterns(ShareholdingsPatternsInput, table=True):
    __tablename__ = "shareholdings_patterns"

    id: UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    symbol: str = Field(default=None)
    promoter: str | None = Field(default=None)
    public: str | None = Field(default=None)
    employee_trusts: str | None = Field(default=None)
    nse_last_updated: date | None = Field(default=None)
    last_updated: datetime = Field(default_factory=datetime.utcnow)

