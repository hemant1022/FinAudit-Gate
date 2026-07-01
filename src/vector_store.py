import os
import chromadb
from chromadb.utils import embedding_functions

# Use a standard local model
try:
    sentence_transformer_ef = embedding_functions.SentenceTransformerEmbeddingFunction(model_name="all-MiniLM-L6-v2")
except Exception as e:
    print("Could not load sentence_transformer_ef, using default. Error:", e)
    sentence_transformer_ef = chromadb.utils.embedding_functions.DefaultEmbeddingFunction()

def get_chroma_client():
    db_path = os.path.join(os.path.dirname(__file__), "..", "vector_store", "chroma")
    os.makedirs(db_path, exist_ok=True)
    return chromadb.PersistentClient(path=db_path)

def build_vector_store(chunks):
    client = get_chroma_client()
    
    collection = client.get_or_create_collection(
        name="financial_narratives",
        embedding_function=sentence_transformer_ef
    )
    
    if not chunks:
        print("No chunks provided to build_vector_store")
        return
        
    documents = [c["text"] for c in chunks]
    metadatas = [{"ticker": c["ticker"], "year": c["year"], "section": c["section"]} for c in chunks]
    ids = [c["chunk_id"] for c in chunks]
    
    collection.upsert(
        documents=documents,
        metadatas=metadatas,
        ids=ids
    )
    
    print(f"Upserted {len(chunks)} chunks into ChromaDB collection 'financial_narratives'")

def query_vector_store(query: str, ticker: str = None, section: str = None, n_results: int = 3):
    client = get_chroma_client()
    try:
        collection = client.get_collection(
            name="financial_narratives",
            embedding_function=sentence_transformer_ef
        )
    except Exception as e:
        print(f"[Vector Store] Collection not found or failed to load: {e}")
        return {"documents": [[]]}
    
    where = {}
    if ticker:
        where["ticker"] = ticker
    if section:
        where["section"] = section
        
    if not where:
        where = None
        
    results = collection.query(
        query_texts=[query],
        n_results=n_results,
        where=where
    )
    
    return results

if __name__ == "__main__":
    # Test loading
    from chunker import process_narratives
    chunks = process_narratives()
    build_vector_store(chunks)
    
    res = query_vector_store("What are the supply chain risks?", ticker="AAPL", section="Item 1A")
    print(res)
