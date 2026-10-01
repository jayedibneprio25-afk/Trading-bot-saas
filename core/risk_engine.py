from utils.logger import logger

class RiskEngine:
    def __init__(self, stop_loss_pct=2.0, take_profit_pct=4.0):
        self.stop_loss_pct = stop_loss_pct
        self.take_profit_pct = take_profit_pct

    def check_exit_conditions(self, entry_price, current_price):
        """
        স্টপ-লাস ও টেক-প্রফিট কন্ডিশন চেক করে
        """
        pnl_pct = ((current_price - entry_price) / entry_price) * 100

        if pnl_pct <= -self.stop_loss_pct:
            logger.warning(f"⚠️ STOP LOSS TRIGGERED! PnL: {pnl_pct:.2f}% (Limit: -{self.stop_loss_pct}%)")
            return "SELL_STOP_LOSS"
        elif pnl_pct >= self.take_profit_pct:
            logger.info(f"🎯 TAKE PROFIT TRIGGERED! PnL: {pnl_pct:.2f}% (Target: +{self.take_profit_pct}%)")
            return "SELL_TAKE_PROFIT"
        
        return "HOLD"

risk_engine = RiskEngine()