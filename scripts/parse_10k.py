import os
from unstructured.partition.html import partition_html
from unstructured.documents.elements import Text, Table, NarrativeText, Title

def parse_10k():
    in_path = os.path.join("data", "raw", "AAPL", "2023", "10k.htm")
    narratives_dir = os.path.join("data", "processed", "narratives")
    tables_dir = os.path.join("data", "processed", "tables")
    
    os.makedirs(narratives_dir, exist_ok=True)
    os.makedirs(tables_dir, exist_ok=True)
    
    print(f"Parsing {in_path} using unstructured...")
    elements = partition_html(filename=in_path)
    
    narrative_path = os.path.join(narratives_dir, "aapl_2023_narrative.txt")
    table_path = os.path.join(tables_dir, "aapl_2023_tables.txt")
    
    with open(narrative_path, "w", encoding="utf-8") as nf, \
         open(table_path, "w", encoding="utf-8") as tf:
        for element in elements:
            if isinstance(element, Table):
                tf.write(str(element) + "\n\n")
            elif isinstance(element, (NarrativeText, Title, Text)):
                # Just dumping all text into the narrative file
                nf.write(str(element) + "\n\n")
                
    print(f"Extraction complete! Narratives saved to {narrative_path}, Tables saved to {table_path}")

if __name__ == "__main__":
    parse_10k()
