import requests

# Hardcoded Telegram Bot token and chat ID
TELEGRAM_BOT_TOKEN = "7876303846:AAHsuPJ9PKUSD1rGFM8o2puPQTS9yJ32H0Y"
CHAT_ID = 1051646958

def send_telegram_message(message: str):
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": CHAT_ID,
        "text": message,
        "parse_mode": "Markdown"
    }
    try:
        resp = requests.post(url, json=payload)
        resp.raise_for_status()
    except Exception as e:
        print(f"Failed to send Telegram message: {e}")