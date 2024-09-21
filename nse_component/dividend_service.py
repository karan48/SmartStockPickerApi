from datetime import datetime
import re
from typing import List
from fastapi import HTTPException
from sqlmodel import Session
from schema.dividend_schema import Dividend


# Override companies dividend results
def override_dividend_results(dividend_results_inputs, symbol, session: Session):
    try:
        remove_dividend_results(symbol, session)
        update_dividend_results(dividend_results_inputs, symbol, session)
    except Exception as e:
        session.rollback()
        raise HTTPException(status_code=400, detail=f"An error occurred while overriding dividend results: {e}")


# Update companies dividend results
def update_dividend_results(dividend_results_inputs, symbol, session: Session):

    new_update_dividend_results = []
    for dividend_results_input in dividend_results_inputs:
        dividends = re.findall(r'\d+', dividend_results_input["purpose"])
        dividends = list(map(int, dividends))

        for dividend in dividends:
            dividend_results_input['dividend'] = dividend
            dividend_results_input['dividend_date'] = datetime.strptime(dividend_results_input['exdate'], "%d-%b-%Y").strftime("%Y-%m-%d")
            dividend_results_input['symbol'] = symbol
            
            dividend_results = Dividend.model_validate(dividend_results_input)
            session.add(dividend_results)
            new_update_dividend_results.append(dividend_results)

    try:
        session.commit()
    except Exception as e:
        session.rollback()
        raise HTTPException(status_code=400, detail=f"An error occurred: {e}")

    for board_meeting in new_update_dividend_results:
        session.refresh(board_meeting)

    return new_update_dividend_results


# Delete companies dividend results by symbol
def remove_dividend_results(symbol: str, session) -> None:
    dividend_results = session.query(Dividend).filter(Dividend.symbol == symbol).all()

    if dividend_results:
        for bm in dividend_results:
            session.delete(bm)
        session.commit()
