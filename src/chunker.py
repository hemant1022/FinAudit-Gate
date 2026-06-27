import os
import re
import json

def extract_sections(text):
    # Very basic regex to find Item 1A and Item 7
    # Note: SEC filings are messy, this is a simplified heuristic
    
    item_1a_pattern = r"(?i)(Item\s+1A\.\s*Risk\s+Factors)(.*?)(?=Item\s+1B\.\s*Unresolved|Item\s+2\.\s*Properties)"
    item_7_pattern = r"(?i)(Item\s+7\.\s*Management['’]?s\s+Discussion\s+and\s+Analysis)(.*?)(?=Item\s+7A\.\s*Quantitative)"
    
    sections = {}
    
    m1a = re.search(item_1a_pattern, text, re.DOTALL)
    if m1a:
        sections["Item 1A"] = m1a.group(2).strip()
        
    m7 = re.search(item_7_pattern, text, re.DOTALL)
    if m7:
        sections["Item 7"] = m7.group(2).strip()
        
    return sections

def chunk_text(text, chunk_size=1000, overlap=200):
    chunks = []
    start = 0
    text_len = len(text)
    while start < text_len:
        end = min(start + chunk_size, text_len)
        # Find the last period in the chunk to avoid cutting words
        if end < text_len:
            last_period = text.rfind('.', start, end)
            if last_period != -1 and last_period > start + chunk_size // 2:
                end = last_period + 1
        
        chunks.append(text[start:end].strip())
        start = end - overlap
        if start >= text_len or end >= text_len:
            break
            
    return chunks

def process_narratives():
    narratives_dir = os.path.join("data", "processed", "narratives")
    all_chunks = []
    
    if not os.path.exists(narratives_dir):
        return all_chunks
        
    for filename in os.listdir(narratives_dir):
        if filename.endswith("_narrative.txt"):
            parts = filename.split("_")
            ticker = parts[0]
            year = parts[1]
            
            with open(os.path.join(narratives_dir, filename), "r", encoding="utf-8") as f:
                text = f.read()
                
            sections = extract_sections(text)
            
            for section_name, section_text in sections.items():
                text_chunks = chunk_text(section_text)
                for idx, chunk in enumerate(text_chunks):
                    if len(chunk) < 50:
                        continue
                    all_chunks.append({
                        "ticker": ticker,
                        "year": year,
                        "section": section_name,
                        "text": chunk,
                        "chunk_id": f"{ticker}_{year}_{section_name.replace(' ', '')}_{idx}"
                    })
    return all_chunks

if __name__ == "__main__":
    chunks = process_narratives()
    print(f"Extracted {len(chunks)} chunks.")
    # For debugging
    if chunks:
        print(f"Sample chunk: {chunks[0]['chunk_id']}")
