import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))

from src.vector_store import query_vector_store
from src.agents.llm_client import ask_llm

def run_auditor(ticker: str, year: int) -> str:
    query = f"What are the biggest macroeconomic, supply chain, and regulatory risks for {ticker}?"
    results = query_vector_store(query, ticker=ticker, section="Item 1A", n_results=5)
    
    if not results or not results["documents"] or not results["documents"][0]:
        return f"No risk factors found in vector store for {ticker} {year}."
        
    context = "\n\n".join(results["documents"][0])
    
    system_prompt = (
        "You are a strict, pessimistic Risk Auditor at a top hedge fund. "
        "Your job is to read raw SEC 10-K Risk Factor excerpts (Item 1A) and produce a concise, 1-paragraph summary "
        "highlighting the top 3 most severe threats to the company's business model."
    )
    
    user_prompt = (
        f"Analyze {ticker} for the year {year}.\n\n"
        f"Excerpts from Item 1A Risk Factors:\n{context}\n\n"
        f"Provide a 1-paragraph summary of the top threats."
    )
    
    print(f"--- Risk Auditor Agent searching Vector DB for {ticker} ---")
    return ask_llm(system_prompt, user_prompt)

if __name__ == "__main__":
    print(run_auditor("AAPL", 2023))
