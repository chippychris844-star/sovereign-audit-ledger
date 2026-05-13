import json
import os
import sqlite3
import hashlib
from datetime import datetime

# CONFIGURATION
EXTRACTS_DIR = r"C:\audits\extracts"
DB_PATH = r"C:\Users\chipp\sovereign_brain.sqlite"

def sync_brain():
    print(f"--- [RA] SOVEREIGN BRAIN SYNC INITIATED ---")
    if not os.path.exists(EXTRACTS_DIR):
        print(f"Extracts directory not found: {EXTRACTS_DIR}")
        return

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    files = [f for f in os.listdir(EXTRACTS_DIR) if f.endswith('.json')]
    print(f"Found {len(files)} potential signals in extracts.")

    new_count = 0
    for f in files:
        path = os.path.join(EXTRACTS_DIR, f)
        with open(path, 'r', encoding='utf-8-sig') as jf:
            try:
                content = jf.read()
                if not content.strip(): continue
                data = json.loads(content)
                
                # Check if it's a list or single object
                signals = data if isinstance(data, list) else [data]
                
                for sig in signals:
                    sig_id = sig.get("capture_id", str(hashlib.sha256(content.encode()).hexdigest()[:8]))
                    timestamp = sig.get("timestamp_utc", datetime.now().isoformat())
                    source = sig.get("source", "UNKNOWN")
                    summary = sig.get("summary", f"Automated capture from {source}")
                    content_str = json.dumps(sig)
                    friction = sig.get("friction_score", 0.1) # Default low friction
                    sig_hash = hashlib.sha256(content_str.encode()).hexdigest()

                    # Check for existence
                    cursor.execute("SELECT id FROM signals WHERE id = ?", (sig_id,))
                    if not cursor.fetchone():
                        cursor.execute("""
                            INSERT INTO signals (id, timestamp, source, summary, content, friction_score, hash)
                            VALUES (?, ?, ?, ?, ?, ?, ?)
                        """, (sig_id, timestamp, source, summary, content_str, friction, sig_hash))
                        new_count += 1
            except Exception as e:
                print(f"Error processing {f}: {e}")

    conn.commit()
    conn.close()
    print(f"Sync complete. {new_count} new signals integrated into the Sovereign Brain.")

if __name__ == "__main__":
    sync_brain()
