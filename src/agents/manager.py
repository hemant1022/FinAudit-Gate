import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))

from src.agents.llm_client import ask_llm

def run_manager(ticker: str, analyst_report: str, auditor_report: str) -> str:
    system_prompt = (
        "You are the Lead Portfolio Manager at a top hedge fund. "
        "You will receive an optimistic financial health report from your Financial Analyst, "
        "and a pessimistic risk warning from your Risk Auditor. "
        "Your job is to synthesize both viewpoints, make a final portfolio decision (BUY, HOLD, or SELL), "
        "and justify it in exactly 3-4 sentences."
    )
    
    user_prompt = (
        f"Portfolio Decision required for: {ticker}\n\n"
        f"--- Analyst Report (Optimistic) ---\n{analyst_report}\n\n"
        f"--- Auditor Report (Pessimistic) ---\n{auditor_report}\n\n"
        f"What is your final decision?"
    )
    
    print(f"--- Lead Manager Agent synthesizing final decision for {ticker} ---")
    return ask_llm(system_prompt, user_prompt, model="gemini-2.5-pro")

if __name__ == "__main__":
    # dummy test
    print(run_manager("AAPL", "Great financials.", "Terrible risks."))
