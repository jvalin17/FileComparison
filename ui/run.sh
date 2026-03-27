#!/bin/bash
cd "$(dirname "$0")"

# Try python commands in order of preference
for cmd in python3.14 python3 python; do
    if command -v "$cmd" > /dev/null 2>&1; then
        if "$cmd" -c "import tkinter" 2>/dev/null; then
            echo "Using: $cmd"
            exec "$cmd" app.py
        fi
    fi
done

echo "Error: No Python with tkinter found."
echo "Install tkinter: brew install python-tk@3.14 (macOS) or apt install python3-tk (Linux)"
exit 1
