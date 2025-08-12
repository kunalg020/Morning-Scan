import pytz
from datetime import datetime
import pandas as pd

from dhan_api import fetch_fno_stocks, get_intraday_ohlcv, get_latest_quote, get_prev_trading_dates
from filters import *
from alerts import send_telegram_message

IST = pytz.timezone('Asia/Kolkata')

def pre_market_scan():
    fno_stocks = fetch_fno_stocks()
    alerts = []
    for symbol in fno_stocks:
        quote = get_latest_quote(symbol)
        if not quote:
            continue
        open_price = quote.get('open')
        prev_close = quote.get('previous_close')
        if open_price is None or prev_close is None:
            continue

        if is_gap_up(open_price, prev_close):
            alerts.append(f"🟢 Gap Up: {symbol} Open: {open_price} Prev Close: {prev_close}")
        elif is_gap_down(open_price, prev_close):
            alerts.append(f"🔴 Gap Down: {symbol} Open: {open_price} Prev Close: {prev_close}")

    if alerts:
        message = "*Pre-market Gap Scan Results:*\n" + "\n".join(alerts)
        send_telegram_message(message)
    else:
        send_telegram_message("No significant pre-market gaps detected today.")

def abnormal_1min_volume_scan():
    fno_stocks = fetch_fno_stocks()
    prev_dates = get_prev_trading_dates(16)

    alerts = []
    for symbol in fno_stocks:
        today_data = get_intraday_ohlcv(symbol, '1m')
        if not today_data:
            continue

        df_today = pd.DataFrame(today_data)
        df_today['timestamp'] = pd.to_datetime(df_today['time'])
        df_today.set_index('timestamp', inplace=True)
        df_today = df_today.sort_index()

        avg_volumes = {}
        for date in prev_dates:
            data = get_intraday_ohlcv(symbol, '1m', date)
            if not data:
                continue
            df_hist = pd.DataFrame(data)
            df_hist['timestamp'] = pd.to_datetime(df_hist['time'])
            df_hist.set_index('timestamp', inplace=True)
            for idx, row in df_hist.iterrows():
                t_str = idx.strftime('%H:%M')
                avg_volumes.setdefault(t_str, []).append(row['volume'])

        avg_vol_df = {k: sum(v)/len(v) for k, v in avg_volumes.items() if len(v) >= 10}

        for idx, row in df_today.iterrows():
            t_str = idx.strftime('%H:%M')
            avg_vol = avg_vol_df.get(t_str, 0)
            if abnormal_volume_1min(row['volume'], avg_vol):
                alerts.append(f"🔥 Abnormal 1-min Volume: {symbol} at {t_str} Vol: {row['volume']:.0f} Avg: {avg_vol:.0f}")

    if alerts:
        message = "*1-Minute Abnormal Volume Scan Results:*\n" + "\n".join(alerts)
        send_telegram_message(message)
    else:
        send_telegram_message("No abnormal 1-min volume detected.")

def intraday_indicators_scan():
    fno_stocks = fetch_fno_stocks()
    alerts = []
    for symbol in fno_stocks:
        data_5m = get_intraday_ohlcv(symbol, '5m')
        if not data_5m:
            continue

        df = pd.DataFrame(data_5m)
        df['timestamp'] = pd.to_datetime(df['time'])
        df.set_index('timestamp', inplace=True)
        df = df.sort_index()

        if len(df) < 14:
            continue

        df['EMA_21'] = calculate_ema(df['close'], 21)
        df['RSI_14'] = calculate_rsi(df['close'], 14)
        df['VWAP'] = calculate_vwap(df)

        latest = df.iloc[-1]
        price = latest['close']
        ema = latest['EMA_21']
        rsi = latest['RSI_14']
        vwap = latest['VWAP']

        if price_above_vwap(price, vwap) and rsi > 60:
            alerts.append(f"📈 Long Setup: {symbol} Price: {price} RSI: {rsi:.1f}")
        elif price_below_vwap(price, vwap) and rsi < 40:
            alerts.append(f"📉 Short Setup: {symbol} Price: {price} RSI: {rsi:.1f}")

    if alerts:
        message = "*Intraday Indicator Scan Results:*\n" + "\n".join(alerts)
        send_telegram_message(message)
    else:
        send_telegram_message("No intraday indicator setups detected.")

def main():
    pre_market_scan()
    abnormal_1min_volume_scan()
    intraday_indicators_scan()

if __name__ == '__main__':
    main()
