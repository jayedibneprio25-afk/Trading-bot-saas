from fastapi import FastAPI
from pydantic import BaseModel
import requests

app = FastAPI(title="Pro Trading Bot Engine")

# --- In-Memory License Store ---
LICENSES = {
    "PRO-AMIR-2026": {"tier": "Pro", "expires": "2027-12-31"},
    "PRO-TEST-2026": {"tier": "Pro", "expires": "2027-12-31"}
}

# --- Virtual Portfolio (Paper Trading) ---
PORTFOLIO = {
    "balance_usdt": 10000.0,
    "btc_holdings": 0.0,
    "last_buy_price": 0.0
}

# --- Telegram Credentials ---
BOT_TOKEN = "YOUR_TELEGRAM_BOT_TOKEN"
CHAT_ID = "YOUR_TELEGRAM_CHAT_ID"

def send_telegram_alert(message: str):
    if not BOT_TOKEN or not CHAT_ID:
        print(f"[Telegram Alert]:\n{message}")
        return False

    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": CHAT_ID,
        "text": message,
        "parse_mode": "Markdown"
    }
    try:
        res = requests.post(url, json=payload)
        return res.status_code == 200
    except Exception as e:
        print(f"Telegram Send Error: {e}")
        return False

# --- Binance Historical Data for Analysis ---
def fetch_market_analysis():
    try:
        # Binance kline API (15m timeframe, last 30 candles)
        url = "https://api.binance.com/api/v3/klines?symbol=BTCUSDT&interval=15m&limit=30"
        data = requests.get(url).json()
        
        close_prices = [float(candle[4]) for candle in data]
        current_price = close_prices[-1]

        # Simple Moving Average (SMA - 20)
        sma_20 = sum(close_prices[-20:]) / 20

        # Simple RSI Calculation (14 period)
        gains, losses = [], []
        for i in range(1, 15):
            change = close_prices[-i] - close_prices[-i-1]
            if change >= 0:
                gains.append(change)
            else:
                losses.append(abs(change))
        
        avg_gain = (sum(gains) / 14) if gains else 0.001
        avg_loss = (sum(losses) / 14) if losses else 0.001
        rs = avg_gain / avg_loss
        rsi = 100 - (100 / (1 + rs))

        return {
            "price": current_price,
            "sma_20": round(sma_20, 2),
            "rsi": round(rsi, 2)
        }
    except Exception as e:
        print(f"Market Data Error: {e}")
        return {"price": 65000.0, "sma_20": 64800.0, "rsi": 50.0}

# --- API Endpoints ---

@app.get("/")
def home():
    return {"status": "Online", "message": "Pro Trading Bot Analysis Engine Active!"}

# ১. লাইভ মার্কেট টেকনিক্যাল এনালাইসিস
@app.get("/market-analysis")
def market_analysis():
    return fetch_market_analysis()

# ২. ট্রেডিং ইন্ডিকেটর নির্ভর স্মার্ট সিগন্যাল ও পেপার ট্রেড ট্রিগার
@app.post("/auto-trade/{license_key}")
def auto_trade(license_key: str):
    if license_key not in LICENSES:
        return {"status": False, "message": "Invalid License Key!"}

    analysis = fetch_market_analysis()
    price = analysis["price"]
    rsi = analysis["rsi"]
    sma = analysis["sma_20"]

    sl_price = round(price * 0.985, 2)  # 1.5% Stop Loss
    tp_price = round(price * 1.03, 2)   # 3.0% Take Profit

    # Trading Signal Strategy Logic
    signal = "NEUTRAL"
    if price > sma and rsi < 45:
        signal = "BUY"
    elif price < sma and rsi > 55:
        signal = "SELL"

    # Execute Trade Message
    if signal == "BUY":
        msg = (
            f"🎯 **AUTOMATED BUY SIGNAL**\n\n"
            f"🪙 **Symbol:** BTC/USDT\n"
            f"💵 **Entry Price:** ${price:,.2f}\n"
            f"📊 **RSI (14):** {rsi} | **SMA (20):** ${sma:,.2f}\n"
            f"🛑 **Stop Loss (1.5%):** ${sl_price:,.2f}\n"
            f"🎯 **Take Profit (3.0%):** ${tp_price:,.2f}\n"
            f"💼 **Strategy:** Trend Following + Oversold Dip"
        )
        send_telegram_alert(msg)
    elif signal == "SELL":
        msg = (
            f"⚠️ **AUTOMATED SELL SIGNAL**\n\n"
            f"🪙 **Symbol:** BTC/USDT\n"
            f"💵 **Exit Price:** ${price:,.2f}\n"
            f"📊 **RSI (14):** {rsi} | **SMA (20):** ${sma:,.2f}\n"
            f"💼 **Strategy:** Trend Breakdown"
        )
        send_telegram_alert(msg)

    return {
        "status": True,
        "signal": signal,
        "market_data": {
            "current_price": price,
            "sma_20": sma,
            "rsi": rsi
        },
        "risk_management": {
            "stop_loss": sl_price,
            "take_profit": tp_price
        }
    }