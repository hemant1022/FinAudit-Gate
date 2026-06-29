import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))

from src.calculator_tools import get_metrics, calc_debt_to_equity, calc_current_ratio, calc_altman_z_score
from src.agents.llm_client import ask_llm

def run_analyst(ticker: str, year: int) -> str:
    metrics = get_metrics(ticker, year)
    if not metrics:
        return f"No financial metrics found for {ticker} in {year}."
        
    de_ratio = calc_debt_to_equity(ticker, year)
    current_ratio = calc_current_ratio(ticker, year)
    z_score = calc_altman_z_score(ticker, year)
    
    system_prompt = (
        "You are a highly skilled Financial Analyst at a top hedge fund. "
        "Your job is to read raw financial metrics and produce a concise, professional 1-paragraph summary "
        "evaluating the company's financial health, liquidity, and solvency."
    )
    
    user_prompt = (
        f"Analyze {ticker} for the year {year}.\n\n"
        f"Metrics:\n"
        f"- Total Assets: {metrics['total_assets']}\n"
        f"- Total Liabilities: {metrics['total_liabilities']}\n"
        f"- Debt-to-Equity Ratio: {de_ratio:.2f} (Calculated)\n"
        f"- Current Ratio: {current_ratio:.2f} (Calculated)\n"
        f"- Altman Z-Score: {z_score:.2f} (Calculated)\n\n"
        f"Provide a 1-paragraph summary of their financial health."
    )
    
    print(f"--- Analyst Agent analyzing quantitative metrics for {ticker} ---")
    return ask_llm(system_prompt, user_prompt)

if __name__ == "__main__":
    print(run_analyst("AAPL", 2023))
