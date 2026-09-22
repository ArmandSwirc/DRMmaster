# DRMmaster

Remove Adobe ADEPT DRM from a PDF you already have, so you can back it up and
read it anywhere. Lossless - decryption removes the encryption without
re-encoding, so the result is byte-identical to the original.

Works with current Adobe Digital Editions (including 4.5.x). Windows is fully
automatic: the launcher installs Python and everything else on first run.

## Windows: one click

1. Make sure **Adobe Digital Editions** is installed and authorized
   (*Help > Authorize Computer*, sign in with your Adobe ID). It must be the
   **same Adobe ID that downloaded the book**.
2. Double-click **`run.bat`**.

That's it. First run installs Python + dependencies automatically (~1 minute,
needs internet), then it finds your book (in *My Digital Editions*, OneDrive,
Downloads, or this folder), decrypts it, and writes a `<name>_clean.pdf` into
this folder.

> The book must already be downloaded and openable in Adobe Digital Editions.
> An `.acsm` file is *not* the book - it is only a download ticket.

## macOS / Linux

```bash
# macOS: double-click run.command   (or:)
python3 run.py
```

## How it works

| File | What it does |
|------|--------------|
| `run.bat` / `run.command` / `run.py` | One-click launcher: sets up Python, gets your key, finds + decrypts the PDF |
| `adobekey.py` | Extracts your Adobe ADEPT key (`adeptkey.der`) from an authorized ADE install (supports ADE 4.5.x) |
| `ineptpdf.py` | Decrypts an Adobe ADEPT-encrypted PDF |
| `dedrm.py` | Thin wrapper: `dedrm.py book.pdf [out.pdf] [key.der]` |

## Manual use (optional)

```bash
python3 adobekey.py adeptkey.der          # once: extract your key
python3 dedrm.py "C:\...\book.pdf"        # decrypt a single file
```

## Scope

- Standard **Adobe ADEPT** DRM (Adobe Content Server 1-4) for PDF.
- Key extraction supports Windows (registry) and macOS (`activation.dat`),
  including current Adobe Digital Editions 4.5.x.
- Does **not** remove Adobe "hardened" DRM (new Adept), Kindle, or Apple FairPlay.

## Legal

For personal use on content you have legally obtained. Do not use to
distribute copyrighted works.

Code is GPL v3 - copyright © 2009-2022 i♥cabbages, Apprentice Harper et al.,
from <https://github.com/noDRM/DeDRM_tools>.
