import json
import os
import re

def extract_accio_chats(log_dir, output_file):
    chats = []
    log_files = [f for f in os.listdir(log_dir) if f.startswith('sdk.log')]
    
    # Sort files to maintain chronological order (sdk.log.5, sdk.log.4 ... sdk.log)
    # Actually, sdk.log is the most recent, sdk.log.1 is older, etc.
    log_files.sort(key=lambda x: (len(x), x), reverse=True)
    
    for log_file in log_files:
        path = os.path.join(log_dir, log_file)
        print(f"Processing {path}...")
        with open(path, 'r', encoding='utf-8', errors='ignore') as f:
            for line in f:
                try:
                    data = json.loads(line)
                    message_str = data.get('message', '')
                    
                    # llm.call trace contains the current userPrompt
                    if data.get('name') == 'llm.call':
                        input_data = data.get('input', {})
                        user_prompt = input_data.get('userPrompt')
                        if user_prompt:
                            chats.append({
                                'timestamp': data.get('timestamp'),
                                'role': 'user',
                                'text': user_prompt,
                                'source': 'llm_call_trace'
                            })
                    
                    # adk.llm.call contains the 'contents' array (history)
                    if data.get('name') == 'adk.llm.call':
                        input_data = data.get('input', {})
                        contents = input_data.get('contents', [])
                        for msg in contents:
                            if msg.get('role') == 'user':
                                parts = msg.get('parts', [])
                                text = "".join([p.get('text', '') for p in parts])
                                if text:
                                    chats.append({
                                        'timestamp': data.get('timestamp'),
                                        'role': 'user',
                                        'text': text,
                                        'source': 'adk_llm_call_contents'
                                    })
                    
                    # AccioADK logs contain frame-by-frame content
                    if '[AccioADK]' in message_str:
                        # Extract the JSON part
                        json_match = re.search(r'\{.*\}', message_str, re.DOTALL)
                        if json_match:
                            try:
                                payload = json.loads(json_match.group(0))
                                content = payload.get('content', {})
                                role = content.get('role')
                                parts = content.get('parts', [])
                                
                                if role == 'user':
                                    text = "".join([p.get('text', '') for p in parts])
                                    if text:
                                        chats.append({
                                            'timestamp': data.get('timestamp'),
                                            'role': 'user',
                                            'text': text,
                                            'source': 'accio_adk_frame'
                                        })
                            except: pass
                except Exception:
                    continue

    # Deduplicate by text while maintaining order
    seen_text = set()
    deduped_chats = []
    for chat in chats:
        # Normalize text for comparison (remove whitespace/newlines)
        norm_text = re.sub(r'\s+', ' ', chat['text']).strip()
        if norm_text not in seen_text:
            deduped_chats.append(chat)
            seen_text.add(norm_text)
    
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(deduped_chats, f, indent=2)
    
    print(f"Extracted and deduplicated {len(deduped_chats)} user messages to {output_file}")

if __name__ == "__main__":
    LOG_DIR = r'C:\Users\chipp\.accio\logs'
    OUTPUT = r'C:\audits\USER_ONLY_CHAT_EXTRACT.json'
    extract_accio_chats(LOG_DIR, OUTPUT)
