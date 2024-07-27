import csv

from fastapi import APIRouter, HTTPException
import requests
import pandas as pd
from io import StringIO

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


@router.get("/holiday-master")
def get_cars(holiday_type="trading"):
    r_session = requests.session()
    return r_session.get(base_url + f"holiday-master?type={holiday_type}", headers=header).json()


@router.get("/top-corp-info")
def get_cars(symbol: str | None = "INFY", market: str = "equities"):
    r_session = requests.session()
    return r_session.get(base_url + f"top-corp-info?symbol={symbol}&market={market}", headers=header).json()


@router.get("/equities")
def get_cars():
    r_session = requests.session()
    response = r_session.get("https://nsearchives.nseindia.com/content/equities/EQUITY_L.csv", headers=header)
    csv_data = StringIO(response.text)
    df = pd.read_csv(csv_data)
    return df.to_json(orient='records')

