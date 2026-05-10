import sqlite3
import json
import urllib.request
import sys

DB_PATH = "C:\\Users\\chipp\\sovereign_brain.sqlite"
OLLAMA_URL = "http://localhost:11434/api/generate"

def query_brain(query_text):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # Search FTS5 table
    cursor.execute('''
        SELECT summary, content FROM signals_search 
        WHERE signals_search MATCH ? 
        LIMIT 3
    ''', (query_text,))
    
    results = cursor.fetchall()
    conn.close()
    return results

def call_gemma(prompt, context):
    full_prompt = f"""
    You are the Sovereign AI of the Resolution Assurance Protocol. 
    Use the following Evidence Context to answer the user query. 
    If the context does not contain the answer, state that it is unanchored in the ledger.
    
    Evidence Context:
    {context}
    
    Query: {prompt}
    
    Answer:
    """
    
    data = {
        "model": "gemma",
        "prompt": full_prompt,
        "stream": False
    }
    
    try:
        req = urllib.request.Request(OLLAMA_URL, data=json.dumps(data).encode('utf-8'), headers={'Content-Type': 'application/json'})
        with urllib.request.urlopen(req, timeout=30) as response:
            res = json.loads(response.read().decode('utf-8'))
            return res.get("response")
    except Exception as e:
        return f"[OFFLINE_REFINERY] Evidence found, but Gemma model node is unreachable. \nContext Summary: {context[:500]}..."

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python sovereign_query.py <query>")
        sys.exit(1)
        
    query = sys.argv[1]
    context_hits = query_brain(query)
    
    if context_hits:
        context_str = "\n---\n".join([f"Source: {h[0]}\nContent: {h[1]}" for h in context_hits])
        answer = call_gemma(query, context_str)
        print(answer)
    else:
        print("No matching signals found in the Sovereign Brain.")
