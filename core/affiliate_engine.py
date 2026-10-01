from utils.logger import logger

class AffiliateDepositEngine:
    def __init__(self, commission_rate_pct=10.0):
        self.commission_rate_pct = commission_rate_pct
        self.referrals = {}

    def register_referral(self, referrer_id, referee_id):
        """নতুন ইউজারকে রেফারের সাথে যুক্ত করে"""
        self.referrals[referee_id] = referrer_id
        logger.info(f"👥 New Referral Linked: User {referee_id} referred by {referrer_id}")

    def process_p2p_deposit(self, user_id, amount_usd, payment_trx_id):
        """পেমেন্ট/ডিপোজিট ভ্যালিডেশন এবং কমিশনের হিসাব"""
        logger.info(f"💳 Deposit Request: ${amount_usd} by User {user_id} (TrxID: {payment_trx_id})")
        
        # Affiliate Commission Calculation
        if user_id in self.referrals:
            referrer = self.referrals[user_id]
            commission = (amount_usd * self.commission_rate_pct) / 100
            logger.info(f"🎁 Affiliate Commission Awarded: ${commission:.2f} to Referrer {referrer}")
            return True, commission
        
        return True, 0.0

affiliate_engine = AffiliateDepositEngine()