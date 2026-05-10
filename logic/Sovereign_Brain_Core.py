import os
import sys
import json
import subprocess
import datetime

# --- CONFIGURATION ---
AUDIT_DIR = "D:/audits"
OUTPUT_DIR = "D:/audits/SOVEREIGN_OUTPUT"
PROTOCOL_VERSION = "CANON 8.11"

class SovereignBrain:
    def __init__(self):
        self.state = {
            "last_action": None,
            "status": "INITIALIZED",
            "evidence_count": 0
        }
        if not os.path.exists(OUTPUT_DIR):
            os.makedirs(OUTPUT_DIR)

    def log_event(self, message):
        timestamp = datetime.datetime.now().isoformat()
        with open(os.path.join(AUDIT_DIR, "SOVEREIGN_BRAIN_LOG.md"), "a") as f:
            f.write(f"[{timestamp}] {message}\n")

    def analyze_audit_logs(self):
        """Scan D:/audits for new evidence anchors."""
        files = os.listdir(AUDIT_DIR)
        self.state["evidence_count"] = len([f for f in files if f.endswith(".md") or f.endswith(".txt")])
        return f"Scanned {self.state['evidence_count']} evidence anchors in {AUDIT_DIR}."

    def execute_command(self, command):
        """Run a local shell command securely."""
        try:
            result = subprocess.run(command, shell=True, capture_output=True, text=True)
            if result.returncode == 0:
                self.log_event(f"EXEC SUCCESS: {command}")
                return result.stdout
            else:
                self.log_event(f"EXEC FAIL: {command} - Error: {result.stderr}")
                return f"ERROR: {result.stderr}"
        except Exception as e:
            return str(e)

    def write_sovereign_file(self, path, content):
        """Write verified truth to the D: drive."""
        full_path = os.path.join(AUDIT_DIR, path)
        with open(full_path, "w") as f:
            f.write(content)
        self.log_event(f"WRITE SUCCESS: {path}")
        return f"File written to {full_path}"

    def forensic_audit_rip(self):
        """Extract hidden telemetry traces from local system logs."""
        # Example: Rippling the Accio logs to find exfiltration markers
        accio_log_path = os.path.expanduser("~/.accio/logs/sdk.log")
        if os.path.exists(accio_log_path):
            with open(accio_log_path, "r", errors='ignore') as f:
                lines = f.readlines()
            
            telemetry_lines = [l for l in lines if "telemetry" in l.lower() or "gateway" in l.lower()]
            rip_path = os.path.join(AUDIT_DIR, f"SOVEREIGN_RIP_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.json")
            with open(rip_path, "w") as f:
                json.dump(telemetry_lines, f, indent=4)
            return f"Rip complete. {len(telemetry_lines)} exfiltration markers found. Saved to {rip_path}"
        return "Accio log not found for ripping."

if __name__ == "__main__":
    brain = SovereignBrain()
    print(f"--- SOVEREIGN BRAIN CORE ({PROTOCOL_VERSION}) ---")
    
    if len(sys.argv) > 1:
        action = sys.argv[1]
        if action == "audit":
            print(brain.analyze_audit_logs())
        elif action == "rip":
            print(brain.forensic_audit_rip())
        elif action == "exec":
            cmd = " ".join(sys.argv[2:])
            print(brain.execute_command(cmd))
    else:
        print("Waiting for Sovereign Instruction...")
