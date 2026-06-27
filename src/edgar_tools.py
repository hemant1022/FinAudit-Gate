import os
import requests
import json
from typing import Optional

USER_AGENT = "FinAudit-Gate Research Project (student@example.com)"

def get_cik_for_ticker(ticker: str) -> Optional[str]:
    url = "https://www.sec.gov/files/company_tickers.json"
    headers = {"User-Agent": USER_AGENT}
    resp = requests.get(url, headers=headers)
    resp.raise_for_status()
    data = resp.json()
    
    ticker = ticker.upper()
    for key, value in data.items():
        if value["ticker"] == ticker:
            return str(value["cik_str"]).zfill(10)
    return None

def fetch_10k_html(ticker: str, year: int, out_dir: str) -> Optional[str]:
    cik = get_cik_for_ticker(ticker)
    if not cik:
        print(f"Could not find CIK for {ticker}")
        return None
        
    submissions_url = f"https://data.sec.gov/submissions/CIK{cik}.json"
    headers = {"User-Agent": USER_AGENT}
    
    resp = requests.get(submissions_url, headers=headers)
    resp.raise_for_status()
    sub_data = resp.json()
    
    filings = sub_data.get("filings", {}).get("recent", {})
    if not filings:
        return None
        
    for i in range(len(filings["form"])):
        if filings["form"][i] == "10-K":
            filing_date = filings["filingDate"][i]
            if filing_date.startswith(str(year)):
                accession_num = filings["accessionNumber"][i]
                primary_doc = filings["primaryDocument"][i]
                
                accession_no_dashes = accession_num.replace("-", "")
                # The SEC url uses the CIK without leading zeros
                doc_url = f"https://www.sec.gov/Archives/edgar/data/{int(cik)}/{accession_no_dashes}/{primary_doc}"
                
                print(f"Downloading 10-K for {ticker} ({year}) from {doc_url}")
                doc_resp = requests.get(doc_url, headers=headers)
                doc_resp.raise_for_status()
                
                os.makedirs(out_dir, exist_ok=True)
                out_path = os.path.join(out_dir, "10k.htm")
                with open(out_path, "w", encoding="utf-8") as f:
                    f.write(doc_resp.text)
                
                return out_path
    
    print(f"No 10-K found for {ticker} in year {year}")
    return None
