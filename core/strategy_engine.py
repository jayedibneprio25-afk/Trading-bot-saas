from utils.logger import logger

class StrategyEngine:
    def __init__(self, short_window=5, long_window=20):
        self.short_window = short_window
        self.long_window = long_window

    def generate_signal(self, price_history):
        """
        ক্যান্ডেল/প্রাইস হিস্ট্রি থেকে ইন্ডিকেটর হিসাব করে সিগন্যাল তৈরি করে।
        BUY: Short Average > Long Average
        SELL: Short Average < Long Average
        """
        if len(price_history) < self.long_window:
            logger.info("Not enough market data to calculate moving averages.")
            return "HOLD"

        short_sma = sum(price_history[-self.short_window:]) / self.short_window
        long_sma = sum(price_history[-self.long_window:]) / self.long_window

        logger.info(f"SMA Analysis -> Short SMA({self.short_window}): {short_sma:.2f} | Long SMA({self.long_window}): {long_sma:.2f}")

        if short_sma > long_sma:
            return "BUY"
        elif short_sma < long_sma:
            return "SELL"
        else:
            return "HOLD"

strategy_engine = StrategyEngine()