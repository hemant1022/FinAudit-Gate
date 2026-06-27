import sqlite3
import os

def get_db_path():
    return os.path.join(os.path.dirname(__file__), "..", "financial_db.sqlite")

def init_db():
    db_path = get_db_path()
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Financial metrics table for easy exact calculation
    # Since we are using yfinance, we will extract key metrics per ticker and year
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS financial_metrics (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        ticker TEXT NOT NULL,
        year INTEGER NOT NULL,
        total_assets REAL,
        total_liabilities REAL,
        current_assets REAL,
        current_liabilities REAL,
        total_equity REAL,
        retained_earnings REAL,
        working_capital REAL,
        ebit REAL,
        net_income REAL,
        UNIQUE(ticker, year)
    )
    ''')
    
    conn.commit()
    conn.close()
    print(f"Database initialized at {db_path}")

if __name__ == "__main__":
    init_db()
