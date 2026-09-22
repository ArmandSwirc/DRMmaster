#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""run.py - the one-click entry point (Windows / macOS / Linux).

Sets up Python + dependencies if needed, extracts your Adobe key, finds the
encrypted book, and decrypts it into this folder as <name>_clean.<ext>.

On Windows you normally just double-click run.bat (which handles Python too);
on macOS double-click run.command. This script can also be run directly.
"""

import os
import sys
import glob
import shutil
import subprocess

HERE = os.path.dirname(os.path.abspath(__file__))
os.chdir(HERE)
IS_WIN = os.name == "nt"


def venv_python():
    return os.path.join(HERE, ".venv",
                        "Scripts" if IS_WIN else "bin",
                        "python.exe" if IS_WIN else "python")


def ensure_env():
    """Return the python to use, installing pycryptodome if needed."""
    # already running in an env that has pycryptodome?
    try:
        import Crypto  # noqa: F401
        return sys.executable
    except ImportError:
        pass
    # an existing venv?
    vpy = venv_python()
    if os.path.exists(vpy):
        p = subprocess.run([vpy, "-c", "import Crypto"], capture_output=True)
        if p.returncode == 0:
            return vpy
    # create one
    print("Setting up Python environment (one-time)...")
    if IS_WIN:
        py = shutil.which("python")
    else:
        py = shutil.which("python3") or shutil.which("python")
    if py is None:
        print("Python 3 is required but not found. Install it from python.org.")
        sys.exit(1)
    subprocess.check_call([py, "-m", "venv", ".venv"])
    pip = os.path.join(HERE, ".venv",
                       "Scripts" if IS_WIN else "bin",
                       "pip.exe" if IS_WIN else "pip")
    subprocess.check_call([pip, "install", "-q", "-r", "requirements.txt"])
    return venv_python()


def ensure_key(py):
    keypath = os.path.join(HERE, "adeptkey.der")
    if os.path.exists(keypath):
        return keypath
    print("Extracting your Adobe key...")
    r = subprocess.run([py, "adobekey.py", keypath])
    if r.returncode != 0 or not os.path.exists(keypath):
        print()
        print("Could not get the key. Authorize Adobe Digital Editions once "
              "(Help > Authorize Computer, sign in with your Adobe ID), "
              "then run me again.")
        sys.exit(1)
    print("Key saved.")
    return keypath


def find_books():
    home = os.path.expanduser("~")
    # OneDrive may be "OneDrive" or "OneDrive - Company Name"
    roots = [home] + [d for d in glob.glob(os.path.join(home, "OneDrive*"))
                      if os.path.isdir(d)]
    dirs = [HERE]
    for r in roots:
        dirs += [
            os.path.join(r, "Documents", "My Digital Editions"),
            os.path.join(r, "Documents", "Digital Editions"),
            os.path.join(r, "Downloads"),
        ]
    books, seen = [], set()
    for d in dirs:
        if not os.path.isdir(d):
            continue
        for ext in ("pdf",):
            for f in sorted(glob.glob(os.path.join(d, "*." + ext))):
                if "_clean" in os.path.basename(f):
                    continue
                if f not in seen:
                    seen.add(f)
                    books.append(f)
    return books


def open_path(path):
    if sys.platform == "darwin":
        subprocess.run(["open", path])
    elif hasattr(os, "startfile"):
        os.startfile(path)
    else:
        print(path)


def main():
    py = ensure_env()
    keypath = ensure_key(py)

    books = find_books()
    if not books:
        acsms = glob.glob(os.path.join(HERE, "*.acsm"))
        if acsms:
            print("Found an .acsm but no downloaded book. "
                  "Opening it in Adobe Digital Editions...")
            open_path(acsms[0])
            print("Once ADE finishes downloading, run me again.")
        else:
            print("Nothing to decrypt. Put your .pdf/.epub in this folder, "
                  "then run me again.")
        return 0

    for b in books:
        out = os.path.join(
            HERE,
            os.path.splitext(os.path.basename(b))[0] + "_clean"
            + os.path.splitext(b)[1])
        print()
        print("Decrypting: " + b)
        subprocess.run([py, "dedrm.py", b, out, keypath])

    print()
    print("Done. Clean file(s) are in this folder:")
    for b in books:
        print("  " + os.path.splitext(os.path.basename(b))[0] + "_clean"
              + os.path.splitext(b)[1])
    open_path(HERE)
    return 0


if __name__ == "__main__":
    sys.exit(main())
