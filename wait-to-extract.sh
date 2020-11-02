#!/bin/bash
set -Eeuo pipefail

DOWNLOADS="$PWD/downloads"

echo "- Waiting for the theme to download..."
while ! ls "$DOWNLOADS" | grep "Chiara.*\.zip$" &> /dev/null; do
    sleep 1
done

./extract-config.sh "$@"
