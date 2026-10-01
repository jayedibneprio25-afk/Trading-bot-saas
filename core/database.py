import sqlite3

DB_NAME = "trading_bot.db"

def init_db():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    
    # ১. trade_history টেবিল
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
    
    # ২. licenses টেবিল
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS licenses (
            key TEXT PRIMARY KEY,
            tier TEXT,
            expires TEXT
        )
    ''')
    
    # ডিফল্ট টেস্ট লাইসেন্স ঢুকিয়ে রাখা
    cursor.execute('''
        INSERT OR IGNORE INTO licenses (key, tier, expires)
        VALUES ('PRO-AMIR-2026', 'Pro', '2027-12-31')
    ''')
    
    conn.commit()
    conn.close()

init_db()