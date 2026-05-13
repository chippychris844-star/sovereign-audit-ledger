import json
import sqlite3
import hashlib
import os

EDGES_FILE = r"D:\SHANE\resolution certificate registry\signal-blog\quality-dataset\signal-graph-edges.jsonl"
DB_PATH = r"C:\Users\chipp\sovereign_brain.sqlite"

def backfill_edges():
    print(f"--- [RA] BACKFILLING 142k EDGES ---")
    if not os.path.exists(EDGES_FILE):
        print("Edges file not found.")
        return

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    batch = []
    batch_size = 5000
    total_imported = 0

    with open(EDGES_FILE, 'r', encoding='utf-8-sig') as f:
        for line in f:
            line = line.strip()
            if not line: continue
            try:
                edge = json.loads(line)
                edge_id = edge.get("edge_id")
                edge_type = edge.get("edge_type")
                from_node = edge.get("from_node_id")
                to_node = edge.get("to_node_id")
                properties = json.dumps(edge.get("properties", {}))
                sig_hash = hashlib.sha256(line.encode()).hexdigest()

                batch.append((edge_id, edge_type, from_node, to_node, properties, sig_hash))

                if len(batch) >= batch_size:
                    cursor.executemany("""
                        INSERT OR IGNORE INTO edges (id, type, from_node, to_node, properties, hash)
                        VALUES (?, ?, ?, ?, ?, ?)
                    """, batch)
                    total_imported += cursor.rowcount
                    batch = []
                    print(f"Progress: {total_imported} edges backfilled...")
            except Exception as e:
                pass

    if batch:
        cursor.executemany("""
            INSERT OR IGNORE INTO edges (id, type, from_node, to_node, properties, hash)
            VALUES (?, ?, ?, ?, ?, ?)
        """, batch)
        total_imported += cursor.rowcount

    conn.commit()
    conn.close()
    print(f"Backfill complete. Total unique edges integrated: {total_imported}")

if __name__ == "__main__":
    backfill_edges()
