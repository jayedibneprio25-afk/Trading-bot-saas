import sqlite3
import os
from utils.logger import logger

DB_PATH = "trading_bot.db"

class DatabaseManager:
    def __init__(self):
        self.conn = sqlite3.connect(DB_PATH, check_same_thread=False)
        self.create_tables()

    def create_tables(self):
        """ডাটাবেসের টেবিলগুলো তৈরি করে"""
        cursor = self.conn.cursor()
        
        # User Settings Table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS settings (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                stop_loss REAL DEFAULT 2.0,
                take_profit REAL DEFAULT 4.0,
                trade_amount REAL DEFAULT 100.0
            )
        """)

        # Trade History Table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS trade_history (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                symbol TEXT,
                side TEXT,
                price REAL,
                pnl REAL,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        """)

        self.conn.commit()
        logger.info("Database tables verified/created successfully.")

    def save_trade(self, symbol, side, price, pnl=0.0):
        """ট্রেডের রেকর্ড সেভ করার ফাংশন"""
        cursor = self.conn.cursor()
        cursor.execute(
            "INSERT INTO trade_history (symbol, side, price, pnl) VALUES (?, ?, ?, ?)",
            (symbol, side, price, pnl)
        )
        self.conn.commit()
        logger.info(f"Saved trade to database: {side} {symbol} at ${price}")

db = DatabaseManager()