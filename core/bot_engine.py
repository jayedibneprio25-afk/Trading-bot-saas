import time
import requests
from core.license_engine import license_engine
from utils.telegram_engine import send_telegram_alert

class TradingBotEngine:
    def __init__(self, user_license_key: str):
        self.license_key = user_license_key
        self.is_running = False

    def start_bot(self):
        # ১. লাইসেন্স ভ্যালিডেশন চেক
        verification = license_engine.verify_license(self.license_key)
        
        if not verification["status"]:
            error_msg = f"🚫 Bot Startup Failed: {verification['message']}"
            print(error_msg)
            send_telegram_alert(error_msg)
            return False

        # ২. লাইসেন্স সঠিক হলে বট স্টার্ট হবে
        self.is_running = True
        success_msg = f"🚀 Bot Started Successfully! Active Tier: {verification['tier']}"
        print(success_msg)
        send_telegram_alert(success_msg)
        return True

    def run_trade_loop(self):
        if not self.is_running:
            return
        
        # ট্রেডিং লুপ এক্সিকিউশন
        print("📊 Running Market Analysis & Strategy Evaluation...")
        # এখানে তোমার পূর্বের ট্রেডিং লজিক ও অর্ডার এক্সিকিউশন চলবে

# টেস্ট করার জন্য ইনস্ট্যান্স তৈরি
bot_instance = TradingBotEngine(user_license_key="PRO-AMIR-2026")