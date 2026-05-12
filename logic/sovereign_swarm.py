import json
import os
import uuid
import urllib.request
from datetime import datetime

def fetch_bgp_anomalies():
    print("Executing BGP Hunt...")
    # BGPStream API / public feeds
    url = "https://api.bgpstream.com/v1/event" # Example public endpoint
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'ResolutionAssurance-Sovereign/8.1.1'})
        with urllib.request.urlopen(req, timeout=20) as response:
            data = json.loads(response.read().decode('utf-8'))
            return data.get('data', {}).get('events', [])[:10]
    except Exception as e:
        print(f"BGP Hunt Failed: {e}")
        return []

def fetch_neo_data():
    print("Executing Space Watch (NEO)...")
    # NASA NeoWs (Near Earth Object Web Service)
    url = "https://api.nasa.gov/neo/rest/v1/feed/today?detailed=false&api_key=DEMO_KEY"
    try:
        with urllib.request.urlopen(url, timeout=20) as response:
            data = json.loads(response.read().decode('utf-8'))
            return data.get('near_earth_objects', {})
    except Exception as e:
        print(f"Space Watch Failed: {e}")
        return {}

def run_swarm():
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    
    # 1. BGP Signals
    bgp_events = fetch_bgp_anomalies()
    if bgp_events:
        signal = {
            "capture_id": str(uuid.uuid4()),
            "timestamp_utc": datetime.utcnow().isoformat() + "Z",
            "source": "BGP_HUNT_SWARM",
            "category": "Network",
            "data": bgp_events,
            "metadata": {"node": "GitHub-Action-Swarm"}
        }
        with open(f"extracts/sig_bgp_{timestamp}.json", "w") as f:
            json.dump(signal, f, indent=2)

    # 2. NEO Signals
    neo_data = fetch_neo_data()
    if neo_data:
        signal = {
            "capture_id": str(uuid.uuid4()),
            "timestamp_utc": datetime.utcnow().isoformat() + "Z",
            "source": "SPACE_WATCH_SWARM",
            "category": "Space",
            "data": neo_data,
            "metadata": {"node": "GitHub-Action-Swarm"}
        }
        with open(f"extracts/sig_neo_{timestamp}.json", "w") as f:
            json.dump(signal, f, indent=2)

if __name__ == "__main__":
    if not os.path.exists("extracts"): os.makedirs("extracts")
    run_swarm()
