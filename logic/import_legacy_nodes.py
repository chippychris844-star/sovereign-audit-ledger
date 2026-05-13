import json
import sqlite3
import hashlib
import os
import uuid
from datetime import datetime

# CONFIGURATION
NODES_FILE = r"D:\SHANE\resolution certificate registry\signal-blog\quality-dataset\signal-graph-nodes.jsonl"
DB_PATH = r"C:\Users\chipp\sovereign_brain.sqlite"

def import_legacy_nodes():
    print(f"--- [RA] IMPORTING LEGACY NODES ---")
    if not os.path.exists(NODES_FILE):
        print("Legacy nodes file not found.")
        return

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    count = 0
    with open(NODES_FILE, 'r', encoding='utf-8-sig') as f:
        for line in f:
            line = line.strip()
            if not line: continue
            try:
                node = json.loads(line)
                sig_id = node.get("id", str(uuid.uuid4()))
                # Standardize for signals table
                timestamp = node.get("timestamp", datetime.now().isoformat())
                source = "LEGACY_SWARM_NODE"
                summary = node.get("claim") or node.get("title") or "Legacy Forensic Node"
                content_str = json.dumps(node)
                friction = node.get("friction_score", 0.5)
                sig_hash = hashlib.sha256(line.encode()).hexdigest()

                cursor.execute("SELECT id FROM signals WHERE id = ?", (sig_id,))
                if not cursor.fetchone():
                    cursor.execute("""
                        INSERT INTO signals (id, timestamp, source, summary, content, friction_score, hash)
                        VALUES (?, ?, ?, ?, ?, ?, ?)
                    """, (sig_id, timestamp, source, summary, content_str, friction, sig_hash))
                    count += 1
            except Exception as e:
                print(f"Error parsing line: {e}")

    conn.commit()
    conn.close()
    print(f"Imported {count} legacy nodes into the Sovereign Brain.")

if __name__ == "__main__":
    import_legacy_nodes()
