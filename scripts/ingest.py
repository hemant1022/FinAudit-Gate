import argparse
import os
import sys

# Add parent dir to path to import src
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from src.edgar_tools import fetch_10k_html
from unstructured.partition.html import partition_html
from unstructured.documents.elements import Text, NarrativeText, Title

def parse_and_save(in_path: str, ticker: str, year: int):
    narratives_dir = os.path.join("data", "processed", "narratives")
    os.makedirs(narratives_dir, exist_ok=True)
    
    print(f"Parsing {in_path} using unstructured...")
    elements = partition_html(filename=in_path)
    
    narrative_path = os.path.join(narratives_dir, f"{ticker}_{year}_narrative.txt")
    
    with open(narrative_path, "w", encoding="utf-8") as nf:
        for element in elements:
            if isinstance(element, (NarrativeText, Title, Text)):
                # Skip tables, just dump text
                if not hasattr(element, "text_as_html"): # Simple heuristic to skip explicit tables if types overlap
                    nf.write(str(element) + "\n\n")
                
    print(f"Extraction complete! Narratives saved to {narrative_path}")

def main():
    parser = argparse.ArgumentParser(description="Ingest 10-K SEC filings")
    parser.add_argument("--ticker", type=str, required=True, help="Stock ticker (e.g., AAPL)")
    parser.add_argument("--years", type=int, required=True, help="Number of years to fetch")
    args = parser.parse_args()
    
    ticker = args.ticker.upper()
    current_year = 2023 # Standardized for project
    
    for i in range(args.years):
        year = current_year - i
        out_dir = os.path.join("data", "raw", ticker, str(year))
        
        print(f"--- Fetching {ticker} for {year} ---")
        out_path = fetch_10k_html(ticker, year, out_dir)
        if out_path:
            parse_and_save(out_path, ticker, year)

if __name__ == "__main__":
    main()
