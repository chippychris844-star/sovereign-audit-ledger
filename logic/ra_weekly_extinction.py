import json
import os
import uuid
import urllib.request
from datetime import datetime, timezone

# CONFIGURATION
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUTPUT_DIR = os.path.join(BASE_DIR, "extracts")

def save_extinction_signal(signal, domain_prefix):
    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    filename = f"extinction_{domain_prefix}_{timestamp}.json"
    filepath = os.path.join(OUTPUT_DIR, filename)
    with open(filepath, 'w') as f:
        json.dump(signal, f, indent=2)
    print(f"Recorded Extinction Signal: {filepath}")

def track_cryosphere():
    """Tracks Arctic/Antarctic Sea Ice Extent (NSIDC Proxy)"""
    print("Tracking Cryosphere Extinction (NSIDC)...")
    # API for monthly/daily sea ice extent data
    url = "https://nsidc.org/api/seaice/index/v2/arctic/daily/extent.json"
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'ResolutionAssurance-Sovereign/8.11'})
        with urllib.request.urlopen(req, timeout=30) as response:
            data = json.loads(response.read().decode('utf-8'))
            # Capture latest entry
            latest = data[-1] if isinstance(data, list) else data
            save_extinction_signal({
                "capture_id": str(uuid.uuid4()),
                "timestamp_utc": datetime.now(timezone.utc).isoformat(),
                "domain": "Cryosphere",
                "source": "NSIDC_API",
                "summary": "Record of vanishing Arctic sea ice extent",
                "data": latest,
                "metadata": {"protocol": "Canon 8.11", "node": "Cloud-Swarm"}
            }, "cryosphere")
    except Exception as e:
        print(f"Cryosphere Tracking Failed: {e}")

def track_orbital_debris():
    """Tracks Orbital Saturation and Collision Probabilities"""
    print("Tracking Orbital Sovereignty (Space-Track/CelesTrak)...")
    # Using CelesTrak GP API for satellite density snapshots
    url = "https://celestrak.org/NORAD/elements/gp.php?GROUP=active&FORMAT=json"
    try:
        # We only need count/density for high-level tracking
        req = urllib.request.Request(url, headers={'User-Agent': 'ResolutionAssurance-Sovereign/8.11'})
        with urllib.request.urlopen(req, timeout=60) as response:
            data = json.loads(response.read().decode('utf-8'))
            count = len(data)
            save_extinction_signal({
                "capture_id": str(uuid.uuid4()),
                "timestamp_utc": datetime.now(timezone.utc).isoformat(),
                "domain": "Orbital",
                "source": "CELESTRAK_ACTIVE_LEO",
                "summary": "Snapshot of LEO satellite saturation",
                "data": {
                    "active_satellite_count": count,
                    "sample": data[:5] # Representative sample
                },
                "metadata": {"protocol": "Canon 8.11", "node": "Cloud-Swarm"}
            }, "orbital")
    except Exception as e:
        print(f"Orbital Tracking Failed: {e}")

def track_biological_loss():
    """Tracks Pollinator/Biodiversity degradation proxies"""
    print("Tracking Biological Resilience...")
    # Using GBIF (Global Biodiversity Information Facility) as proxy
    # Focusing on Apis mellifera (Honey Bee) occurrence frequency
    url = "https://api.gbif.org/v1/occurrence/count?taxonKey=1341976" # Honey Bee
    try:
        with urllib.request.urlopen(url, timeout=20) as response:
            count = response.read().decode('utf-8')
            save_extinction_signal({
                "capture_id": str(uuid.uuid4()),
                "timestamp_utc": datetime.now(timezone.utc).isoformat(),
                "domain": "Biological",
                "source": "GBIF_API",
                "summary": "Pollinator (Apis mellifera) global occurrence count",
                "data": {"recorded_occurrences": int(count)},
                "metadata": {"protocol": "Canon 8.11", "node": "Cloud-Swarm"}
            }, "biological")
    except Exception as e:
        print(f"Biological Tracking Failed: {e}")

def run_weekly_extinction():
    print(f"--- [RA] WEEKLY EXTINCTION BASELINE CAPTURE: {datetime.now().isoformat()} ---")
    track_cryosphere()
    track_orbital_debris()
    track_biological_loss()
    print("Weekly Extinction Cycle Complete.")

if __name__ == "__main__":
    run_weekly_extinction()
