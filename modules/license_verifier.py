#!/usr/bin/env python3
"""
AEGIS PRIME - REMOTE LICENSE VERIFIER & GITHUB TELEMETRY ENGINE
Author: Eduardo Mex Rodriguez (EMR)

Features:
1. Real-time Remote Revocation Check against Eduardo's live GitHub Gist URL.
2. Immediate execution block if license key is listed as revoked on GitHub.
3. Instant Telegram push alert upon software launch.
"""

import sys
import json
import requests

# Live GitHub Gist Revocation URL (Managed by Eduardo Mex Rodriguez - Eduardo1127)
GITHUB_REVOCATION_URL = "https://gist.githubusercontent.com/Eduardo1127/02ba956d3504f63c480680e28a96eb67/raw/revoked_licenses.txt"
DEFAULT_TELEGRAM_TOKEN = "8893915158:AAFWy8WTn2sXP0_GXgRFEKsOkGtMeOfpie0"
DEFAULT_TELEGRAM_CHAT_ID = "8926630685"

class AegisLicenseVerifier:
    def __init__(self, license_key="LIC-CLIENTE-DEFAULT-2026"):
        self.license_key = license_key

    def check_github_revocation(self):
        """Fetches live revoked license list from Eduardo's GitHub Gist."""
        try:
            r = requests.get(GITHUB_REVOCATION_URL, timeout=4)
            if r.status_code == 200:
                revoked_list = [line.strip() for line in r.text.splitlines() if line.strip()]
                return revoked_list
        except Exception as e:
            print(f"[WARN] Remote Revocation Check Offline: {e}")
        return []

    def verify_and_telemetry(self):
        if sys.platform == "win32":
            try:
                sys.stdout.reconfigure(encoding='utf-8')
            except Exception:
                pass
        print("=" * 70)
        print("🔑 AEGIS PRIME - REMOTE LICENSE & TELEMETRY VERIFIER")
        print("   Author: Eduardo Mex Rodriguez (EMR)")
        print("=" * 70)
        print(f"[+] Verifying License Key: '{self.license_key}'...")

        # 1. Check live GitHub Gist list
        revoked_list = self.check_github_revocation()
        
        if self.license_key in revoked_list or self.license_key.startswith("REVOKED"):
            print("\n❌ [ACCESS DENIED] Your Aegis Prime License Key has been REVOKED.")
            print("   Execution blocked. Please contact Eduardo Mex Rodriguez (EMR) for renewal.")
            print("=" * 70)
            
            # Send Telegram alert for unauthorized / revoked launch
            try:
                url = f"https://api.telegram.org/bot{DEFAULT_TELEGRAM_TOKEN}/sendMessage"
                msg = f"🚨 *[AEGIS ACCESS DENIED]*\nA revoked client tried to launch the software!\n*License Key:* `{self.license_key}`\n*Author:* Eduardo Mex Rodriguez (EMR)\n*Status:* BLOCKED ❌"
                payload = {"chat_id": DEFAULT_TELEGRAM_CHAT_ID, "text": msg, "parse_mode": "Markdown"}
                requests.post(url, json=payload, timeout=3)
            except Exception:
                pass
            return False

        # 2. Dispatch Telemetry Ping to Telegram for Authorized Launch
        try:
            url = f"https://api.telegram.org/bot{DEFAULT_TELEGRAM_TOKEN}/sendMessage"
            msg = f"🚀 *[AEGIS LICENSE TELEMETRY]*\nSoftware initiated by authorized client!\n*License Key:* `{self.license_key}`\n*Author:* Eduardo Mex Rodriguez (EMR)\n*Status:* AUTHORIZED ✅"
            payload = {"chat_id": DEFAULT_TELEGRAM_CHAT_ID, "text": msg, "parse_mode": "Markdown"}
            requests.post(url, json=payload, timeout=3)
            print("[+] Telemetry notification dispatched to Eduardo's phone.")
        except Exception:
            pass

        print("✅ [LICENSE VALID] Aegis Prime Execution Authorized!")
        print("=" * 70)
        return True

if __name__ == "__main__":
    if sys.platform == "win32":
        sys.stdout.reconfigure(encoding='utf-8')
    verifier = AegisLicenseVerifier()
    if not verifier.verify_and_telemetry():
        sys.exit(1)
