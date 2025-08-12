# Market Scanner - Hardcoded Version

This project performs automated scans on F&O stocks using Dhan API and sends Telegram alerts for:

- Pre-market gap ups/downs
- Abnormal 1-minute volume
- Intraday indicator setups (EMA, RSI, VWAP)

## Setup

1. Install dependencies:

```bash
pip install -r requirements.txt
```

2. The API tokens and Telegram bot credentials are **hardcoded** in the scripts for ease of use.

3. Run the scanner:

```bash
python3 scanner.py
```

## Files

- `dhan_api.py` — Contains Dhan API interaction functions with hardcoded token
- `alerts.py` — Telegram messaging utility with hardcoded bot token & chat ID
- `filters.py` — Contains scan filter functions and indicator calculations
- `scanner.py` — Main script running all scans and sending alerts