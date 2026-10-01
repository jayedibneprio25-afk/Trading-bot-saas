from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import sqlite3
from datetime import datetime

app = FastAPI(title="Pro Trading Bot SaaS API")

DB_NAME = "trading_bot.db"

# ১. ডাটাবেস ও টেবিল স্বয়ংক্রিয়ভাবে তৈরি করার ফাংশন
def init_db():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    
    # trade_history টেবিল
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS trade_history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            symbol TEXT,
            action TEXT,
            price REAL,
            amount REAL,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # licenses টেবিল
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS licenses (
            key TEXT PRIMARY KEY,
            tier TEXT,
            expires TEXT
        )
    ''')
    
    # প্রাথমিক টেস্ট কি
    cursor.execute('''
        INSERT OR IGNORE INTO licenses (key, tier, expires)
        VALUES ('PRO-AMIR-2026', 'Pro', '2027-12-31')
    ''')
    
    conn.commit()
    conn.close()

# অ্যাপ চালুর সময় ডাটাবেস ইনিশিয়ালাইজেশন
init_db()


# ২. ডাটা মডেল (Pydantic)
class LicenseModel(BaseModel):
    key: str
    tier: str
    expires: str


# ৩. রুট এপিআই (Root Route)
@app.get("/")
def home():
    return {"status": "Online", "message": "Pro Trading Bot SaaS API Engine Running!"}


# ৪. লাইসেন্স ভ্যালিডেশন করার এন্ডপয়েন্ট
@app.get("/verify-license/{license_key}")
def verify_license(license_key: str):
    init_db()
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    
    cursor.execute("SELECT tier, expires FROM licenses WHERE key = ?", (license_key,))
    row = cursor.fetchone()
    conn.close()

    if not row:
        return {"status": False, "tier": "None", "message": "Invalid License Key!"}

    tier, expires_str = row
    try:
        expiry_date = datetime.strptime(expires_str, "%Y-%m-%d")
        if datetime.now() > expiry_date:
            return {"status": False, "tier": tier, "message": f"License Key Expired on {expires_str}"}
    except ValueError:
        pass

    return {"status": True, "tier": tier, "message": f"License Valid! Tier: {tier}"}


# ৫. ড্যাশবোর্ড থেকে নতুন লাইসেন্স সেভ/আপডেট করার এন্ডপয়েন্ট
@app.post("/add-license")
def add_new_license(data: LicenseModel):
    init_db()
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    
    cursor.execute('''
        INSERT INTO licenses (key, tier, expires)
        VALUES (?, ?, ?)
        ON CONFLICT(key) DO UPDATE SET
            tier = excluded.tier,
            expires = excluded.expires
    ''', (data.key, data.tier, data.expires))
    
    conn.commit()
    conn.close()
    
    return {"status": True, "message": f"License key '{data.key}' successfully saved to database."}