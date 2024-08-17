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

