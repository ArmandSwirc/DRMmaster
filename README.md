# Adobe Digital Editions DRM removal tools

Remove Adobe ADEPT DRM from ebooks you own, so you can back them up and read
them on any device. Lossless - the decrypted PDF/EPUB is byte-identical to the
original (decryption does not re-encode anything).

## What this does

| Script | Purpose |
|--------|---------|
| `dedrm.py` | One command: point at an encrypted `.pdf`/`.epub`, get a clean copy |
| `adobekey.py` | Extract your Adobe ADEPT key (`adeptkey.der`) from an activated ADE install |
| `ineptpdf.py` | Low-level PDF decryptor (`key.der in.pdf out.pdf`) |
| `ineptepub.py` | Low-level EPUB decryptor (`key.der in.epub out.epub`) |

## Important: an .acsm is not the book

An `.acsm` file is a small *download ticket* (XML). It contains no book
content and no DRM - you cannot decrypt it directly. You must first
**fulfill** it to download the actual encrypted `.pdf`/`.epub`:

1. Install [Adobe Digital Editions](https://www.adobe.com/solutions/ebook/digital-editions.html)
   (free). Version 2.0.x is recommended.
2. Authorize it with a free **Adobe ID** (this particular `.acsm` uses
   `auth="user"`, so an anonymous device will not work).
3. Open the `.acsm` in ADE → it downloads the book to
   `~/Documents/Digital Editions/`.
4. (No-ADE alternative: [libgourou](https://forge.soutade.fr/Artem/libgourou)
   `adept_activate -u <adobeid>` then `acsmdownloader file.acsm`.)

## Usage

```bash
# one-time setup
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt

# one-time: extract your key (needs an activated ADE install)
python3 adobekey.py adeptkey.der

# decrypt a book (point at the file)
python3 dedrm.py "~/Documents/Digital Editions/MyBook.pdf"
# -> writes MyBook_clean.pdf next to the input
```

The key defaults to `adeptkey.der` in this folder; `dedrm.py` will try to
extract it automatically if it's missing.

## Scope / limitations

- Handles standard **Adobe ADEPT** DRM (Adobe Content Server 1-4) for PDF and
  EPUB. It does **not** remove the newer Adobe "hardened" DRM from ADE 4.5+,
  Amazon/Kindle, or Apple FairPlay DRM.
- macOS / Windows / Linux (the key extractor supports macOS and Windows).
- Requires `pycryptodome` (or an OpenSSL `libcrypto` on the system).

## Legal

For personal use on content you have legally obtained. Do not use to
distribute copyrighted works.

Code is GPL v3 - copyright © 2009-2020 i♥cabbages, Apprentice Harper et al.,
originally from <https://github.com/apprenticeharper/DeDRM_tools>.
