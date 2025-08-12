import pandas as pd
import numpy as np

def is_gap_up(open_price, prev_close, threshold=0.013):
    return (open_price - prev_close) / prev_close >= threshold

def is_gap_down(open_price, prev_close, threshold=0.013):
    return (prev_close - open_price) / prev_close >= threshold

def abnormal_volume_1min(current_vol, avg_vol, factor=2):
    if avg_vol == 0:
        return False
    return current_vol >= avg_vol * factor

def calculate_ema(series, period):
    return series.ewm(span=period, adjust=False).mean()

def calculate_rsi(series, period):
    delta = series.diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=period).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=period).mean()
    rs = gain / loss
    rsi = 100 - (100 / (1 + rs))
    return rsi

def calculate_vwap(df):
    cum_vol = df['volume'].cumsum()
    cum_vol_price = (df['close'] * df['volume']).cumsum()
    return cum_vol_price / cum_vol

def price_above_vwap(price, vwap):
    return price > vwap

def price_below_vwap(price, vwap):
    return price < vwap