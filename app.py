from fastapi import FastAPI
import threading
import time
from config.settings import config
from utils.logger import logger
from core.data_engine import data_engine
from core.trade_engine import trade_engine
from core.strategy_engine import strategy_engine
from core.risk_engine import risk_engine
from core.telegram_engine import telegram_engine

app = FastAPI(title="Pro Trading Bot SaaS Engine")

bot_running = False

def run_bot_loop():
    """২৪/৭ ব্যাকগ্রাউন্ড অটো-ট্রেডিং লুপ"""
    global bot_running
    bot_running = True
    logger.info("🚀 Background Trading Engine Started (24/7 Loop Active)...")
    
    # Deployment Notification to Telegram
    telegram_engine.send_alert("🌐 *SaaS Bot Engine Live on Cloud Server!*")

    while bot_running:
        try:
            # 1. Fetch Live Price
            price = data_engine.get_live_price("BTCUSDT")
            
            if price:
                # 2. Check Strategy Signal
                prices = [price * (1 + (i * 0.001)) for i in range(-20, 0)]
                signal = strategy_engine.generate_signal(prices)
                
                # 3. Execute Trade on Signal
                if signal == "BUY" and "BTCUSDT" not in trade_engine.positions:
                    trade_engine.execute_order("BTCUSDT", "BUY", price, 100.0)
                    telegram_engine.send_alert(f"🟢 *BUY Executed* at ${price}")
                
                # 4. Check Risk Management
                if "BTCUSDT" in trade_engine.positions:
                    pos = trade_engine.positions["BTCUSDT"]
                    action = risk_engine.check_exit_conditions(pos["entry_price"], price)
                    if action in ["SELL_STOP_LOSS", "SELL_TAKE_PROFIT"]:
                        trade_engine.execute_order("BTCUSDT", "SELL", price, pos["amount_usd"])
                        telegram_engine.send_alert(f"🔴 *Position Closed ({action})* at ${price}")

        except Exception as e:
            logger.error(f"Error in trading loop: {e}")

        time.sleep(30)

@app.on_event("startup")
def startup_event():
    thread = threading.Thread(target=run_bot_loop, daemon=True)
    thread.start()

@app.get("/")
def health_check():
    return {
        "status": "online",
        "system": "Pro Trading Bot SaaS",
        "environment": config.ENV
    }