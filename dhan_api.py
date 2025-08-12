import requests
from datetime import datetime, timedelta
import pytz

# Hardcoded Dhan API token
DHAN_API_TOKEN = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzUxMiJ9.eyJpc3MiOiJkaGFuIiwicGFydG5lcklkIjoiIiwiZXhwIjoxNzU0OTcwMDI4LCJ0b2tlbkNvbnN1bWVyVHlwZSI6IlNFTEYiLCJ3ZWJob29rVXJsIjoiIiwiZGhhbkNsaWVudElkIjoiMTEwMDI3OTk2OCJ9.xCXf8u7XL6iWuXs6XbJfXHhUTY7CYtfDFATmZC51jn717cy4uq3VQuzjJyfEqxtDMa-tWswXrnZS0j7FBEFdMA"
HEADERS = {'Authorization': f'Bearer {DHAN_API_TOKEN}'}
IST = pytz.timezone('Asia/Kolkata')

def fetch_fno_stocks():
    url = 'https://openapi.dhan.co/api/v1/market/instruments/fno'
    resp = requests.get(url, headers=HEADERS)
    resp.raise_for_status()
    data = resp.json()
    return [item['symbol'] for item in data['data'] if item['exchange'] == 'NSE']

def get_prev_trading_dates(days=16):
    today = datetime.now(IST).date()
    dates = []
    delta = 1
    while len(dates) < days:
        day = today - timedelta(days=delta)
        if day.weekday() < 5:  # Mon-Fri only
            dates.append(day.strftime('%Y-%m-%d'))
        delta += 1
    return dates[::-1]

def get_intraday_ohlcv(symbol, interval='1m', date=None):
    if date is None:
        date = datetime.now(IST).strftime('%Y-%m-%d')
    url = f'https://openapi.dhan.co/api/v1/market/chart/intraday/{symbol}/NSE/{interval}?date={date}'
    resp = requests.get(url, headers=HEADERS)
    if resp.status_code != 200:
        return None
    data = resp.json()
    return data.get('data')

def get_latest_quote(symbol):
    url = f'https://openapi.dhan.co/api/v1/market/quote/{symbol}/NSE'
    resp = requests.get(url, headers=HEADERS)
    if resp.status_code != 200:
        return None
    data = resp.json()
    return data.get('data')