#!/usr/bin/env bash

set -euo pipefail

APP_NAME="sync-sl"
INSTALL_DIR="/opt/$APP_NAME"
CONFIG_DIR="/etc/$APP_NAME"
BIN_PATH="/usr/local/bin/$APP_NAME"

SOURCE_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

echo "[/] Installing Sync_SL..."

# Require root
if [[ "$EUID" -ne 0 ]]; then
    echo "[X] Please run: sudo ./install.sh"
    exit 1
fi

# Check required files
for file in app.py ini_parser.py requirements.txt config.ini; do
    if [[ ! -f "$SOURCE_DIR/$file" ]]; then
        echo "[X] Missing required file: $file"
        exit 1
    fi
done

# Install application directory
mkdir -p "$INSTALL_DIR"

echo "[/] Copying application files..."

install -m 644 "$SOURCE_DIR/app.py" "$INSTALL_DIR/app.py"
install -m 644 "$SOURCE_DIR/ini_parser.py" "$INSTALL_DIR/ini_parser.py"
install -m 644 "$SOURCE_DIR/requirements.txt" "$INSTALL_DIR/requirements.txt"

# Install configuration directory
mkdir -p "$CONFIG_DIR"

# Preserve existing configuration
if [[ ! -f "$CONFIG_DIR/config.ini" ]]; then
    install -m 600 "$SOURCE_DIR/config.ini" "$CONFIG_DIR/config.ini"
    echo "[+] Configuration installed"
else
    echo "[!] Existing configuration preserved"
fi

# Create Python virtual environment
if [[ ! -x "$INSTALL_DIR/.venv/bin/python" ]]; then
    echo "[/] Creating Python virtual environment..."
    python3 -m venv "$INSTALL_DIR/.venv"
fi

# Install Python dependencies
echo "[/] Installing dependencies..."

"$INSTALL_DIR/.venv/bin/python" -m pip install \
    -r "$INSTALL_DIR/requirements.txt"

# Create executable launcher
echo "[/] Creating command..."

cat > "$BIN_PATH" <<'EOF'
#!/usr/bin/env bash

set -e

APP_DIR="/opt/sync-sl"
PYTHON="$APP_DIR/.venv/bin/python"
APP="$APP_DIR/app.py"

if [[ ! -f "$APP" ]]; then
    echo "[X] Sync_SL application not found"
    exit 1
fi

if [[ ! -f "/etc/sync-sl/config.ini" ]]; then
    echo "[X] Configuration file not found"
    exit 1
fi

exec "$PYTHON" "$APP" "$@"
EOF

chmod 755 "$BIN_PATH"
chmod 755 "$INSTALL_DIR"

echo ""
echo "[+] Sync_SL installed successfully!"
echo "[+] Application: $INSTALL_DIR"
echo "[+] Configuration: $CONFIG_DIR/config.ini"
echo "[+] Command: $BIN_PATH"
echo ""
echo "Run using: sync-sl"
