import requests

class TelegramNotifier:
    def __init__(self, bot_token: str = "", chat_id: str = ""):
        self.bot_token = bot_token
        self.chat_id = chat_id

    def send_message(self, message: str):
        if not self.bot_token or not self.chat_id:
            print(f"[Telegram Mock Alert]: {message}")
            return False

        url = f"https://api.telegram.org/bot{self.bot_token}/sendMessage"
        payload = {
            "chat_id": self.chat_id,
            "text": message,
            "parse_mode": "Markdown"
        }
        try:
            res = requests.post(url, json=payload)
            return res.status_code == 200
        except Exception as e:
            print(f"Failed to send Telegram message: {e}")
            return False

telegram_notifier = TelegramNotifier()