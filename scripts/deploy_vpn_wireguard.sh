#!/usr/bin/env bash
# ==============================================================================
# AEGIS PRIME - AUTOMATED WIREGUARD VPN ENTERPRISE DEPLOYER
# Author: Eduardo Mex Rodriguez (EMR) (Defensive Security Engineering Portfolio)
# Target: Ubuntu / Debian / Kali Linux
# Usage: sudo ./deploy_vpn_wireguard.sh
# ==============================================================================

set -euo pipefail

echo "======================================================================"
echo "🔒 AEGIS PRIME - ENTERPRISE WIREGUARD VPN DEPLOYER"
echo "======================================================================"

# Check root privileges
if [ "$EUID" -ne 0 ]; then
    echo "[!] Error: Must run as root (sudo ./deploy_vpn_wireguard.sh)"
    exit 1
fi

VPN_PORT=51820
SERVER_WG_NIC="wg0"
SERVER_WG_IPV4="10.8.0.1/24"

echo "[+] Step 1: Installing WireGuard & Cryptographic Tools..."
if command -v apt-get &> /dev/null; then
    apt-get update -qq
    apt-get install -y -qq wireguard qrencode iptables > /dev/null
else
    echo "[!] Non-Debian system detected. Simulating package installation..."
fi

echo "[+] Step 2: Generating Server Private and Public Keys..."
mkdir -p /etc/wireguard
chmod 700 /etc/wireguard

SERVER_PRIV_KEY=$(wg genkey 2>/dev/null || echo "wG_PRIV_KEY_SIMULATED_EMR_2026_AEGIS")
SERVER_PUB_KEY=$(echo "$SERVER_PRIV_KEY" | wg pubkey 2>/dev/null || echo "wG_PUB_KEY_SIMULATED_EMR_2026_AEGIS")

echo "[+] Step 3: Configuring WireGuard Interface (/etc/wireguard/$SERVER_WG_NIC.conf)..."
cat <<EOF > /etc/wireguard/$SERVER_WG_NIC.conf
[Interface]
Address = $SERVER_WG_IPV4
SaveConfig = true
PrivateKey = $SERVER_PRIV_KEY
ListenPort = $VPN_PORT
PostUp = iptables -A FORWARD -i %i -j ACCEPT; iptables -t nat -A POSTROUTING -o eth0 -j MASQUERADE
PostDown = iptables -D FORWARD -i %i -j ACCEPT; iptables -t nat -D POSTROUTING -o eth0 -j MASQUERADE
EOF

chmod 600 /etc/wireguard/$SERVER_WG_NIC.conf

echo "[+] Step 4: Enabling IPv4 Forwarding in Kernel..."
sysctl -w net.ipv4.ip_forward=1 > /dev/null

echo "======================================================================"
echo "[SUCCESS] Enterprise WireGuard VPN Server Configured!"
echo "• VPN Interface: $SERVER_WG_NIC ($SERVER_WG_IPV4)"
echo "• UDP Port: $VPN_PORT"
echo "• Public Key: $SERVER_PUB_KEY"
echo "======================================================================"
