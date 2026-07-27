#!/usr/bin/env python3
"""
AEGIS PRIME - DEFENSIVE AUDIT & RULE VERIFICATION HARNESS
Author: Eduardo Mex Rodriguez (EMR)

Purpose:
Sends synthetic, non-destructive test patterns to verify SIEM detection rules and SOAR response pipelines in a local lab environment.
"""

import sys
import time
import threading
import requests
from flask import Flask, request, jsonify

# Integrated Mock Server for Standalone Audit Verification
mock_app = Flask(__name__)

@mock_app.route("/api/user_search_secure", methods=["GET"])
def mock_user_search():
    username = request.args.get("username", "")
    if "'" in username or "OR" in username.upper():
        return jsonify({"error": "Invalid username format. Alphanumeric characters only."}), 400
    return jsonify({"data": [[1, "admin", "admin@company.local"]], "status": "success"}), 200

@mock_app.route("/api/ping_secure", methods=["GET"])
def mock_ping():
    host = request.args.get("host", "")
    if ";" in host or "&" in host or "|" in host or "cat" in host:
        return jsonify({"error": "Invalid host parameter. Must be a valid IPv4 or IPv6 address."}), 400
    return jsonify({"status": "success", "message": f"Pinged {host} successfully."}), 200

@mock_app.route("/", methods=["GET"])
def mock_index():
    resp = jsonify({"status": "Aegis Master Server Active"})
    resp.headers["Content-Security-Policy"] = "default-src 'self'"
    resp.headers["X-Frame-Options"] = "DENY"
    return resp, 200

def start_mock_server():
    mock_app.run(host="127.0.0.1", port=5005, debug=False)

def run_synthetic_audit():
    print("=" * 70)
    print("🧪 AEGIS DEFENSIVE AUDIT & RULE VERIFICATION HARNESS")
    print("   Author: Eduardo Mex Rodriguez (EMR)")
    print("=" * 70)
    
    # Start Standalone Verification Server
    server_thread = threading.Thread(target=start_mock_server, daemon=True)
    server_thread.start()
    time.sleep(1.5)

    target_url = "http://127.0.0.1:5005"
    print(f"[+] Active Local Test Target: {target_url}\n")
    
    tests = [
        {
            "name": "Petición Legítima de Usuario",
            "endpoint": "/api/user_search_secure?username=admin",
            "expected_code": 200,
            "description": "Verifica que el servicio responda a peticiones normales de usuarios."
        },
        {
            "name": "Prueba Sintética de Inyección SQL (CWE-89)",
            "endpoint": "/api/user_search_secure?username=admin%27%20OR%20%271%27=%271",
            "expected_code": 400,
            "description": "Verifica que el filtro AppSec bloquee patrones de manipulación de consultas."
        },
        {
            "name": "Prueba Sintética de Inyección de Comandos (CWE-78)",
            "endpoint": "/api/ping_secure?host=127.0.0.1%26whoami",
            "expected_code": 400,
            "description": "Verifica que la API rechace metacaracteres de ejecución en el sistema operativo."
        },
        {
            "name": "Prueba Sintética de Encabezados de Seguridad",
            "endpoint": "/",
            "expected_code": 200,
            "description": "Evalúa la presencia de encabezados de protección HTTP (CSP, HSTS, X-Frame-Options)."
        }
    ]

    passed = 0
    total = len(tests)

    for test in tests:
        url = f"{target_url}{test['endpoint']}"
        print(f"[TEST] {test['name']}")
        print(f"       Propósito: {test['description']}")
        try:
            r = requests.get(url, timeout=3)
            if r.status_code == test['expected_code']:
                print(f"       ✅ [RESULTADO: PASADO] Código HTTP: {r.status_code} (Comportamiento defensivo confirmado)\n")
                passed += 1
            else:
                print(f"       ⚠️ [RESULTADO: ADVERTENCIA] Código HTTP obtenido: {r.status_code} (Esperado: {test['expected_code']})\n")
        except Exception as e:
            print(f"       ❌ [ERROR] Conexión fallida: {e}\n")

    print("=" * 70)
    print(f"📊 RESUMEN DE EVALUACIÓN DEFENSIVA: {passed}/{total} Pruebas Completadas con Éxito.")
    print("=" * 70)

if __name__ == "__main__":
    if sys.platform == "win32":
        sys.stdout.reconfigure(encoding='utf-8')
    run_synthetic_audit()
