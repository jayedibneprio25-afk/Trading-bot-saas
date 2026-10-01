from fastapi import FastAPI
from pydantic import BaseModel
from datetime import datetime
import requests

app = FastAPI(title="Pro Trading Bot SaaS API")

# Central In-Memory Storage for API Server
VALID_LICENSES = {
    "PRO-AMIR-2026": {"tier": "Pro", "expires": "2027-12-31"},
    "PRO-TEST-2026": {"tier": "Pro", "expires": "2027-12-31"}
}

# --- Telegram Notifier Helper ---
BOT_TOKEN = ""  # BotFather থেকে পাওয়া টোকেন এখানে দিতে পারো
CHAT_ID = ""    # userinfobot থেকে পাওয়া আইডি এখানে দিতে পারো

def send_telegram_alert(message: str):
    if not BOT_TOKEN or not CHAT_ID:
        print(f"[Telegram Mock Alert]: {message}")
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
        print(f"Failed to send Telegram message: {e}")
        return False

# --- Paper Trading Helper ---
def fetch_btc_price() -> float:
    try:
        url = "https://api.binance.com/api/v3/ticker/price?symbol=BTCUSDT"
        res = requests.get(url).json()
        return float(res["price"])
    except Exception:
        return 65000.0

# --- Pydantic Data Model ---
class LicenseModel(BaseModel):
    key: str
    tier: str
    expires: str

# --- API Endpoints ---

@app.get("/")
def home():
    return {"status": "Online", "message": "Pro Trading Bot SaaS API Engine Running!"}

# ১. লাইসেন্স ভ্যালিডেশন
@app.get("/verify-license/{license_key}")
def verify_license(license_key: str):
    if license_key not in VALID_LICENSES:
        return {"status": False, "tier": "None", "message": "Invalid License Key!"}

    lic_data = VALID_LICENSES[license_key]
    tier = lic_data["tier"]
    expires_str = lic_data["expires"]

    try:
        expiry_date = datetime.strptime(expires_str, "%Y-%m-%d")
        if datetime.now() > expiry_date:
            return {"status": False, "tier": tier, "message": f"License Key Expired on {expires_str}"}
    except ValueError:
        pass

    return {"status": True, "tier": tier, "message": f"License Valid! Tier: {tier}"}

# ২. ড্যাশবোর্ড থেকে লাইসেন্স যোগ করার এন্ডপয়েন্ট
@app.post("/add-license")
def add_new_license(data: LicenseModel):
    VALID_LICENSES[data.key] = {
        "tier": data.tier,
        "expires": data.expires
    }
    return {"status": True, "message": f"License key '{data.key}' added to active API memory!"}

# ৩. ট্রেড ট্রিগার ও টেলিগ্রাম অ্যালার্ট এন্ডপয়েন্ট
@app.post("/trigger-trade/{license_key}/{action}")
def trigger_trade(license_key: str, action: str):
    # লাইসেন্স চেক
    val_res = verify_license(license_key)
    if not val_res["status"]:
        return {"status": False, "message": "Unauthorized! Invalid or expired license key."}

    # বাই/সেল প্রাইস ফেচ
    price = fetch_btc_price()
    action_upper = action.upper()

    # নোটিফিকেশন মেসেজ ফরম্যাট
    if action_upper == "BUY":
        msg = (
            f"🚀 **BUY SIGNAL EXECUTED**\n\n"
            f"🔑 **License:** `{license_key}`\n"
            f"🪙 **Symbol:** BTC/USDT\n"
            f"💵 **Price:** ${price:,.2f}\n"
            f"💼 **Status:** Paper Trade Executed"
        )
    else:
        msg = (
            f"🔻 **SELL SIGNAL EXECUTED**\n\n"
            f"🔑 **License:** `{license_key}`\n"
            f"🪙 **Symbol:** BTC/USDT\n"
            f"💵 **Price:** ${price:,.2f}\n"
            f"💼 **Status:** Paper Trade Executed"
        )

    # টেলিগ্রামে মেসেজ পাঠানো
    send_telegram_alert(msg)

    return {
        "status": True,
        "message": f"{action_upper} trade executed successfully!",
        "data": {
            "license_key": license_key,
            "action": action_upper,
            "symbol": "BTCUSDT",
            "price": price
        }
    }