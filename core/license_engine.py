import sqlite3
from datetime import datetime

class LicenseEngine:
    def __init__(self, db_name="trading_bot.db"):
        self.db_name = db_name

    def verify_license(self, license_key: str) -> dict:
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        
        cursor.execute("SELECT tier, expires FROM licenses WHERE key = ?", (license_key,))
        row = cursor.fetchone()
        conn.close()

        if not row:
            return {"status": False, "tier": "None", "message": "Invalid License Key!"}

        tier, expires_str = row
        expiry_date = datetime.strptime(expires_str, "%Y-%m-%d")
        
        if datetime.now() > expiry_date:
            return {"status": False, "tier": tier, "message": f"License Key Expired on {expires_str}"}

        return {"status": True, "tier": tier, "message": f"License Valid! Tier: {tier}"}

    def add_or_update_license(self, key: str, tier: str, expires: str):
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO licenses (key, tier, expires)
            VALUES (?, ?, ?)
            ON CONFLICT(key) DO UPDATE SET
                tier = excluded.tier,
                expires = excluded.expires
        ''', (key, tier, expires))
        conn.commit()
        conn.close()

    def get_all_licenses(self) -> dict:
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        cursor.execute("SELECT key, tier, expires FROM licenses")
        rows = cursor.fetchall()
        conn.close()
        
        licenses = {}
        for row in rows:
            licenses[row[0]] = {"tier": row[1], "expires": row[2]}
        return licenses

license_engine = LicenseEngine()