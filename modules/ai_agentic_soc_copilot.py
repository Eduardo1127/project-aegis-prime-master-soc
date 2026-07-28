#!/usr/bin/env python3
"""
AEGIS PRIME - AI AGENTIC SOC COPILOT & INCIDENT EXPLAINER
Author: Eduardo Mex Rodriguez (EMR)

Purpose:
Simulates an Enterprise AI Security Copilot (similar to Microsoft Security Copilot & Google Security AI).
Takes raw SIEM incident alerts and uses AI natural language analysis to generate:
1. Executive Incident Summaries in Plain Spanish.
2. Attack Vector Analysis & MITRE ATT&CK Correlation.
3. Automated Tactical Remediation Playbooks.
"""

import sys
import json
import datetime

if sys.platform == "win32":
    sys.stdout.reconfigure(encoding='utf-8')


class AgenticSOCCopilot:
    def __init__(self):
        self.timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    def analyze_incident(self, incident_data):
        """Analyzes an incident log and produces an AI Agentic Copilot Executive Report."""
        print("=" * 70)
        print("🤖 AEGIS AI AGENTIC SOC COPILOT — INCIDENT ANALYSIS")
        print("   Author: Eduardo Mex Rodriguez (EMR)")
        print("=" * 70)
        print(f"[+] Analyzing Incident Alert: {incident_data.get('incident_id', 'INC-UNKNOWN')}...\n")

        attack_type = incident_data.get("attack_type", "Unknown Threat")
        source_ip = incident_data.get("source_ip", "0.0.0.0")
        target_service = incident_data.get("target_service", "Web Gateway")
        mitre_technique = incident_data.get("mitre_id", "T1059")
        raw_payload = incident_data.get("payload", "")

        # AI Agent Reasoning Engine
        severity = "HIGH" if "injection" in attack_type.lower() or "brute" in attack_type.lower() else "CRITICAL"
        threat_score = 88.5 if severity == "HIGH" else 96.0

        ai_narrative = (
            f"El copiloto de IA ha detectado un intento de ataque de tipo '{attack_type}' procedente de la IP externa "
            f"{source_ip} hacia el servicio '{target_service}'. El atacante intentó ejecutar cargas maliciosas "
            f"('{raw_payload}') utilizando la técnica catalogada en MITRE ATT&CK como {mitre_technique}. "
            f"El motor defensivo de Aegis contuvo la amenaza automáticamente con un score de confianza del {threat_score}%."
        )

        playbook_recommendations = [
            f"1. Mantener bloqueada la IP {source_ip} en el Firewall (UFW / iptables) por 72 horas.",
            f"2. Auditar los registros del servicio {target_service} en busca de peticiones secundarias.",
            "3. Verificar la rotación de credenciales administrativas de acceso remoto.",
            "4. Exportar el reporte Syslog CEF a Splunk Enterprise para correlación de eventos."
        ]

        report = {
            "copilot_version": "Aegis AI Agentic Copilot v2.0",
            "author": "Eduardo Mex Rodriguez (EMR)",
            "timestamp": self.timestamp,
            "incident_id": incident_data.get("incident_id", "INC-001"),
            "severity": severity,
            "threat_score": threat_score,
            "ai_executive_summary": ai_narrative,
            "recommended_playbook": playbook_recommendations
        }

        # Print AI Copilot Output
        print(f"📌 INCIDENT ID:        {report['incident_id']}")
        print(f"🚨 SEVERITY LEVEL:     {report['severity']} (Threat Score: {report['threat_score']}/100)")
        print("\n📝 AI EXECUTIVE SUMMARY (PLAIN SPANISH):")
        print(f"   \"{report['ai_executive_summary']}\"\n")
        print("🛡️ AI RECOMMENDED REMEDIATION PLAYBOOK:")
        for rec in report['recommended_playbook']:
            print(f"   {rec}")

        print("\n" + "=" * 70)
        print("✅ AI AGENTIC COPILOT INCIDENT BRIEFING COMPLETE")
        print("=" * 70)

        return report


if __name__ == "__main__":
    copilot = AgenticSOCCopilot()
    sample_incident = {
        "incident_id": "INC-2026-8819",
        "attack_type": "Command Injection (CWE-78)",
        "source_ip": "185.220.101.5",
        "target_service": "API Gateway /api/ping_secure",
        "mitre_id": "T1059.004 (Unix Shell Execution)",
        "payload": "127.0.0.1; cat /etc/passwd"
    }
    copilot.analyze_incident(sample_incident)
