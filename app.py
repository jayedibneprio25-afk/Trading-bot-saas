from fastapi import FastAPI
from pydantic import BaseModel
from datetime import datetime
import requests
from supabase import create_client, Client

app = FastAPI(title="Pro Trading Bot SaaS API")

# --- Supabase Credentials ---
SUPABASE_URL = "https://zvzbbhjzesubyxbknxd.supabase.co"
SUPABASE_KEY = "sb_publishable_7vsvBnouIM1bFkYkHX_dYg_vkgan5EO"  # Supabase Publishable Key purota boshao

# Supabase Client Initialization
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

# --- Telegram Credentials ---
BOT_TOKEN = "8615449265:AAEVgIIdI-ZkneGlOfNP30QfsgPrymqa5_Y"  # Tomar Telegram Bot Token
CHAT_ID = "6819917637"      # Tomar Telegram Chat ID

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
    return {"status": "Online", "message": "Pro Trading Bot SaaS API Engine Running with Supabase DB!"}

# 1. License Validation (Supabase DB)
@app.get("/verify-license/{license_key}")
def verify_license(license_key: str):
    try:
        response = supabase.table("licenses").select("*").eq("key", license_key).execute()
        data = response.data

        if not data:
            return {"status": False, "tier": "None", "message": "Invalid License Key!"}

        lic_data = data[0]
        tier = lic_data["tier"]
        expires_str = str(lic_data["expires"])

        expiry_date = datetime.strptime(expires_str, "%Y-%m-%d")
        if datetime.now() > expiry_date:
            return {"status": False, "tier": tier, "message": f"License Key Expired on {expires_str}"}

        return {"status": True, "tier": tier, "message": f"License Valid! Tier: {tier}"}
    except Exception as e:
        return {"status": False, "tier": "None", "message": f"Database Error: {str(e)}"}

# 2. Add License Endpoint (Supabase DB)
@app.post("/add-license")
def add_new_license(data: LicenseModel):
    try:
        payload = {
            "key": data.key,
            "tier": data.tier,
            "expires": data.expires
        }
        supabase.table("licenses").upsert(payload).execute()
        return {"status": True, "message": f"License key '{data.key}' permanently saved to Supabase!"}
    except Exception as e:
        return {"status": False, "message": f"Database Error: {str(e)}"}

# 3. Trade Trigger & Telegram Alert Endpoint
@app.post("/trigger-trade/{license_key}/{action}")
def trigger_trade(license_key: str, action: str):
    val_res = verify_license(license_key)
    if not val_res["status"]:
        return {"status": False, "message": "Unauthorized! Invalid or expired license key."}

    price = fetch_btc_price()
    action_upper = action.upper()

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