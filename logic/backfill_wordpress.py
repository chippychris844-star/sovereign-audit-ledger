import sqlite3
import json
import urllib.request
import os
import hashlib
from datetime import datetime

# CONFIGURATION
DB_PATH = r"C:\Users\chipp\sovereign_brain.sqlite"
RA_API_KEY = "f3edb74ebae01e95760836b8b89a6f66080cab980b15c3030daf055399c44a9633127c2b5d8d1a07b5d43a65c0b1fd85"
WP_BASE_URL = "https://resolutionassurance.com.au/wp-json/ra/v2"

def get_all_signals():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT id, source, timestamp, summary, content, hash FROM signals ORDER BY timestamp ASC")
    rows = cursor.fetchall()
    conn.close()
    return rows

def push_batch(batch_signals, batch_num):
    endpoint = f"{WP_BASE_URL}/mobile/template-submit"
    
    formatted_signals = []
    for row in batch_signals:
        formatted_signals.append({
            "header": {
                "schema_version": "7.0.8",
                "witness_node": "VAL-WITNESS-001",
                "timestamp_ingested": row[2],
                "ingestion_cycle": f"BACKFILL-BATCH-{batch_num}"
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

    payload = {
        "generated_at": datetime.now().isoformat(),
        "dataset_id": f"RA-BACKFILL-{batch_num}-{datetime.now().strftime('%Y%m%d%H%M%S')}",
        "signals": formatted_signals,
        "reality_benchmark": {},
        "validator_heartbeat": { "node_id": "VAL-WITNESS-001", "status": "ACTIVE", "quorum_participation": "EXTERNAL", "latest_witness": {} }
    }
    
    payload_json = json.dumps(payload, separators=(',', ':'))
    integrity_fingerprint = hashlib.sha256(payload_json.encode('utf-8')).hexdigest()
    
    envelope = {
        "record_id": payload["dataset_id"],
        "integrity_fingerprint": integrity_fingerprint,
        "metadata": {
            "package_name": "RA-BACKFILL",
            "manifest_sha256": hashlib.sha256("manifest".encode('utf-8')).hexdigest(),
            "created_at": payload["generated_at"],
            "source_fingerprint": "BACKFILL-v7.0.8",
            "manifest_type": "graph-projection",
            "graph_payload": payload
        }
    }
    
    headers = { 'Content-Type': 'application/json', 'X-API-Key': RA_API_KEY, 'Authorization': f'Bearer {RA_API_KEY}', 'User-Agent': 'ResolutionAssurance-Validator/7.0.8' }
    
    print(f"[BACKFILL] Pushing batch {batch_num} ({len(batch_signals)} signals)...")
    data = json.dumps(envelope).encode('utf-8')
    req = urllib.request.Request(endpoint, data=data, headers=headers, method='POST')
    
    try:
        with urllib.request.urlopen(req, timeout=120) as response:
            print(f"[BACKFILL] Batch {batch_num} SUCCESS.")
            return True
    except Exception as e:
        print(f"[BACKFILL] Batch {batch_num} FAILED: {e}")
        return False

def run_backfill():
    all_signals = get_all_signals()
    total = len(all_signals)
    print(f"Starting backfill of {total} signals...")
    
    batch_size = 100
    for i in range(0, total, batch_size):
        batch = all_signals[i:i+batch_size]
        batch_num = (i // batch_size) + 1
        success = push_batch(batch, batch_num)
        if not success:
            print("Stopping backfill due to error.")
            break

if __name__ == "__main__":
    run_backfill()
