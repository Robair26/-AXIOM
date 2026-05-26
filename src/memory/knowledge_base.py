import os
import json
import chromadb
from chromadb.utils import embedding_functions

KNOWLEDGE_DIR = os.path.join(os.path.dirname(__file__), 'knowledge')
CHROMA_DIR = os.path.join(os.path.dirname(__file__), 'chroma_db')
os.makedirs(KNOWLEDGE_DIR, exist_ok=True)
os.makedirs(CHROMA_DIR, exist_ok=True)

def get_collection():
    try:
        client = chromadb.PersistentClient(path=CHROMA_DIR)
        ef = embedding_functions.SentenceTransformerEmbeddingFunction(model_name="all-MiniLM-L6-v2")
        collection = client.get_or_create_collection(name="axiom_knowledge", embedding_function=ef)
        return collection
    except Exception as e:
        print(f"ChromaDB error: {e}")
        return None

def add_to_knowledge(text, source, doc_id=None):
    try:
        collection = get_collection()
        if not collection:
            return False
        import hashlib
        if not doc_id:
            doc_id = hashlib.md5(f"{source}{text[:100]}".encode()).hexdigest()
        chunks = [text[i:i+500] for i in range(0, len(text), 400)]
        ids = [f"{doc_id}_chunk_{i}" for i in range(len(chunks))]
        metadatas = [{"source": source, "chunk": i} for i in range(len(chunks))]
        collection.upsert(documents=chunks, ids=ids, metadatas=metadatas)
        meta_file = os.path.join(KNOWLEDGE_DIR, 'index.json')
        index = {}
        if os.path.exists(meta_file):
            with open(meta_file, 'r') as f:
                index = json.load(f)
        index[doc_id] = {"source": source, "chunks": len(chunks), "preview": text[:200]}
        with open(meta_file, 'w') as f:
            json.dump(index, f, indent=2)
        return True
    except Exception as e:
        print(f"Knowledge add error: {e}")
        return False

def search_knowledge(query, n_results=3):
    try:
        collection = get_collection()
        if not collection or collection.count() == 0:
            return ""
        results = collection.query(query_texts=[query], n_results=min(n_results, collection.count()))
        if results and results['documents']:
            docs = results['documents'][0]
            metas = results['metadatas'][0]
            output = []
            for doc, meta in zip(docs, metas):
                output.append(f"[From: {meta['source']}] {doc}")
            return "\n\n".join(output)
        return ""
    except Exception as e:
        print(f"Knowledge search error: {e}")
        return ""

def list_knowledge():
    try:
        meta_file = os.path.join(KNOWLEDGE_DIR, 'index.json')
        if not os.path.exists(meta_file):
            return []
        with open(meta_file, 'r') as f:
            index = json.load(f)
        return list(index.values())
    except:
        return []

def clear_knowledge():
    try:
        client = chromadb.PersistentClient(path=CHROMA_DIR)
        client.delete_collection("axiom_knowledge")
        meta_file = os.path.join(KNOWLEDGE_DIR, 'index.json')
        if os.path.exists(meta_file):
            os.remove(meta_file)
        return True
    except:
        return False
