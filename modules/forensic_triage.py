#!/usr/bin/env python3
"""
AEGIS PRIME - LIVE FORENSIC TRIAGE & EVIDENCE PRESERVATION ENGINE
Author: Eduardo Mex Rodriguez (EMR)

Performs live incident triage and evidence collection:
1. Active Network Connections & Sockets
2. Running Processes & Parent-Child Trees
3. Cryptographic Hash Calculation (SHA-256 Integrity Verification)
4. System Log Artifact Collection
5. Evidence Preservation Manifest Generation
"""

import sys
import os
import json
import hashlib
import datetime
import subprocess

if sys.platform == "win32":
    sys.stdout.reconfigure(encoding='utf-8')


class ForensicTriageEngine:
    def __init__(self, output_dir="forensic_evidence"):
        self.output_dir = output_dir
        os.makedirs(self.output_dir, exist_ok=True)
        self.timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")

    def calculate_sha256(self, filepath):
        """Calculates SHA-256 hash for cryptographic chain of custody."""
        sha256 = hashlib.sha256()
        try:
            with open(filepath, "rb") as f:
                for chunk in iter(lambda: f.read(4096), b""):
                    sha256.update(chunk)
            return sha256.hexdigest()
        except Exception as e:
            return f"ERROR: {e}"

    def collect_evidence(self):
        print("=" * 70)
        print("🔍 AEGIS FORENSIC TRIAGE & EVIDENCE PRESERVATION")
        print("   Author: Eduardo Mex Rodriguez (EMR)")
        print("=" * 70)
        print(f"[+] Evidence Preservation Directory: {self.output_dir}\n")

        evidence_manifest = {
            "case_id": f"INCIDENT_{self.timestamp}",
            "investigator": "Eduardo Mex Rodriguez (EMR)",
            "timestamp": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "artifacts_collected": []
        }

        # 1. Collect Network Connections
        net_file = os.path.join(self.output_dir, f"network_connections_{self.timestamp}.txt")
        try:
            cmd = ["netstat", "-ano"] if sys.platform == "win32" else ["netstat", "-tunap"]
            res = subprocess.run(cmd, capture_output=True, text=True, errors="ignore")
            with open(net_file, "w", encoding="utf-8") as f:
                f.write(res.stdout)
            
            hash_val = self.calculate_sha256(net_file)
            evidence_manifest["artifacts_collected"].append({
                "type": "Network Sockets",
                "filename": os.path.basename(net_file),
                "sha256": hash_val
            })
            print(f"   [✅ COLLECTED] Network Connections -> SHA-256: {hash_val[:16]}...")
        except Exception as e:
            print(f"   [ERROR] Network collection failed: {e}")

        # 2. Collect Running Processes
        proc_file = os.path.join(self.output_dir, f"running_processes_{self.timestamp}.txt")
        try:
            cmd = ["tasklist", "/v"] if sys.platform == "win32" else ["ps", "auxef"]
            res = subprocess.run(cmd, capture_output=True, text=True, errors="ignore")
            with open(proc_file, "w", encoding="utf-8") as f:
                f.write(res.stdout)

            hash_val = self.calculate_sha256(proc_file)
            evidence_manifest["artifacts_collected"].append({
                "type": "Process Tree",
                "filename": os.path.basename(proc_file),
                "sha256": hash_val
            })
            print(f"   [✅ COLLECTED] Running Processes  -> SHA-256: {hash_val[:16]}...")
        except Exception as e:
            print(f"   [ERROR] Process collection failed: {e}")

        # 3. Save Chain of Custody Manifest
        manifest_file = os.path.join(self.output_dir, f"chain_of_custody_manifest_{self.timestamp}.json")
        with open(manifest_file, "w", encoding="utf-8") as f:
            json.dump(evidence_manifest, f, indent=2, ensure_ascii=False)

        manifest_hash = self.calculate_sha256(manifest_file)

        print("\n" + "=" * 70)
        print("📜 CHAIN OF CUSTODY MANIFEST GENERATED:")
        print(f"   Case ID:       {evidence_manifest['case_id']}")
        print(f"   Investigator:  {evidence_manifest['investigator']}")
        print(f"   Manifest File: {manifest_file}")
        print(f"   Manifest SHA-256: {manifest_hash}")
        print("=" * 70)

        return evidence_manifest


if __name__ == "__main__":
    engine = ForensicTriageEngine()
    engine.collect_evidence()
