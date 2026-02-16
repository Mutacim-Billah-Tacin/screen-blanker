#!/bin/bash

# 1. Auto-detect the keyboard event ID
KBD_EVENT=$(grep -E 'Handlers|EV=' /proc/bus/input/devices | \
            grep -B1 'EV=120013' | \
            grep -Eo 'event[0-9]+' | head -n 1)

if [ -z "$KBD_EVENT" ]; then
    echo "[ERROR] No keyboard detected via EV=120013 bitmask."
    exit 1
fi

DEVICE="/dev/input/$KBD_EVENT"
echo "[SUCCESS] Found keyboard at: $DEVICE"

# 2. Capture Test
echo "Press F6 now (or Ctrl+C to stop)..."

# We use 'stdbuf' to ensure the output isn't buffered (delayed)
stdbuf -oL evtest "$DEVICE" | while read line; do
    # Log every key event to the console so you can see if F6 has a different name
    if [[ "$line" == *"value 1"* ]]; then
        echo "[LOG] Key Pressed: $(echo $line | grep -Po '\(KEY_.*?\)')"
    fi

    if [[ "$line" == *"(KEY_F6), value 1"* ]]; then
        echo "--------------------------------------"
        echo "!!! F6 DETECTED - TRIGGERING PYTHON !!!"
        echo "--------------------------------------"
        # For testing, we just try to print the python version instead of launching
        python3 --version
    fi
done
