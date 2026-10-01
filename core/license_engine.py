import datetime

class LicenseEngine:
    def __init__(self):
        # নমুনা লাইসেন্স ডাটাবেস (বাস্তবে এটি ডাটাবেসে থাকে)
        self.valid_keys = {
            "PRO-AMIR-2026": {"tier": "Pro", "expires": "2027-12-31"},
            "FREE-DEMO-123": {"tier": "Free", "expires": "2026-11-01"}
        }

    def verify_license(self, key: str) -> dict:
        """লাইসেন্স কি ভ্যালিড কি না তা যাচাই করে"""
        if key in self.valid_keys:
            data = self.valid_keys[key]
            expiry_date = datetime.datetime.strptime(data["expires"], "%Y-%m-%d").date()
            if expiry_date >= datetime.date.today():
                return {"status": True, "tier": data["tier"], "message": f"License Valid! Tier: {data['tier']}"}
            else:
                return {"status": False, "tier": "None", "message": "License Key has expired!"}
        return {"status": False, "tier": "None", "message": "Invalid License Key!"}

license_engine = LicenseEngine()