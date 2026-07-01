import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))

from src.vector_store import query_vector_store
from src.agents.llm_client import ask_llm

import json

def run_auditor(ticker: str, year: int, analyst_report: str = "") -> dict:
    query = f"What are the biggest macroeconomic, supply chain, and regulatory risks for {ticker}?"
    results = query_vector_store(query, ticker=ticker, section="Item 1A", n_results=5)
    
    if not results or not results["documents"] or not results["documents"][0]:
        context = f"No risk factors found in vector store for {ticker} {year}."
    else:
        context = "\n\n".join(results["documents"][0])
    
    system_prompt = (
        "You are a strict, pessimistic Risk Auditor at a top hedge fund. "
        "Your job is two-fold:\n"
        "1. Read the Analyst's Report. Validate it against these strict guardrails: "
        "missing metrics, hallucinated numbers, incorrect formatting, contradictory statements, or logically flawed conclusions.\n"
        "2. Read raw SEC 10-K Risk Factor excerpts (Item 1A) and summarize the top 3 most severe threats.\n\n"
        "You MUST output your response in strict JSON format with exactly three keys:\n"
        "- 'status': 'PASS' if the analyst report meets all guardrails, or 'FAIL' if it violates any.\n"
        "- 'feedback': If 'status' is 'FAIL', provide specific corrective feedback for the analyst. If 'PASS', write 'None'.\n"
        "- 'risk_report': A concise 1-paragraph summary of the top 3 threats from the SEC 10-K excerpts."
    )
    
    user_prompt = (
        f"Analyze {ticker} for the year {year}.\n\n"
        f"--- Analyst Report to Validate ---\n"
        f"{analyst_report}\n\n"
        f"--- Excerpts from Item 1A Risk Factors ---\n"
        f"{context}\n\n"
        f"Output strict JSON only. No markdown formatting like ```json."
    )
    
    print(f"--- Risk Auditor Agent auditing report and searching Vector DB for {ticker} ---")
    response_text = ask_llm(system_prompt, user_prompt)
    
    # Try to parse the JSON
    try:
        # Strip potential markdown formatting if the model still includes it
        clean_text = response_text.replace("```json", "").replace("```", "").strip()
        result = json.loads(clean_text)
        # Ensure required keys exist
        if not all(k in result for k in ['status', 'feedback', 'risk_report']):
            raise ValueError("Missing keys in JSON")
        return result
    except Exception as e:
        print(f"Failed to parse Auditor JSON output: {e}. Defaulting to FAIL.")
        return {
            "status": "FAIL",
            "feedback": f"Failed to parse your output correctly. Ensure it is valid JSON. Raw output: {response_text}",
            "risk_report": "Could not generate risk report due to formatting error."
        }

if __name__ == "__main__":
    res = run_auditor("AAPL", 2023, "Apple is doing great with infinite money and no debt.")
    print(res)
