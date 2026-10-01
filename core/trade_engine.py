from utils.logger import logger

class TradeEngine:
    def __init__(self, initial_balance=1000.0):
        self.balance = initial_balance
        self.positions = {}

    def execute_order(self, symbol, side, price, amount_usd):
        """ভার্চুয়াল অর্ডার এক্সিকিউশন সিস্টেম"""
        if side.upper() == "BUY":
            if self.balance < amount_usd:
                logger.error(f"Insufficient funds to BUY {symbol}. Balance: ${self.balance}")
                return False
            
            quantity = amount_usd / price
            self.balance -= amount_usd
            self.positions[symbol] = {
                "entry_price": price,
                "quantity": quantity,
                "amount_usd": amount_usd
            }
            logger.info(f"🟢 BUY ORDER EXECUTED: {symbol} at ${price} | Qty: {quantity:.6f} | Remaining Bal: ${self.balance:.2f}")
            return True

        elif side.upper() == "SELL":
            if symbol not in self.positions:
                logger.error(f"No active position found for {symbol} to SELL.")
                return False

            pos = self.positions.pop(symbol)
            pnl = (price - pos["entry_price"]) * pos["quantity"]
            self.balance += (pos["amount_usd"] + pnl)
            
            pnl_str = f"+${pnl:.2f}" if pnl >= 0 else f"-${abs(pnl):.2f}"
            logger.info(f"🔴 SELL ORDER EXECUTED: {symbol} at ${price} | PnL: {pnl_str} | New Bal: ${self.balance:.2f}")
            return True

trade_engine = TradeEngine()