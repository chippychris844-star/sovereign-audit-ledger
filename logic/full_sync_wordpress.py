import json
import sqlite3
import urllib.request
import os
import hashlib
import time
from datetime import datetime

# CONFIGURATION
DB_PATH = r"C:\Users\chipp\sovereign_brain.sqlite"
RA_API_KEY = "f3edb74ebae01e95760836b8b89a6f66080cab980b15c3030daf055399c44a9633127c2b5d8d1a07b5d43a65c0b1fd85"
WP_BASE_URL = "https://resolutionassurance.com.au/wp-json/ra/v2"

def get_db_connection():
    return sqlite3.connect(DB_PATH)

def push_batch(payload_type, data_list, batch_num):
    endpoint = f"{WP_BASE_URL}/mobile/template-submit"
    
    # Prepare graph payload
    graph_payload = {
        "generated_at": datetime.now().isoformat(),
        "dataset_id": f"RA-FULL-SYNC-{payload_type.upper()}-{batch_num}-{datetime.now().strftime('%Y%m%d%H%M%S')}",
        "reality_benchmark": {},
        "validator_heartbeat": {
            "node_id": "VAL-WITNESS-001",
            "status": "ACTIVE",
            "quorum_participation": "EXTERNAL",
            "latest_witness": {}
        }
    }
    
    if payload_type == "signals":
        graph_payload["signals"] = data_list
    elif payload_type == "edges":
        graph_payload["edges"] = data_list

    payload_json = json.dumps(graph_payload, separators=(',', ':'))
    integrity_fingerprint = hashlib.sha256(payload_json.encode('utf-8')).hexdigest()
    
    envelope = {
        "record_id": graph_payload["dataset_id"],
        "integrity_fingerprint": integrity_fingerprint,
        "metadata": {
            "package_name": f"RA-FULL-SYNC-{payload_type.upper()}",
            "manifest_sha256": hashlib.sha256("manifest".encode('utf-8')).hexdigest(),
            "created_at": graph_payload["generated_at"],
            "source_fingerprint": "SYNC-v7.0.8",
            "manifest_type": "graph-projection",
            "graph_payload": graph_payload
        }
    }
    
    headers = {
        'Content-Type': 'application/json',
        'X-API-Key': RA_API_KEY,
        'Authorization': f'Bearer {RA_API_KEY}',
        'User-Agent': 'ResolutionAssurance-Validator/7.0.8'
    }

    print(f"[SYNC] Pushing {payload_type} batch {batch_num} ({len(data_list)} items)...")
    data = json.dumps(envelope).encode('utf-8')
    req = urllib.request.Request(endpoint, data=data, headers=headers, method='POST')
    
    try:
        with urllib.request.urlopen(req, timeout=120) as response:
            print(f"[SYNC] Batch {batch_num} SUCCESS.")
            return True
    except Exception as e:
        print(f"[SYNC] Batch {batch_num} FAILED: {e}")
        return False

def sync_all_signals():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id, source, timestamp, summary, content, hash FROM signals ORDER BY timestamp ASC")
    rows = cursor.fetchall()
    conn.close()
    
    total = len(rows)
    print(f"Syncing {total} signals...")
    
    batch_size = 100
    for i in range(0, total, batch_size):
        batch_rows = rows[i:i+batch_size]
        batch_data = []
        for row in batch_rows:
            batch_data.append({
                "header": {
                    "schema_version": "7.0.8",
                    "witness_node": "VAL-WITNESS-001",
                    "timestamp_ingested": row[2],
                    "ingestion_cycle": "FULL-SYNC-BACKFILL"
                },
                "signal": {
                    "id": f"SIG-{row[0]}",
                    "source": { "id": f"SRC_{row[1].upper()}", "name": row[1], "provenance": f"ra://provenance/{row[1]}" },
                    "domain": "audit",
                    "data": row[4],
                    "metadata": {"summary": row[3]}
                },
                "witness_interpretation": { "narrative": row[3], "witness_posture": "Non-Advisory, Evidence-First" },
                "governance": { "reality_anchor_hash": row[5] or "0" * 64, "rights": "EXCLUSIVE_NON_DEGRADABLE_HISTORY" }
            })
        
        batch_num = (i // batch_size) + 1
        push_batch("signals", batch_data, batch_num)
        time.sleep(1) # Rate limit protection

def sync_all_edges():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id, type, from_node, to_node, properties, hash FROM edges")
    rows = cursor.fetchall()
    conn.close()
    
    total = len(rows)
    print(f"Syncing {total} edges...")
    
    batch_size = 500 # Smaller batch for edges due to volume
    for i in range(0, total, batch_size):
        batch_rows = rows[i:i+batch_size]
        batch_data = []
        for row in batch_rows:
            batch_data.append({
                "id": row[0],
                "type": row[1],
                "from": row[2],
                "to": row[3],
                "properties": json.loads(row[4]),
                "hash": row[5]
            })
        
        batch_num = (i // batch_size) + 1
        push_batch("edges", batch_data, batch_num)
        # Push only a limited number of batches for now to verify, or all if feasible
        # Given 142k edges, 500 per batch = 284 batches. 
        # I'll let it run but maybe add a check.
        if batch_num % 10 == 0:
            print(f"Progress: {i + len(batch_rows)} edges pushed...")
        
        time.sleep(0.5)

if __name__ == "__main__":
    print("--- [RA] FULL WORDPRESS SYNC INITIATED ---")
    sync_all_signals()
    sync_all_edges()
    print("--- [RA] FULL WORDPRESS SYNC COMPLETE ---")
