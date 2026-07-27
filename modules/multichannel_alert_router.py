#!/usr/bin/env python3
"""
AEGIS PRIME - MULTI-CHANNEL SOAR ALERT ROUTER (TELEGRAM, DISCORD, SLACK)
Author: Eduardo Mex Rodriguez (EMR) (Defensive Security Engineering Portfolio)

Features:
1. Unified dispatch of security incident alerts across Telegram, Discord Webhooks, and Slack Webhooks.
2. Color-coded severity formatting (CRITICAL, HIGH, MEDIUM, INFO).
"""

import os
import sys
import json
import requests

class MultiChannelAlertRouter:
    def __init__(self, telegram_token=None, telegram_chat_id=None, discord_webhook=None, slack_webhook=None):
        self.telegram_token = telegram_token
        self.telegram_chat_id = telegram_chat_id
        self.discord_webhook = discord_webhook
        self.slack_webhook = slack_webhook

    def send_telegram_alert(self, title, message, severity):
        if not self.telegram_token or not self.telegram_chat_id:
            print("[INFO] Telegram alert skipped (Token or Chat ID not configured).")
            return False
        
        icon = "🔴" if severity == "CRITICAL" else ("🟠" if severity == "HIGH" else "🟡")
        full_msg = f"{icon} *[AEGIS SOAR ALERT]*\n*Severity:* {severity}\n*Title:* {title}\n\n{message}"
        
        url = f"https://api.telegram.org/bot{self.telegram_token}/sendMessage"
        payload = {"chat_id": self.telegram_chat_id, "text": full_msg, "parse_mode": "Markdown"}
        try:
            r = requests.post(url, json=payload, timeout=5)
            if r.status_code == 200:
                print("[SUCCESS] Telegram Alert Dispatched.")
                return True
        except Exception as e:
            print(f"[ERROR] Telegram Alert Failed: {e}")
        return False

    def send_discord_webhook(self, title, message, severity):
        if not self.discord_webhook:
            print("[INFO] Discord alert skipped (Webhook URL not configured).")
            return False
            
        color = 15158332 if severity == "CRITICAL" else (15105570 if severity == "HIGH" else 3066993)
        payload = {
            "embeds": [{
                "title": f"🛡️ AEGIS SOAR ALERT: {title}",
                "description": message,
                "color": color,
                "fields": [
                    {"name": "Severity", "value": severity, "inline": True},
                    {"name": "Status", "value": "Mitigation Pending", "inline": True}
                ],
                "footer": {"text": "Aegis Prime Master SOC Engine • EMR Security"}
            }]
        }
        try:
            r = requests.post(self.discord_webhook, json=payload, timeout=5)
            if r.status_code in [200, 204]:
                print("[SUCCESS] Discord Webhook Alert Dispatched.")
                return True
        except Exception as e:
            print(f"[ERROR] Discord Webhook Failed: {e}")
        return False

    def send_slack_webhook(self, title, message, severity):
        if not self.slack_webhook:
            print("[INFO] Slack alert skipped (Webhook URL not configured).")
            return False
            
        payload = {
            "text": f"*:warning: AEGIS SOAR ALERT [{severity}]: {title}*\n```{message}```"
        }
        try:
            r = requests.post(self.slack_webhook, json=payload, timeout=5)
            if r.status_code == 200:
                print("[SUCCESS] Slack Webhook Alert Dispatched.")
                return True
        except Exception as e:
            print(f"[ERROR] Slack Webhook Failed: {e}")
        return False

    def broadcast_incident(self, title, message, severity="HIGH"):
        print("=" * 70)
        print(f"📢 BROADCASTING MULTI-CHANNEL INCIDENT ALERT [{severity}]")
        print("=" * 70)
        self.send_telegram_alert(title, message, severity)
        self.send_discord_webhook(title, message, severity)
        self.send_slack_webhook(title, message, severity)
        print("=" * 70)

if __name__ == "__main__":
    if sys.platform == "win32":
        sys.stdout.reconfigure(encoding='utf-8')
    
    router = MultiChannelAlertRouter(
        telegram_token="8893915158:AAFWy8WTn2sXP0_GXgRFEKsOkGtMeOfpie0",
        telegram_chat_id="8926630685"
    )
    router.broadcast_incident(
        title="Unauthorized Privilege Escalation & Command Injection",
        message="Source IP: 192.168.1.227 attempted 'cat /etc/passwd' via web API endpoint /api/ping_secure.",
        severity="CRITICAL"
    )
