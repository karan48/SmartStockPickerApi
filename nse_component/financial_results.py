from datetime import datetime
from typing import List
from fastapi import HTTPException
from sqlmodel import Session
from schema.financial_results_schema import FinancialResults


# Override companies financial_results
def override_financial_results(financial_results_inputs, symbol, session: Session):
    try:
        remove_financial_results(symbol, session)
        update_financial_results(financial_results_inputs, symbol, session)
    except Exception as e:
        session.rollback()
        raise HTTPException(status_code=400, detail=f"An error occurred while overriding financial results: {e}")


# Update companies financial results
def update_financial_results(financial_results_inputs, symbol, session: Session):

    new_update_financial_results = []
    for financial_results_input in financial_results_inputs:
        financial_results_input['from_date'] = datetime.strptime(financial_results_input['from_date'], "%d %b %Y").strftime("%Y-%m-%d")
        financial_results_input['to_date'] = datetime.strptime(financial_results_input['to_date'], "%d %b %Y").strftime("%Y-%m-%d")
        financial_results_input['re_broadcast_timestamp'] = datetime.strptime(financial_results_input['re_broadcast_timestamp'],"%d-%b-%Y %H:%M").strftime("%Y-%m-%d %H:%M")
        financial_results_input['symbol'] = symbol
        
        financial_results = FinancialResults.model_validate(financial_results_input)
        session.add(financial_results)
        new_update_financial_results.append(financial_results)

    try:
        session.commit()
    except Exception as e:
        session.rollback()
        raise HTTPException(status_code=400, detail=f"An error occurred: {e}")

    for board_meeting in new_update_financial_results:
        session.refresh(board_meeting)

    return new_update_financial_results


# Delete companies financial results by symbol
def remove_financial_results(symbol: str, session) -> None:
    financial_results = session.query(FinancialResults).filter(FinancialResults.symbol == symbol).all()

    if financial_results:
        for bm in financial_results:
            session.delete(bm)
        session.commit()
