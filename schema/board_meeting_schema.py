from datetime import date

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


class BoardMeeting(BoardMeetingInput, table=True):
    __tablename__ = "board_meeting"

    id: int | None = Field(primary_key=True, default=None)
    symbol: str = Field()
    meetingdate: str = Field(default=None)
    purpose: str = Field(default=None)

