from config.settings import config
from utils.logger import logger
from core.affiliate_engine import affiliate_engine

def start_app():
    logger.info("Initializing Pro Trading Bot SaaS Engine...")
    logger.info("Testing Affiliate & Local P2P Deposit System...")

    # Step 1: Link Referral
    affiliate_engine.register_referral(referrer_id="USER_AMIR_01", referee_id="USER_NEW_02")

    # Step 2: Process Deposit
    success, commission = affiliate_engine.process_p2p_deposit(
        user_id="USER_NEW_02", 
        amount_usd=100.0, 
        payment_trx_id="TRX9988776655"
    )

    if success:
        logger.info("✅ Lesson 9 Affiliate & Deposit Engine Working!")

if __name__ == "__main__":
    start_app()