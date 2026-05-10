import sqlite3
import os
import hashlib
import sys
from datetime import datetime

DB_PATH = "C:\\Users\\chipp\\sovereign_brain.sqlite"

def get_file_hash(filepath):
    """Generate a hash for a file to prevent duplicate indexing."""
    hasher = hashlib.sha256()
    with open(filepath, 'rb') as f:
        buf = f.read(65536)
        while len(buf) > 0:
            hasher.update(buf)
            buf = f.read(65536)
    return hasher.hexdigest()

def index_directory(target_dir):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    print(f"--- [RA] INDEXING DIRECTORY: {target_dir} ---")
    
    count = 0
    for root, dirs, files in os.walk(target_dir):
        for file in files:
            filepath = os.path.join(root, file)
            # Only index common text-based files for now
            if file.endswith(('.txt', '.md', '.json', '.csv', '.log', '.py', '.js', '.html')):
                try:
                    file_hash = get_file_hash(filepath)
                    
                    # Check if hash already exists
                    cursor.execute("SELECT id FROM signals WHERE hash = ?", (file_hash,))
                    if cursor.fetchone():
                        # print(f"Skipping (already indexed): {file}")
                        continue
                    
                    with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
                        content = f.read()
                        
                    sig_id = f"FILE-{file_hash[:12]}"
                    timestamp = datetime.fromtimestamp(os.path.getmtime(filepath)).isoformat()
                    source = f"Local_File_{os.path.basename(root)}"
                    summary = f"File: {file} | Path: {filepath}"
                    
                    cursor.execute('''
                    INSERT OR REPLACE INTO signals (id, timestamp, source, summary, content, friction_score, hash)
                    VALUES (?, ?, ?, ?, ?, ?, ?)
                    ''', (sig_id, timestamp, source, summary, content, 0.5, file_hash))
                    
                    count += 1
                    if count % 10 == 0:
                        print(f"Indexed {count} files...")
                except Exception as e:
                    print(f"Error indexing {file}: {e}")

    conn.commit()
    conn.close()
    print(f"--- [RA] INDEXING COMPLETE: {count} NEW FILES ADDED ---")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python index_files.py <directory_path>")
        sys.exit(1)
        
    target = sys.argv[1]
    if os.path.isdir(target):
        index_directory(target)
    else:
        print(f"Error: {target} is not a valid directory.")
