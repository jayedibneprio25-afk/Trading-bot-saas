import requests
from config.settings import config
from utils.logger import logger

class TelegramEngine:
    def __init__(self):
        self.bot_token = config.BOT_TOKEN
        self.chat_id = config.CHAT_ID
        self.base_url = f"https://api.telegram.org/bot{self.bot_token}"

    def send_alert(self, message: str):
        """টেলিগ্রামে রিয়েল-টাইম নোটিফিকেশন/অ্যালার্ট পাঠানোর ফাংশন"""
        if not self.bot_token or not self.chat_id:
            logger.error("Telegram Credentials missing in config!")
            return False

        try:
            url = f"{self.base_url}/sendMessage"
            payload = {
                "chat_id": self.chat_id,
                "text": message,
                "parse_mode": "Markdown"
            }
            response = requests.post(url, json=payload, timeout=5)
            if response.status_code == 200:
                logger.info("📱 Telegram alert sent successfully!")
                return True
            else:
                logger.error(f"Failed to send Telegram alert: {response.text}")
                return False
        except Exception as e:
            logger.error(f"Error sending Telegram alert: {e}")
            return False

telegram_engine = TelegramEngine()