#!/usr/bin/env python3
"""Audit a product image folder before listing.

Usage: python3 audit_folder.py "/path/to/SKU-FOLDER" [--colours BLACK,WHITE,RED,GREY,NAVY]

Prints a per-colour count table and a list of problems (missing FRONT,
unexpected counts, stray files). Exit code 1 if a blocking problem is found.
"""
import argparse
import os
import sys

IMG_EXT = {".jpg", ".jpeg", ".png", ".webp", ".avif"}
EXPECTED = {
    "01_FRONT": (1, 1),
    "02_BACK": (1, 1),
    "03_SIDE": (1, 1),
    "04_GALLERY": (1, 10),
    "05_MODEL": (1, 10),
    "06_CART": (1, 1),
    "07_FABRIC_MICRO": (0, 6),
}


def images(path):
    if not os.path.isdir(path):
        return []
    return sorted(
        f for f in os.listdir(path)
        if not f.startswith(".") and os.path.splitext(f)[1].lower() in IMG_EXT
    )


def find_dir(parent, name):
    """Case-insensitive sub-directory lookup."""
    if not os.path.isdir(parent):
        return None
    for d in os.listdir(parent):
        if d.upper() == name.upper() and os.path.isdir(os.path.join(parent, d)):
            return os.path.join(parent, d)
    return None


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("folder")
    ap.add_argument("--colours", default="BLACK,WHITE,RED,GREY,NAVY")
    a = ap.parse_args()

    root = os.path.abspath(a.folder)
    if not os.path.isdir(root):
        print(f"ERROR: folder not found: {root}")
        sys.exit(1)

    colours = [c.strip().upper() for c in a.colours.split(",") if c.strip()]
    blocking, warnings = [], []
    print(f"SKU folder: {os.path.basename(root)}\n")
    header = "COLOUR".ljust(8) + "".join(k[:9].ljust(11) for k in EXPECTED)
    print(header)

    for c in colours:
        cdir = find_dir(root, c)
        if not cdir:
            blocking.append(f"{c}: colour folder missing")
            print(c.ljust(8) + "missing")
            continue
        row = c.ljust(8)
        for sub, (lo, hi) in EXPECTED.items():
            sdir = find_dir(cdir, sub)
            n = len(images(sdir)) if sdir else 0
            row += str(n).ljust(11)
            if sub == "01_FRONT" and n == 0:
                blocking.append(f"{c}: no 01_FRONT image (Main image is required)")
            elif n < lo or n > hi:
                warnings.append(f"{c}/{sub}: {n} images (expected {lo}-{hi})")
        print(row)
        # files that mention another colour in their name
        for sub in EXPECTED:
            sdir = find_dir(cdir, sub)
            for f in images(sdir) if sdir else []:
                other = [o for o in colours if o != c and o in f.upper()]
                if other:
                    warnings.append(f"{c}/{sub}/{f}: file name mentions {other[0]}")

    print()
    for w in warnings:
        print("WARNING:", w)
    for b in blocking:
        print("BLOCKING:", b)
    if not warnings and not blocking:
        print("OK: folder is ready to list")
    sys.exit(1 if blocking else 0)


if __name__ == "__main__":
    main()
