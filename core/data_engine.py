import requests
from utils.logger import logger

class DataEngine:
    def __init__(self):
        self.base_url = "https://api.binance.com/api/v3"

    def get_live_price(self, symbol="BTCUSDT"):
        """Binance থেকে লাইভ প্রাইস নিয়ে আসার ফাংশন"""
        try:
            url = f"{self.base_url}/ticker/price?symbol={symbol}"
            response = requests.get(url, timeout=5)
            if response.status_code == 200:
                data = response.json()
                price = float(data["price"])
                logger.info(f"Market Price fetched - {symbol}: ${price}")
                return price
            else:
                logger.error(f"Failed to fetch price for {symbol}")
                return None
        except Exception as e:
            logger.error(f"Error connecting to Binance API: {e}")
            return None

data_engine = DataEngine()