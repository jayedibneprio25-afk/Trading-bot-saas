from fastapi import FastAPI
from pydantic import BaseModel
from datetime import datetime

app = FastAPI(title="Pro Trading Bot SaaS API")

# Central In-Memory Storage for API Server
VALID_LICENSES = {
    "PRO-AMIR-2026": {"tier": "Pro", "expires": "2027-12-31"},
    "PRO-TEST-2026": {"tier": "Pro", "expires": "2027-12-31"}
}

class LicenseModel(BaseModel):
    key: str
    tier: str
    expires: str

@app.get("/")
def home():
    return {"status": "Online", "message": "Pro Trading Bot SaaS API Engine Running!"}

# লাইসেন্স ভ্যালিডেশন
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

# ড্যাশবোর্ড থেকে কি যুক্ত করার এন্ডপয়েন্ট
@app.post("/add-license")
def add_new_license(data: LicenseModel):
    VALID_LICENSES[data.key] = {
        "tier": data.tier,
        "expires": data.expires
    }
    return {"status": True, "message": f"License key '{data.key}' added to active API memory!"}
    