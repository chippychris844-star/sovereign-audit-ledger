import json
import os
import uuid
import urllib.request
from datetime import datetime

# CONFIGURATION
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUTPUT_DIR = os.path.join(BASE_DIR, "extracts")
TEMPLATE_DIR = os.path.join(BASE_DIR, "core", "templates")
BRAIN_DB = os.path.join(os.path.expanduser("~"), "sovereign_brain.sqlite") # Default to home dir for local/cloud

def fetch_space_signals():
    # Placeholder for actual API calls (NASA, etc.)
    # For now, we simulate the ingestion of baseline space data
    # In a real scenario, we'd use NASA's APOD or NeoWs API
    print("Fetching Space signals...")
    template_path = os.path.join(TEMPLATE_DIR, "space-signal-template.json")
    with open(template_path, 'r') as f:
        signal = json.load(f)
    
    signal["capture_id"] = str(uuid.uuid4())
    signal["timestamp_utc"] = datetime.utcnow().isoformat() + "Z"
    
    # Simulated data points
    signal["data"]["solar_activity_index"] = 4.2 # Mock value
    signal["data"]["near_earth_objects"] = ["2024-XA1", "2024-BY5"]
    
    save_signal(signal, "space")

def fetch_deep_sea_signals():
    print("Fetching Deep Sea signals...")
    template_path = os.path.join(TEMPLATE_DIR, "deep-sea-signal-template.json")
    with open(template_path, 'r') as f:
        signal = json.load(f)
    
    signal["capture_id"] = str(uuid.uuid4())
    signal["timestamp_utc"] = datetime.utcnow().isoformat() + "Z"
    
    # Simulated data points
    signal["data"]["ocean_temp_c"] = 3.8 # Mock value
    signal["data"]["sea_level_m"] = 0.45 # Mock value
    
    save_signal(signal, "deep_sea")

def save_signal(signal, prefix):
    filename = f"sig_{prefix}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    filepath = os.path.join(OUTPUT_DIR, filename)
    with open(filepath, 'w') as f:
        json.dump(signal, f, indent=2)
    print(f"Saved signal to {filepath}")

def run_ingester():
    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)
    
    # 0. Core Logic: Fetch and Save signals
    fetch_space_signals()
    fetch_deep_sea_signals()
    
    print("Ingestion cycle complete.")

if __name__ == "__main__":
    run_ingester()
