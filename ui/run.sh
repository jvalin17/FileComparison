#!/bin/bash
cd "$(dirname "$0")"

# Find a Python with tkinter
find_python() {
    for cmd in python3.14 python3 python; do
        if command -v "$cmd" > /dev/null 2>&1; then
            if "$cmd" -c "import tkinter" 2>/dev/null; then
                echo "$cmd"
                return 0
            fi
        fi
    done
    return 1
}

PYTHON=$(find_python)

if [ -n "$PYTHON" ]; then
    echo "Using: $PYTHON"
    exec "$PYTHON" app.py
fi

# No Python with tkinter found — try to install automatically
echo "tkinter not found. Attempting to install..."

if [ "$(uname)" = "Darwin" ]; then
    # macOS
    if command -v brew > /dev/null 2>&1; then
        echo "Installing python-tk via Homebrew..."
        brew install python-tk@3.14 2>&1
        PYTHON=$(find_python)
        if [ -n "$PYTHON" ]; then
            echo "Using: $PYTHON"
            exec "$PYTHON" app.py
        fi
    else
        echo "Homebrew not found. Install it from https://brew.sh then re-run this script."
        exit 1
    fi
elif command -v dnf > /dev/null 2>&1; then
    # Fedora/RHEL
    echo "Installing python3-tkinter via dnf..."
    sudo dnf install -y python3-tkinter 2>&1
    PYTHON=$(find_python)
    if [ -n "$PYTHON" ]; then
        echo "Using: $PYTHON"
        exec "$PYTHON" app.py
    fi
elif command -v apt > /dev/null 2>&1; then
    # Debian/Ubuntu
    echo "Installing python3-tk via apt..."
    sudo apt install -y python3-tk 2>&1
    PYTHON=$(find_python)
    if [ -n "$PYTHON" ]; then
        echo "Using: $PYTHON"
        exec "$PYTHON" app.py
    fi
fi

echo "Error: Could not install tkinter automatically."
echo "Please install manually:"
echo "  macOS:         brew install python-tk@3.14"
echo "  Ubuntu/Debian: sudo apt install python3-tk"
echo "  Fedora/RHEL:   sudo dnf install python3-tkinter"
exit 1
