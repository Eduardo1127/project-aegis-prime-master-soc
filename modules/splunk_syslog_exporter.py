#!/usr/bin/env python3
"""
AEGIS PRIME - SPLUNK & SYSLOG CEF EVENT EXPORTER
Author: Eduardo Mex Rodriguez (EMR) (Defensive Security Engineering Portfolio)

Features:
1. Converts Aegis SIEM / SOAR alerts into Splunk HEC (HTTP Event Collector) & Syslog CEF (Common Event Format).
2. Industry-standard JSON schema for CrowdStrike & Splunk enterprise ingestion.
"""

import sys
import json
import time
import datetime

class SplunkSyslogExporter:
    def __init__(self, splunk_hec_url=None, splunk_token=None):
        self.splunk_hec_url = splunk_hec_url
        self.splunk_token = splunk_token

    def format_cef_event(self, source_ip, attack_type, severity, mitre_id, raw_event):
        """Formats security alert into Common Event Format (CEF) for SIEM/Splunk."""
        timestamp = datetime.datetime.now(datetime.timezone.utc).strftime("%b %d %H:%M:%S")
        cef_string = f"CEF:0|AEGIS-PRIME|MasterSOC|2.0|{mitre_id}|{attack_type}|{severity}|src={source_ip} msg={raw_event}"
        return f"{timestamp} aegis-soc-engine: {cef_string}"

    def format_splunk_hec_json(self, source_ip, attack_type, severity, mitre_id, raw_event):
        """Formats security alert into Splunk HTTP Event Collector (HEC) JSON payload."""
        payload = {
            "time": time.time(),
            "host": "aegis-master-server",
            "source": "aegis:soar:engine",
            "sourcetype": "_json",
            "event": {
                "vendor": "EMR Defensive Security",
                "product": "Aegis Prime Master SOC",
                "mitre_attack_id": mitre_id,
                "severity": severity,
                "attacker_ip": source_ip,
                "attack_classification": attack_type,
                "raw_event_payload": raw_event,
                "containment_status": "AUTOMATED_BLOCK_TRIGGERED"
            }
        }
        return payload

    def export_sample_telemetry(self):
        print("=" * 70)
        print("📊 AEGIS PRIME - SPLUNK & SYSLOG CEF EVENT EXPORTER")
        print("=" * 70)
        
        sample_cef = self.format_cef_event(
            source_ip="192.168.1.227",
            attack_type="Web Command Injection Attack",
            severity="CRITICAL",
            mitre_id="T1059.004",
            raw_event="GET /api/ping_secure?host=127.0.0.1%3Bcat%20/etc/passwd"
        )
        print("\n[+] Formatted Syslog CEF Payload (Ready for Splunk / Logstash):")
        print(f"    {sample_cef}")

        sample_splunk = self.format_splunk_hec_json(
            source_ip="192.168.1.227",
            attack_type="Web Command Injection Attack",
            severity="CRITICAL",
            mitre_id="T1059.004",
            raw_event="GET /api/ping_secure?host=127.0.0.1%3Bcat%20/etc/passwd"
        )
        print("\n[+] Formatted Splunk HEC JSON Payload (Splunk Enterprise Compatible):")
        print(json.dumps(sample_splunk, indent=4))
        
        print("=" * 70)
        print("[SUCCESS] Telemetry Successfully Formatted for Splunk & Enterprise SIEMs!")
        print("=" * 70)

if __name__ == "__main__":
    if sys.platform == "win32":
        sys.stdout.reconfigure(encoding='utf-8')
    exporter = SplunkSyslogExporter()
    exporter.export_sample_telemetry()
