from datetime import date, datetime
import uuid
from uuid import UUID

from sqlalchemy import String, Text
from sqlmodel import SQLModel, Field, Relationship, VARCHAR, Column


class BoardMeetingInput(SQLModel):
    meetingdate: str
    purpose: str
    symbol: str


class BoardMeetingOutput(BoardMeetingInput):
    id: int
    meetingdate: str
    purpose: str
    symbol: str
    last_updated: datetime


class BoardMeeting(BoardMeetingInput, table=True):
    __tablename__ = "board_meeting"

    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    symbol: str = Field()
    meetingdate: str = Field(default=None)
    purpose: str = Field(sa_column=Column(Text))
    last_updated: datetime = Field(default_factory=datetime.utcnow)

