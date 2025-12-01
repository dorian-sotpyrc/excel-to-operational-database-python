#!/usr/bin/env bash
set -euo pipefail

# Simple helper to run the Excel -> DB pipeline using the default config.

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT_DIR"

CONFIG_PATH="config/config.yaml"

if [ ! -f "$CONFIG_PATH" ]; then
  echo "Config file '$CONFIG_PATH' not found."
  echo "Copying config/config.example.yaml as a starting point..."
  cp config/config.example.yaml "$CONFIG_PATH"
fi

echo "Using config: $CONFIG_PATH"
echo "Running dry-run first..."
python3 -m src.cli migrate --config "$CONFIG_PATH" --dry-run

echo
echo "Running full migration..."
python3 -m src.cli migrate --config "$CONFIG_PATH"
