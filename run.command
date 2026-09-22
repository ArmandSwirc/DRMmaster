#!/bin/bash
# Double-click me (macOS) — or run:  bash run.command
cd "$(dirname "$0")"

if ! command -v python3 >/dev/null 2>&1; then
  echo "Python 3 is required but not installed."
  echo "Install it once:  xcode-select --install"
  echo "(or download from https://www.python.org)"
  read -n 1 -s -r -p "Press any key to close..."
  echo
  exit 1
fi

python3 run.py
rc=$?

echo
if [ "$rc" -eq 0 ]; then
  read -n 1 -s -r -p "Done. Press any key to close this window..."
else
  read -n 1 -s -r -p "Something went wrong (exit $rc). Press any key to close..."
fi
echo
exit $rc
