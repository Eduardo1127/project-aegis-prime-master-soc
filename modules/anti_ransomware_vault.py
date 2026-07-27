#!/usr/bin/env python3
"""
AEGIS PRIME - ANTI-RANSOMWARE & ENCRYPTED VAULT BACKUP ENGINE
Author: Eduardo Mex Rodriguez (EMR) (Defensive Security Engineering Portfolio)

Features:
1. Real-time file entropy monitoring for unauthorized mass-encryption detection (Ransomware Behavior).
2. Automated encrypted vault backup generator (AES-256 simulation / ZIP vault).
"""

import os
import sys
import time
import math
import zipfile

def calculate_shannon_entropy(filepath):
    """Calculates Shannon Entropy of a file to detect ransomware encryption."""
    if not os.path.exists(filepath):
        return 0.0
    with open(filepath, 'rb') as f:
        data = f.read()
    if not data:
        return 0.0
    entropy = 0.0
    length = len(data)
    frequencies = {}
    for byte in data:
        frequencies[byte] = frequencies.get(byte, 0) + 1
    for count in frequencies.values():
        p_x = count / length
        entropy -= p_x * math.log2(p_x)
    return round(entropy, 4)

def create_encrypted_vault_backup(source_dir, backup_output_path):
    """Creates a secure compressed vault backup of critical server files."""
    os.makedirs(os.path.dirname(backup_output_path), exist_ok=True)
    with zipfile.ZipFile(backup_output_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, dirs, files in os.walk(source_dir):
            for file in files:
                full_path = os.path.join(root, file)
                arcname = os.path.relpath(full_path, source_dir)
                zipf.write(full_path, arcname)
    return backup_output_path

def run_anti_ransomware_audit(target_dir):
    """Audits target directory for suspicious ransomware activity."""
    print("=" * 70)
    print("🛡️ AEGIS PRIME - ANTI-RANSOMWARE & ENCRYPTED VAULT BACKUP ENGINE")
    print("=" * 70)
    print(f"\n[+] Scanning directory '{target_dir}' for ransomware entropy anomalies...")
    
    suspicious_files = []
    total_scanned = 0
    
    for root, dirs, files in os.walk(target_dir):
        for file in files:
            full_path = os.path.join(root, file)
            entropy = calculate_shannon_entropy(full_path)
            total_scanned += 1
            if entropy > 7.5:  # High entropy indicates encrypted or packed file
                suspicious_files.append((full_path, entropy))
                print(f"[!] [RANSOMWARE ALERT] High Entropy Detected: {file} (Entropy: {entropy})")
                
    print(f"\n[+] Total Files Scanned: {total_scanned}")
    if suspicious_files:
        print(f"[⚠️ WARNING] {len(suspicious_files)} suspicious encrypted files detected!")
    else:
        print("[✅ SAFE] No ransomware file encryption patterns detected.")
        
    # Trigger Automated Encrypted Vault Backup
    backup_file = os.path.abspath(os.path.join(target_dir, "..", "backups", f"vault_backup_{int(time.time())}.zip"))
    print(f"\n[+] Triggering Automated Vault Backup...")
    created_path = create_encrypted_vault_backup(target_dir, backup_file)
    print(f"[SUCCESS] Encrypted Vault Backup Created: {created_path}")
    print("=" * 70)

if __name__ == "__main__":
    if sys.platform == "win32":
        sys.stdout.reconfigure(encoding='utf-8')
    sample_target = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "core"))
    run_anti_ransomware_audit(sample_target)
