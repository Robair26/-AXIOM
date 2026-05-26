import os
import json
import hashlib
import re

KNOWLEDGE_DIR = os.path.join(os.path.dirname(__file__), 'knowledge')
os.makedirs(KNOWLEDGE_DIR, exist_ok=True)
KNOWLEDGE_FILE = os.path.join(KNOWLEDGE_DIR, 'knowledge.json')

def load_knowledge():
    if os.path.exists(KNOWLEDGE_FILE):
        with open(KNOWLEDGE_FILE, 'r') as f:
            return json.load(f)
    return {}

def save_knowledge(data):
    with open(KNOWLEDGE_FILE, 'w') as f:
        json.dump(data, f, indent=2)

def add_to_knowledge(text, source, doc_id=None):
    try:
        knowledge = load_knowledge()
        if not doc_id:
            doc_id = hashlib.md5(f"{source}{text[:100]}".encode()).hexdigest()
        chunks = [text[i:i+600] for i in range(0, len(text), 500)]
        knowledge[doc_id] = {
            "source": source,
            "chunks": chunks,
            "preview": text[:200],
            "full_text": text[:10000]
        }
        save_knowledge(knowledge)
        return True
    except Exception as e:
        print(f"Knowledge add error: {e}")
        return False

def search_knowledge(query, n_results=3):
    try:
        knowledge = load_knowledge()
        if not knowledge:
            return ""
        query_words = set(re.findall(r'\w+', query.lower()))
        scored = []
        for doc_id, doc in knowledge.items():
            text = doc.get('full_text', '').lower()
            score = sum(1 for word in query_words if word in text and len(word) > 3)
            if score > 0:
                scored.append((score, doc))
        scored.sort(key=lambda x: x[0], reverse=True)
        results = []
        for score, doc in scored[:n_results]:
            results.append(f"[From: {doc['source']}]\n{doc['preview']}")
        return "\n\n".join(results)
    except Exception as e:
        print(f"Knowledge search error: {e}")
        return ""

def list_knowledge():
    try:
        knowledge = load_knowledge()
        return [{"source": v["source"], "preview": v["preview"]} for v in knowledge.values()]
    except:
        return []

def clear_knowledge():
    try:
        if os.path.exists(KNOWLEDGE_FILE):
            os.remove(KNOWLEDGE_FILE)
        return True
    except:
        return False
