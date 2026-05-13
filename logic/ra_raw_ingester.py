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

def fetch_network_signals():
    print("Executing Network Watch (RIPE Stat)...")
    url = "https://stat.ripe.net/data/routing-status/data.json?resource=1.1.1.1"
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'ResolutionAssurance-Sovereign/8.11'})
        with urllib.request.urlopen(req, timeout=20) as response:
            data = json.loads(response.read().decode('utf-8'))
            routing_data = data.get('data', {})
            if routing_data:
                save_signal({
                    "capture_id": str(uuid.uuid4()),
                    "timestamp_utc": datetime.utcnow().isoformat() + "Z",
                    "source": "RIPE_STAT_NETWORK",
                    "category": "Network",
                    "data": routing_data,
                    "metadata": {"node": "Cloud-Node", "protocol": "Canon 8.11"}
                }, "network")
                print("Captured Network routing data.")
    except Exception as e:
        print(f"Network Watch Failed: {e}")

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

def fetch_security_signals():
    print("Executing Security/Disaster Watch (GDACS)...")
    url = "https://www.gdacs.org/gdacsapi/api/events/geteventlist/json"
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'ResolutionAssurance-Sovereign/8.11'})
        with urllib.request.urlopen(req, timeout=20) as response:
            data = json.loads(response.read().decode('utf-8'))
            events = data[:10] if isinstance(data, list) else []
            if events:
                save_signal({
                    "capture_id": str(uuid.uuid4()),
                    "timestamp_utc": datetime.utcnow().isoformat() + "Z",
                    "source": "GDACS_SECURITY_MONITOR",
                    "category": "Security",
                    "data": events,
                    "metadata": {"node": "Cloud-Node", "protocol": "Canon 8.11"}
                }, "security")
                print(f"Captured {len(events)} Security/Disaster events.")
    except Exception as e:
        print(f"Security Watch Failed: {e}")

def fetch_maritime_signals():
    print("Executing Maritime/Deep Sea Watch (Open-Meteo)...")
    # Coordinates for Mariana Trench (Deep Sea baseline)
    lat, lon = 11.35, 142.20
    url = f"https://marine-api.open-meteo.com/v1/marine?latitude={lat}&longitude={lon}&hourly=wave_height,wave_direction,wave_period"
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'ResolutionAssurance/8.11'})
        with urllib.request.urlopen(req, timeout=20) as response:
            data = json.loads(response.read().decode('utf-8'))
            # Get latest hourly reading
            latest_idx = 0 
            signals = {
                "location": {"lat": lat, "lon": lon, "name": "Mariana Trench"},
                "wave_height_m": data['hourly']['wave_height'][latest_idx],
                "wave_period_s": data['hourly']['wave_period'][latest_idx],
                "wave_direction": data['hourly']['wave_direction'][latest_idx]
            }
            save_signal({
                "capture_id": str(uuid.uuid4()),
                "timestamp_utc": datetime.utcnow().isoformat() + "Z",
                "source": "OPEN_METEO_MARITIME",
                "category": "Trade",
                "data": signals,
                "metadata": {"node": "Cloud-Node", "protocol": "Canon 8.11"}
            }, "deep_sea")
            print("Captured Deep Sea/Maritime signals.")
    except Exception as e:
        print(f"Maritime Watch Failed: {e}")
        # Fallback to mock
        save_signal({
            "capture_id": str(uuid.uuid4()),
            "timestamp_utc": datetime.utcnow().isoformat() + "Z",
            "source": "DEEP_SEA_MONITOR_FALLBACK",
            "category": "Trade",
            "data": {"ocean_temp_c": 3.8, "sea_level_m": 0.45},
            "metadata": {"node": "Local-Node", "protocol": "Canon 8.11", "status": "MOCK_FALLBACK"}
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
    print(f"Starting Ingestion Cycle (Network, Space, Trade, Security, Maritime)")
    fetch_network_signals()
    fetch_neo_data()
    fetch_trade_signals()
    fetch_security_signals()
    fetch_maritime_signals()
    print("Ingestion cycle complete.")

if __name__ == "__main__":
    run_ingester()
