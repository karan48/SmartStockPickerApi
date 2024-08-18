import csv

from fastapi import APIRouter, HTTPException
import requests
import pandas as pd
from io import StringIO

from fastapi import Depends, HTTPException, APIRouter
from sqlmodel import Session, select
from db import get_session
from typing import Sequence, Type, List
from schema.equity import Equity, EquityInput
from schema.board_meeting_schema import BoardMeeting, BoardMeetingInput

router = APIRouter(prefix="/api/nse")

header = {
    "Connection": "keep-alive",
    "Cache-Control": "max-age=0",
    "DNT": "1",
    "Upgrade-Insecure-Requests": "1",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                  "Chrome/111.0.0.0 Safari/537.36",
    "Sec-Fetch-User": "?1", "Accept": "*/*", "Sec-Fetch-Site": "none", "Sec-Fetch-Mode": "navigate",
    "Accept-Encoding": "gzip, deflate, br", "Accept-Language": "en-US,en;q=0.9,hi;q=0.8"
}

base_url = "https://www.nseindia.com/api/"


@router.get("/equities")
def get_equities(symbol: str | None = None, isin_number: str | None = None,
                 session: Session = Depends(get_session)) -> Sequence[Equity]:
    query = select(Equity)
    if symbol:
        query = query.where(Equity.symbol == symbol)
    if isin_number:
        query = query.where(Equity.isin_number == isin_number)
    return session.exec(query).all()


@router.get("/update-companies-corp-info")
def update_companies_corp_info(session: Session = Depends(get_session)):
    query = select(Equity)
    query = query.where(Equity.symbol == 'INFY')
    all_equities: Sequence[Equity] = session.exec(query).all()
    company_info = []

    # Apply for loop to process each Equity instance
    for equity in all_equities:
        print(f"Processing Equity with symbol: {equity.symbol}")
        if equity.series == 'EQ':
            r_session = requests.session()
            company_info = r_session.get(base_url + f"top-corp-info?symbol={equity.symbol}&market=equities",
                                         headers=header).json()

    # Return the equities (or modify as needed)
    return company_info


@router.post("/insert-equity", response_model=Equity)
def insert_equity(car_input: EquityInput, session: Session = Depends(get_session)) -> Equity:
    new_equity = Equity.model_validate(car_input)
    session.add(new_equity)
    session.commit()
    session.refresh(new_equity)
    return new_equity


@router.post("/insert-equity-multiple", response_model=List[Equity])
def insert_equity_multiple(equity_inputs: List[EquityInput], session: Session = Depends(get_session)) -> List[Equity]:
    new_equities = []
    for equity_input in equity_inputs:
        new_equity = Equity.model_validate(equity_input)
        session.add(new_equity)
        new_equities.append(new_equity)

    try:
        session.commit()
    except Exception as e:
        session.rollback()
        raise HTTPException(status_code=400, detail=f"An error occurred: {e}")

    for equity in new_equities:
        session.refresh(equity)

    return new_equities


@router.get("/holiday-master")
def holiday_master(holiday_type="trading"):
    r_session = requests.session()
    return r_session.get(base_url + f"holiday-master?type={holiday_type}", headers=header).json()


@router.get("/top-corp-info")
def top_corp_info(symbol: str | None = "INFY", market: str = "equities"):
    r_session = requests.session()
    return r_session.get(base_url + f"top-corp-info?symbol={symbol}&market={market}", headers=header).json()


@router.get("/equities_nse")
def equities():
    r_session = requests.session()
    response = r_session.get("https://nsearchives.nseindia.com/content/equities/EQUITY_L.csv", headers=header)
    csv_data = StringIO(response.text)
    df = pd.read_csv(csv_data)
    return df.to_json(orient='records')



@router.post("/insert-borad-meeting")
def insert_borad_meeting(board_meeting_inputs: List[BoardMeetingInput], session: Session = Depends(get_session)) -> List[BoardMeeting]:
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

    for board_meeting in new_board_meeting:
        session.refresh(board_meeting)

    return new_board_meetings
