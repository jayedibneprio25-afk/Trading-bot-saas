import hashlib
from utils.logger import logger

class SecurityEngine:
    def __init__(self, valid_license_key="PRO-SAAS-2026-KEY"):
        self.valid_license_key = valid_license_key

    def verify_license(self, user_key):
        """লাইসেন্স কি ভ্যালিডেশন চেক"""
        if user_key == self.valid_license_key:
            logger.info("🔑 License Verification Successful! Access Granted.")
            return True
        else:
            logger.error("❌ Invalid License Key! Access Denied.")
            return False

    def generate_hwid_hash(self, machine_id="USER-PC-001"):
        """ডিভাইস লক বা HWID এনক্রিপশন হ্যাশ তৈরি"""
        hwid_hash = hashlib.sha256(machine_id.encode()).hexdigest()
        logger.info(f"🔒 Encrypted HWID Hash generated: {hwid_hash[:16]}...")
        return hwid_hash

security_engine = SecurityEngine()