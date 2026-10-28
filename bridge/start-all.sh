#!/bin/sh
# Linux/macOS equivalent of start-all.bat — same steps, same order:
# cd to this script's dir, default BRIDGE_HOST, create .venv if missing,
# install requirements, then run bridge.py in the foreground.
set -eu
cd "$(dirname "$0")"

: "${BRIDGE_HOST:=127.0.0.1}"
export BRIDGE_HOST

if [ ! -x ".venv/bin/python" ]; then
    python3 -m venv .venv
fi

.venv/bin/python -m pip install -r requirements.txt

echo "Starting the local bridge on ${BRIDGE_HOST}:5000. Press Ctrl+C to stop."
echo "Remote binding requires BRIDGE_API_KEY; CORS is disabled unless configured."
exec .venv/bin/python bridge.py
