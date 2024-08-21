from typing import List

from fastapi import HTTPException
from sqlmodel import Session
from datetime import datetime

from schema.shareholdings_patterns_schema import ShareholdingsPatterns, ShareholdingsPatternsInput


# Override companies board meeting
def override_shareholdings_patterns(shareholdings_patterns_fetched_inputs, symbol, session: Session):
    try:
        # Remove existing share holding
        remove_shareholdings_patterns(symbol, session)

        shareholdings_patterns_inputs: List[ShareholdingsPatternsInput] = []
        for date, holdings in shareholdings_patterns_fetched_inputs.items():
            date_object = datetime.strptime(date.strip(), "%d-%b-%Y")
            nse_date = date_object.strftime("%Y-%m-%d")
            shareholdings_patterns_inputs = [
                ShareholdingsPatternsInput(
                    promoter=holdings[0]['Promoter & Promoter Group'].strip(),
                    public=holdings[1]['Public'].strip(),
                    employee_trusts=holdings[2]['Shares held by Employee Trusts'].strip(),
                    symbol=symbol,
                    nse_last_updated=nse_date
                )
            ]

        # Update share holding
        update_shareholdings_patterns(shareholdings_patterns_inputs, session)
    except Exception as e:
        session.rollback()
        raise HTTPException(status_code=400, detail=f"An error occurred while overriding shareholdings patterns: {e}")


# update_shareholdings_patterns
def update_shareholdings_patterns(shareholdings_patterns_inputs: List[ShareholdingsPatternsInput], session: Session):
    new_board_meetings = []
    for shareholdings_patterns_input in shareholdings_patterns_inputs:
        shareholdings_patterns = ShareholdingsPatterns.model_validate(shareholdings_patterns_input)
        session.add(shareholdings_patterns)
        new_board_meetings.append(shareholdings_patterns)

    try:
        session.commit()
    except Exception as e:
        session.rollback()
        raise HTTPException(status_code=400, detail=f"An error occurred: {e}")

    for board_meeting in new_board_meetings:
        session.refresh(board_meeting)

    return new_board_meetings


# Delete update_shareholdings_patterns by symbol
def remove_shareholdings_patterns(symbol: str, session) -> None:
    shareholdings_patterns = session.query(ShareholdingsPatterns).filter(ShareholdingsPatterns.symbol == symbol).all()

    if shareholdings_patterns:
        for bm in shareholdings_patterns:
            session.delete(bm)
        session.commit()
