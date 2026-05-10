import os
import re
import json

def extract_strings(db_path, output_file):
    chat_fragments = []
    
    if not os.path.exists(db_path):
        print(f"Error: Path {db_path} does not exist.")
        return

    print(f"Scanning LevelDB at: {db_path}")
    
    for root, dirs, files in os.walk(db_path):
        for file in files:
            if file.endswith('.ldb') or file.endswith('.log'):
                file_path = os.path.join(root, file)
                try:
                    with open(file_path, 'rb') as f:
                        content = f.read()
                        # Extract readable strings
                        matches = re.findall(rb'[\x20-\x7E\xA0-\xFF]{20,}', content)
                        for match in matches:
                            text = match.decode('utf-8', errors='ignore').strip()
                            if len(text) > 40:
                                chat_fragments.append({
                                    'file': file,
                                    'text': text
                                })
                except Exception as e:
                    print(f"Could not read {file}: {e}")

    # Deduplicate
    seen = set()
    unique_fragments = []
    for frag in chat_fragments:
        if frag['text'] not in seen:
            unique_fragments.append(frag)
            seen.add(frag['text'])

    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(unique_fragments, f, indent=2)
    
    print(f"Extraction complete. {len(unique_fragments)} fragments saved to {output_file}")

if __name__ == "__main__":
    TARGETS = [
        (r'C:\Users\chipp\AppData\Local\Microsoft\Edge\User Data\Default\IndexedDB\https_chatgpt.com_0.indexeddb.leveldb', 'CHATGPT_EDGE_EXTRACT.json'),
        (r'C:\Users\chipp\AppData\Local\Microsoft\Edge\User Data\Default\IndexedDB\https_claude.ai_0.indexeddb.leveldb', 'CLAUDE_EDGE_EXTRACT.json'),
        (r'C:\Users\chipp\AppData\Local\Google\Chrome\User Data\Default\IndexedDB\https_chatgpt.com_0.indexeddb.leveldb', 'CHATGPT_CHROME_EXTRACT.json'),
        (r'C:\Users\chipp\AppData\Local\Google\Chrome\User Data\Default\IndexedDB\https_claude.ai_0.indexeddb.leveldb', 'CLAUDE_CHROME_EXTRACT.json')
    ]
    
    DESKTOP_PATH = r'C:\Users\chipp\OneDrive\Desktop'
    
    for db_path, out_name in TARGETS:
        output = os.path.join(DESKTOP_PATH, out_name)
        extract_strings(db_path, output)
