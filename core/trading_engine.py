import requests
from core.telegram_notifier import telegram_notifier

class PaperTradingEngine:
    def __init__(self, initial_balance=1000.0):
        self.balance = initial_balance
        self.position = None

    def fetch_btc_price(self) -> float:
        try:
            # Binance Public API থেকে স্পট প্রাইস নেওয়া
            url = "https://api.binance.com/api/v3/ticker/price?symbol=BTCUSDT"
            res = requests.get(url).json()
            return float(res["price"])
        except Exception:
            return 65000.0  # Fallback price

    def execute_paper_trade(self, action: str, license_key: str):
        price = self.fetch_btc_price()
        
        if action.upper() == "BUY":
            msg = (
                f"🚀 **BUY SIGNAL EXECUTED**\n\n"
                f"🔑 **License:** `{license_key}`\n"
                f"🪙 **Symbol:** BTC/USDT\n"
                f"💵 **Price:** ${price:,.2f}\n"
                f"💼 **Paper Balance:** ${self.balance:,.2f}"
            )
        else:
            msg = (
                f"🔻 **SELL SIGNAL EXECUTED**\n\n"
                f"🔑 **License:** `{license_key}`\n"
                f"🪙 **Symbol:** BTC/USDT\n"
                f"💵 **Price:** ${price:,.2f}\n"
                f"💼 **Paper Balance:** ${self.balance:,.2f}"
            )

        # টেলিগ্রাম নোটিফিকেশন পাঠানো
        telegram_notifier.send_message(msg)
        return {"status": True, "action": action, "symbol": "BTCUSDT", "price": price}

trading_engine = PaperTradingEngine()