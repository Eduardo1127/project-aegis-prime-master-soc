#!/usr/bin/env python3
"""
AEGIS PRIME - HARDWARE-BASED DYNAMIC LICENSE VERIFIER & TELEMETRY ENGINE
Author: Eduardo Mex Rodriguez (EMR)

Features:
1. Dynamic HWID Generation: Automatically creates a 100% UNIQUE Hardware ID for each client
   based on their machine's hostname, MAC address, and CPU architecture.
2. Individual Tracking: Every single buyer generates a unique key (e.g. EMR-HWID-A8F9-22B4).
3. Selective Remote Revocation: Eduardo can block Client A without affecting Client B.
4. Telegram Push Telemetry: Sends the client's unique HWID to Eduardo's phone upon launch.
"""

import sys
import os
import json
import uuid
import hashlib
import platform
import requests

GITHUB_REVOCATION_URL = "https://gist.githubusercontent.com/Eduardo1127/02ba956d3504f63c480680e28a96eb67/raw/revoked_licenses.txt"
DEFAULT_TELEGRAM_TOKEN = "8893915158:AAFWy8WTn2sXP0_GXgRFEKsOkGtMeOfpie0"
DEFAULT_TELEGRAM_CHAT_ID = "8926630685"


class AegisLicenseVerifier:
    def __init__(self, license_key=None):
        self.raw_key = license_key
        self.hwid = self._generate_unique_hwid()

    def _generate_unique_hwid(self):
        """Generates a unique hardware fingerprint for the client machine."""
        mac = hex(uuid.getnode())
        hostname = platform.node()
        system_info = f"{hostname}-{mac}-{platform.machine()}"
        sha = hashlib.sha256(system_info.encode("utf-8")).hexdigest().upper()
        # Returns a clean unique ID: EMR-HWID-A8F9-22B4
        return f"EMR-HWID-{sha[:4]}-{sha[4:8]}"

    def check_github_revocation(self):
        """Fetches live revoked license list from Eduardo's GitHub Gist."""
        try:
            r = requests.get(GITHUB_REVOCATION_URL, timeout=4)
            if r.status_code == 200:
                revoked_list = [line.strip() for line in r.text.splitlines() if line.strip()]
                return revoked_list
        except Exception:
            pass
        return []

    def verify_and_telemetry(self):
        if sys.platform == "win32":
            try:
                sys.stdout.reconfigure(encoding='utf-8')
            except Exception:
                pass

        print("=" * 70)
        print("🔑 AEGIS PRIME - AUTOMATIC UNIQUE LICENSE VERIFIER")
        print("   Author: Eduardo Mex Rodriguez (EMR)")
        print("=" * 70)
        print(f"[+] Client Hardware ID (HWID): '{self.hwid}'...")

        # Fetch revoked list from Eduardo's GitHub
        revoked_list = self.check_github_revocation()

        # Check if this specific client's HWID is in the revocation list
        if self.hwid in revoked_list or (self.raw_key and self.raw_key in revoked_list):
            print(f"\n❌ [ACCESS DENIED] License key for HWID '{self.hwid}' has been REVOKED.")
            print("   Execution blocked. Please contact Eduardo Mex Rodriguez (EMR) for renewal.")
            print("=" * 70)

            try:
                url = f"https://api.telegram.org/bot{DEFAULT_TELEGRAM_TOKEN}/sendMessage"
                msg = f"🚨 *[AEGIS ACCESS DENIED]*\nA revoked client tried to launch the software!\n*Client HWID:* `{self.hwid}`\n*Author:* Eduardo Mex Rodriguez (EMR)\n*Status:* BLOCKED ❌"
                payload = {"chat_id": DEFAULT_TELEGRAM_CHAT_ID, "text": msg, "parse_mode": "Markdown"}
                requests.post(url, json=payload, timeout=3)
            except Exception:
                pass
            return False

        # Dispatch Telemetry Ping to Eduardo's Telegram
        try:
            url = f"https://api.telegram.org/bot{DEFAULT_TELEGRAM_TOKEN}/sendMessage"
            msg = f"🚀 *[AEGIS LICENSE TELEMETRY]*\nSoftware initiated by client!\n*Unique HWID:* `{self.hwid}`\n*Author:* Eduardo Mex Rodriguez (EMR)\n*Status:* AUTHORIZED ✅"
            payload = {"chat_id": DEFAULT_TELEGRAM_CHAT_ID, "text": msg, "parse_mode": "Markdown"}
            requests.post(url, json=payload, timeout=3)
            print(f"[+] Unique HWID '{self.hwid}' dispatched to Eduardo's phone.")
        except Exception:
            pass

        print(f"✅ [LICENSE VALID] Client '{self.hwid}' Authorized!")
        print("=" * 70)
        return True


if __name__ == "__main__":
    verifier = AegisLicenseVerifier()
    verifier.verify_and_telemetry()
