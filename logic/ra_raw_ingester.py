import json
import os
import uuid
import urllib.request
from datetime import datetime

# CONFIGURATION
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUTPUT_DIR = os.path.join(BASE_DIR, "extracts")
TEMPLATE_DIR = os.path.join(BASE_DIR, "core", "templates")
BRAIN_DB = os.path.join(os.path.expanduser("~"), "sovereign_brain.sqlite")

def fetch_bgp_anomalies():
    print("Executing BGP Hunt...")
    # Updated to CAIDA BGPStream V2 API
    url = "https://api.bgpstream.caida.org/v2/events"
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'ResolutionAssurance-Sovereign/8.11'})
        with urllib.request.urlopen(req, timeout=20) as response:
            data = json.loads(response.read().decode('utf-8'))
            events = data.get('data', {}).get('events', [])[:10]
            if events:
                save_signal({
                    "capture_id": str(uuid.uuid4()),
                    "timestamp_utc": datetime.utcnow().isoformat() + "Z",
                    "source": "BGP_HUNT_SWARM",
                    "category": "Network",
                    "data": events,
                    "metadata": {"node": "Cloud-Node", "protocol": "Canon 8.11"}
                }, "bgp")
                print(f"Captured {len(events)} BGP events.")
    except Exception as e:
        print(f"BGP Hunt Failed: {e}")

def fetch_neo_data():
    print("Executing Space Watch (NEO)...")
    url = "https://api.nasa.gov/neo/rest/v1/feed/today?detailed=false&api_key=DEMO_KEY"
    try:
        with urllib.request.urlopen(url, timeout=20) as response:
            data = json.loads(response.read().decode('utf-8'))
            neo_data = data.get('near_earth_objects', {})
            if neo_data:
                save_signal({
                    "capture_id": str(uuid.uuid4()),
                    "timestamp_utc": datetime.utcnow().isoformat() + "Z",
                    "source": "SPACE_WATCH_SWARM",
                    "category": "Space",
                    "data": neo_data,
                    "metadata": {"node": "Cloud-Node", "protocol": "Canon 8.11"}
                }, "neo")
                print("Captured NEO data.")
    except Exception as e:
        print(f"Space Watch Failed: {e}")

def fetch_trade_signals():
    print("Fetching Trade/Value signals...")
    # Using CoinGecko as a proxy for high-velocity value signals
    url = "https://api.coingecko.com/api/v3/simple/price?ids=bitcoin,ethereum,gold&vs_currencies=usd"
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'ResolutionAssurance/8.11'})
        with urllib.request.urlopen(req, timeout=20) as response:
            data = json.loads(response.read().decode('utf-8'))
            save_signal({
                "capture_id": str(uuid.uuid4()),
                "timestamp_utc": datetime.utcnow().isoformat() + "Z",
                "source": "MARKET_VALUE_PROXY",
                "category": "Trade",
                "data": data,
                "metadata": {"node": "Cloud-Node", "protocol": "Canon 8.11"}
            }, "trade")
            print("Captured Trade/Value signals.")
    except Exception as e:
        print(f"Trade Fetch Failed: {e}")

def fetch_mock_deep_sea():
    print("Fetching Mock Deep Sea signals...")
    save_signal({
        "capture_id": str(uuid.uuid4()),
        "timestamp_utc": datetime.utcnow().isoformat() + "Z",
        "source": "DEEP_SEA_MONITOR",
        "category": "Trade",
        "data": {"ocean_temp_c": 3.8, "sea_level_m": 0.45},
        "metadata": {"node": "Local-Node", "protocol": "Canon 8.11"}
    }, "deep_sea")

def save_signal(signal, prefix):
    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    filename = f"sig_{prefix}_{timestamp}.json"
    filepath = os.path.join(OUTPUT_DIR, filename)
    with open(filepath, 'w') as f:
        json.dump(signal, f, indent=2)
    print(f"Saved signal to {filepath}")

def run_ingester():
    print(f"Starting Ingestion Cycle (Network, Space, Trade)")
    fetch_bgp_anomalies()
    fetch_neo_data()
    fetch_trade_signals()
    fetch_mock_deep_sea()
    print("Ingestion cycle complete.")

if __name__ == "__main__":
    run_ingester()
