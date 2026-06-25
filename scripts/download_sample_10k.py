import os
import requests

def download_aapl_10k_2023():
    # Apple's CIK: 320193. 10-K filed in Nov 2023 for FY 2023
    url = "https://www.sec.gov/Archives/edgar/data/320193/000032019323000106/aapl-20230930.htm"
    
    headers = {
        "User-Agent": "FinAudit-Gate Research Project (student@example.com)"
    }
    
    print(f"Downloading AAPL 2023 10-K from {url}...")
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    
    # Save to data/raw/AAPL/2023/
    out_dir = os.path.join("data", "raw", "AAPL", "2023")
    os.makedirs(out_dir, exist_ok=True)
    
    out_path = os.path.join(out_dir, "10k.htm")
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(response.text)
        
    print(f"Successfully downloaded 10-K to {out_path}")

if __name__ == "__main__":
    download_aapl_10k_2023()
