#!/usr/bin/env bash

set -euo pipefail

APP_NAME="sync-sl"

INSTALL_DIR="/opt/$APP_NAME"
CONFIG_DIR="/etc/$APP_NAME"
BIN_PATH="/usr/local/bin/$APP_NAME"

echo "[/] Uninstalling Sync_SL..."

# Require root
if [[ "$EUID" -ne 0 ]]; then
    echo "[X] Please run: sudo ./uninstall.sh"
    exit 1
fi

echo ""
echo "The following will be removed:"
echo "  - $INSTALL_DIR"
echo "  - $BIN_PATH"
echo ""
echo "The following will be preserved:"
echo "  - $CONFIG_DIR"
echo ""

read -rp "Continue uninstalling? [y/N]: " answer

if [[ ! "$answer" =~ ^[Yy]$ ]]; then
    echo "[!] Uninstallation cancelled."
    exit 0
fi

# Remove application
if [[ -d "$INSTALL_DIR" ]]; then
    rm -rf -- "$INSTALL_DIR"
    echo "[+] Application removed"
fi

# Remove launcher
if [[ -f "$BIN_PATH" ]]; then
    rm -f -- "$BIN_PATH"
    echo "[+] Launcher removed"
fi

echo ""
echo "[+] Sync_SL uninstalled successfully!"
echo "[+] Configuration preserved at: $CONFIG_DIR"
