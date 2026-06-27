import os
import yfinance as yf
import sqlite3
import pandas as pd
from db_setup import get_db_path, init_db

def fetch_financial_data(ticker: str, year: int):
    stock = yf.Ticker(ticker)
    
    try:
        bs = stock.balance_sheet
        inc = stock.income_stmt
        
        # yfinance columns are dates. We find the one corresponding to the year
        # Note: Depending on the fiscal year, we'll try to find the closest match.
        target_col = None
        for col in bs.columns:
            if str(year) in str(col):
                target_col = col
                break
                
        if target_col is None:
            # Fallback to the first available if not strictly year
            target_col = bs.columns[0]
            print(f"Warning: Exact year {year} not found for {ticker}, using latest {target_col}")

        # Extract needed fields (mapping yfinance keys)
        # Using basic try-get to avoid key errors
        def get_val(df, key):
            try:
                return float(df.loc[key, target_col])
            except Exception:
                return 0.0

        total_assets = get_val(bs, "TotalAssets")
        total_liabilities = get_val(bs, "TotalLiabilitiesNetMinorityInterest")
        current_assets = get_val(bs, "CurrentAssets")
        current_liabilities = get_val(bs, "CurrentLiabilities")
        total_equity = get_val(bs, "StockholdersEquity")
        retained_earnings = get_val(bs, "RetainedEarnings")
        ebit = get_val(inc, "EBIT")
        net_income = get_val(inc, "NetIncome")
        
        working_capital = current_assets - current_liabilities
        
        metrics = {
            "ticker": ticker.upper(),
            "year": year,
            "total_assets": total_assets,
            "total_liabilities": total_liabilities,
            "current_assets": current_assets,
            "current_liabilities": current_liabilities,
            "total_equity": total_equity,
            "retained_earnings": retained_earnings,
            "working_capital": working_capital,
            "ebit": ebit,
            "net_income": net_income
        }
        
        return metrics
    except Exception as e:
        print(f"Error fetching data for {ticker}: {e}")
        return None

def store_metrics(metrics: dict):
    if not metrics:
        return
        
    db_path = get_db_path()
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Upsert logic
    cursor.execute('''
    INSERT INTO financial_metrics 
    (ticker, year, total_assets, total_liabilities, current_assets, current_liabilities, total_equity, retained_earnings, working_capital, ebit, net_income)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ON CONFLICT(ticker, year) DO UPDATE SET
        total_assets=excluded.total_assets,
        total_liabilities=excluded.total_liabilities,
        current_assets=excluded.current_assets,
        current_liabilities=excluded.current_liabilities,
        total_equity=excluded.total_equity,
        retained_earnings=excluded.retained_earnings,
        working_capital=excluded.working_capital,
        ebit=excluded.ebit,
        net_income=excluded.net_income
    ''', (
        metrics["ticker"], metrics["year"], metrics["total_assets"], metrics["total_liabilities"],
        metrics["current_assets"], metrics["current_liabilities"], metrics["total_equity"],
        metrics["retained_earnings"], metrics["working_capital"], metrics["ebit"], metrics["net_income"]
    ))
    
    conn.commit()
    conn.close()
    print(f"Stored metrics for {metrics['ticker']} ({metrics['year']}) in SQLite")
    
if __name__ == "__main__":
    init_db()
    data = fetch_financial_data("AAPL", 2023)
    if data:
        store_metrics(data)
