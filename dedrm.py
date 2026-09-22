#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""dedrm.py - point at an Adobe ADEPT PDF, get a clean copy.

Usage:
    python3 dedrm.py <book.pdf> [out.pdf] [key.der]

    out.pdf  default: <book>_clean.pdf
    key.der  default: adeptkey.der in this folder

If the key file is missing, we try to extract it from an installed and
authorized copy of Adobe Digital Editions (via adobekey.py).

Note: an .acsm file is *not* the book - it is a download ticket. Open it in
Adobe Digital Editions first to obtain the real .pdf, then run this on that.
"""

import os
import sys

import ineptpdf
import adobekey


def clean_name(path):
    base, ext = os.path.splitext(path)
    return base + "_clean" + ext


def load_key(keypath):
    if os.path.exists(keypath):
        with open(keypath, "rb") as f:
            return f.read()
    print("No key at {0}, trying to extract from Adobe Digital Editions..."
          .format(keypath))
    try:
        if adobekey.getkey(keypath):
            print("Saved key to {0}".format(keypath))
            with open(keypath, "rb") as f:
                return f.read()
    except Exception as e:
        print("Could not extract key: {0}".format(e))
    print("Authorize Adobe Digital Editions (with your Adobe ID), then re-run.")
    return None


def main(argv):
    if not argv or argv[0] in ("-h", "--help"):
        print(__doc__)
        return 1

    inpath = argv[0]
    if not os.path.exists(inpath):
        print("File not found: {0}".format(inpath))
        return 1

    if os.path.splitext(inpath)[1].lower() != ".pdf":
        print("Expected a .pdf file (not {0}).".format(inpath))
        return 1

    outpath = argv[1] if len(argv) > 1 else clean_name(inpath)
    keypath = argv[2] if len(argv) > 2 else "adeptkey.der"

    userkey = load_key(keypath)
    if userkey is None:
        return 1

    rc = ineptpdf.decryptBook(userkey, inpath, outpath)
    if rc == 0:
        print("Clean file written to {0}".format(outpath))
    else:
        print("Decryption failed (exit {0}).".format(rc))
    return rc


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
