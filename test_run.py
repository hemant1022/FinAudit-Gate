from src.agents.analyst import run_analyst
from src.agents.auditor import run_auditor
from src.agents.manager import run_manager

def test_pipeline(ticker="AAPL", year=2023):
    print("="*50)
    print(f"STARTING PHASE 2 PROTOTYPE PIPELINE FOR {ticker} ({year})")
    print("="*50)
    
    analyst_report = run_analyst(ticker, year)
    print("\n[ANALYST OUTPUT]")
    print(analyst_report)
    
    print("\n" + "-"*50 + "\n")
    
    auditor_report = run_auditor(ticker, year)
    print("\n[AUDITOR OUTPUT]")
    print(auditor_report)
    
    print("\n" + "-"*50 + "\n")
    
    final_decision = run_manager(ticker, analyst_report, auditor_report)
    print("\n[LEAD MANAGER FINAL DECISION]")
    print(final_decision)
    
    print("\n" + "="*50)
    
if __name__ == "__main__":
    test_pipeline()
