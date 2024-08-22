import requests
import pandas as pd
from io import StringIO

from fastapi import Depends, HTTPException, APIRouter
from sqlmodel import Session, select
from db import get_session
from typing import Sequence, List

from nse_component.board_meeting import override_board_meeting
from nse_component.dividend_service import override_dividend_results
from nse_component.financial_results import override_financial_results
from nse_component.shareholdings_patterns import override_shareholdings_patterns
from schema.equity import Equity, EquityInput

router = APIRouter(prefix="/api/nse")

header = {
    "Connection": "keep-alive",
    "Cache-Control": "max-age=0",
    "DNT": "1",
    "Upgrade-Insecure-Requests": "1",
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 '
                  'Safari/537.36',
    "Sec-Fetch-User": "?1", "Accept": "*/*",
    "Sec-Fetch-Site": "none", "Sec-Fetch-Mode": "navigate",
    "Accept-Encoding": "gzip, deflate, br",
    "Accept-Language": "en-US,en;q=0.9,hi;q=0.8",
}

base_url = "https://www.nseindia.com/api/"


# Use to fet NSE API
def nsefetch(url):
    try:
        output = requests.get(url, headers=header).json()
    except ValueError:
        s = requests.Session()
        output = s.get("http://nseindia.com", headers=header)
        output = s.get(url, headers=header).json()
    return output


# Get all equities or search equity by Symbol or ISIN
@router.get("/equities")
def get_equities(symbol: str | None = None, isin_number: str | None = None,
                 session: Session = Depends(get_session)) -> Sequence[Equity]:
    query = select(Equity)
    if symbol:
        query = query.where(Equity.symbol == symbol)
    if isin_number:
        query = query.where(Equity.isin_number == isin_number)
    return session.exec(query).all()


# Insert equity into database
@router.post("/insert-equity", response_model=Equity)
def insert_equity(car_input: EquityInput, session: Session = Depends(get_session)) -> Equity:
    new_equity = Equity.model_validate(car_input)
    session.add(new_equity)
    session.commit()
    session.refresh(new_equity)
    return new_equity


# Insert multiple equities into database
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


# Get trading holidays
@router.get("/holiday-master")
def holiday_master(holiday_type="trading"):
    r_session = requests.session()
    return r_session.get(base_url + f"holiday-master?type={holiday_type}", headers=header).json()


# Get company corporation information
@router.get("/top-corp-info")
def top_corp_info(symbol: str | None = "INFY", market: str = "equities"):
    r_session = requests.session()
    return r_session.get(base_url + f"top-corp-info?symbol={symbol}&market={market}", headers=header).json()


# Get all equeties in CSV format
@router.get("/equities_nse")
def equities():
    r_session = requests.session()
    response = r_session.get("https://nsearchives.nseindia.com/content/equities/EQUITY_L.csv", headers=header)
    csv_data = StringIO(response.text)
    df = pd.read_csv(csv_data)
    return df.to_json(orient='records')


# Update corporation information of companies
@router.get("/update-companies-corp-info")
def update_companies_corp_info(offset: int = 0, limit: int = 1, session: Session = Depends(get_session)):
    # query = select(Equity).where(Equity.symbol == 'AAREYDRUGS')
    query = select(Equity).offset(offset).limit(limit)
    all_equities: Sequence[Equity] = session.exec(query).all()
    errors: List[dict] = []
    for equity in all_equities:
        if equity.series == 'EQ':
            try:
                company_info = nsefetch(base_url + f"top-corp-info?symbol={equity.symbol}&market=equities")
                override_board_meeting(company_info['borad_meeting']['data'], session)
                override_shareholdings_patterns(company_info['shareholdings_patterns']['data'], equity.symbol, session)
                override_financial_results(company_info['financial_results']['data'], equity.symbol, session)
                override_dividend_results(company_info['corporate_actions']['data'], equity.symbol, session)    
            except requests.exceptions.JSONDecodeError:
                errors.append({"symbol": equity.symbol, "error": "Json parse error or No data available"})
                # return {"message": f"Failed to parse JSON {equity.symbol}"}
            except Exception as e:
                    errors.append({"symbol": equity.symbol, "error": str(e)})
                # return {"message": f"An error occurred while processing {equity.symbol}: {str(e)}"}
    return_msg = {
        "message": f"Company information updated successfully",
        "data": {
            "symbol": [equity.symbol for equity in all_equities],
            "error": errors
        }
    }
    return return_msg
