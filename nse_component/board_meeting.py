from typing import List

from fastapi import HTTPException
from sqlmodel import Session

from schema.board_meeting_schema import BoardMeetingInput, BoardMeeting


# Override companies board meeting
def override_board_meeting(board_meeting_inputs: List[BoardMeetingInput], session: Session):
    try:
        if board_meeting_inputs.__len__() > 0:
            remove_cars_by_size(board_meeting_inputs[0]['symbol'], session)

        update_board_meeting(board_meeting_inputs, session)
    except Exception as e:
        session.rollback()
        raise HTTPException(status_code=400, detail=f"An error occurred while overriding board meetings: {e}")


# override companies board meeting
def update_board_meeting(board_meeting_inputs: List[BoardMeetingInput], session: Session):
    new_board_meetings = []
    for board_meeting_input in board_meeting_inputs:
        new_board_meeting = BoardMeeting.model_validate(board_meeting_input)
        session.add(new_board_meeting)
        new_board_meetings.append(new_board_meeting)

    try:
        session.commit()
    except Exception as e:
        session.rollback()
        raise HTTPException(status_code=400, detail=f"An error occurred: {e}")

    for board_meeting in new_board_meetings:
        session.refresh(board_meeting)

    return new_board_meetings


# Delete companies board meeting by symbol
def remove_cars_by_size(symbol: str, session) -> None:
    board_meeting = session.query(BoardMeeting).filter(BoardMeeting.symbol == symbol).all()

    if board_meeting:
        for bm in board_meeting:
            session.delete(bm)
        session.commit()
