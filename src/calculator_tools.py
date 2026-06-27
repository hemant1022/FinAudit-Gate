import sqlite3
import os
from db_setup import get_db_path

def get_metrics(ticker: str, year: int):
    db_path = get_db_path()
    if not os.path.exists(db_path):
        return None
        
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    cursor.execute('''
    SELECT total_assets, total_liabilities, current_assets, current_liabilities, total_equity, retained_earnings, working_capital, ebit, net_income
    FROM financial_metrics
    WHERE ticker = ? AND year = ?
    ''', (ticker.upper(), year))
    
    row = cursor.fetchone()
    conn.close()
    
    if not row:
        return None
        
    return {
        "total_assets": row[0],
        "total_liabilities": row[1],
        "current_assets": row[2],
        "current_liabilities": row[3],
        "total_equity": row[4],
        "retained_earnings": row[5],
        "working_capital": row[6],
        "ebit": row[7],
        "net_income": row[8]
    }

def calc_debt_to_equity(ticker: str, year: int):
    metrics = get_metrics(ticker, year)
    if not metrics or metrics["total_equity"] == 0:
        return None
    return metrics["total_liabilities"] / metrics["total_equity"]

def calc_current_ratio(ticker: str, year: int):
    metrics = get_metrics(ticker, year)
    if not metrics or metrics["current_liabilities"] == 0:
        return None
    return metrics["current_assets"] / metrics["current_liabilities"]

def calc_altman_z_score(ticker: str, year: int):
    """
    Altman Z-Score = 1.2A + 1.4B + 3.3C + 0.6D + 1.0E
    A = Working Capital / Total Assets
    B = Retained Earnings / Total Assets
    C = EBIT / Total Assets
    D = Market Value of Equity / Total Liabilities
    E = Sales / Total Assets (Using Net Income / Total Assets as proxy if Sales not extracted)
    
    Note: For a precise Z-Score, Sales is needed, but we'll use Net Income for the prototype if Sales is missing.
    Also, Market Value of Equity is typically calculated from stock price * shares. 
    We will use Book Value of Equity (total_equity) as a simplified proxy for this prototype.
    """
    metrics = get_metrics(ticker, year)
    if not metrics or metrics["total_assets"] == 0 or metrics["total_liabilities"] == 0:
        return None
        
    A = metrics["working_capital"] / metrics["total_assets"]
    B = metrics["retained_earnings"] / metrics["total_assets"]
    C = metrics["ebit"] / metrics["total_assets"]
    D = metrics["total_equity"] / metrics["total_liabilities"] # Using book equity as proxy
    E = metrics["net_income"] / metrics["total_assets"] # Using net income as proxy for sales
    
    return 1.2*A + 1.4*B + 3.3*C + 0.6*D + 1.0*E

if __name__ == "__main__":
    ticker = "AAPL"
    year = 2023
    print(f"Metrics for {ticker} ({year}):")
    print(f"D/E Ratio: {calc_debt_to_equity(ticker, year)}")
    print(f"Current Ratio: {calc_current_ratio(ticker, year)}")
    print(f"Altman Z-Score: {calc_altman_z_score(ticker, year)}")
