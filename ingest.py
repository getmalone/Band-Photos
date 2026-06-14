#!/usr/bin/env python3
"""ingest.py — normalize the band-photo corpus.

Renames every JPEG in photos/ to a stable content-hash photo id
(`band-<sha12>.jpg`), de-duplicates byte-identical photos, and rebuilds
labels.csv keyed by photo id while preserving any ground-truth already filled
in and the original (phone) source filename for traceability.

Idempotent: re-run any time after dropping new photos into photos/.

Usage:  python3 ingest.py
"""
import csv
import hashlib
import os
import sys

ROOT = os.path.dirname(os.path.abspath(__file__))
PHOTOS = os.path.join(ROOT, "photos")
LABELS = os.path.join(ROOT, "labels.csv")
FIELDS = ["photo_id", "source_filename", "sha256",
          "expected_brand", "expected_line", "expected_vitola",
          "expected_slug", "wrapper", "notes"]


def sha256_hex(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def main():
    # 1) Preserve any prior labels (by photo_id) so a re-run never clobbers
    #    hand-entered ground truth.
    prior = {}
    if os.path.exists(LABELS):
        with open(LABELS, newline="") as f:
            for row in csv.DictReader(f):
                prior[row.get("photo_id", "")] = row

    renamed = deduped = unchanged = 0
    records = {}  # photo_id -> record
    for name in sorted(os.listdir(PHOTOS)):
        if not name.lower().endswith((".jpg", ".jpeg")):
            continue
        src = os.path.join(PHOTOS, name)
        if not os.path.isfile(src):
            continue
        full = sha256_hex(src)
        pid = "band-" + full[:12] + ".jpg"
        dst = os.path.join(PHOTOS, pid)

        source_filename = "" if name.startswith("band-") else name
        if name == pid:
            unchanged += 1
        elif os.path.exists(dst):
            os.remove(src)          # byte-identical duplicate
            deduped += 1
            continue
        else:
            os.rename(src, dst)
            renamed += 1

        # carry forward prior ground-truth / source filename if we have it
        p = prior.get(pid, {})
        records[pid] = {
            "photo_id": pid,
            "source_filename": source_filename or p.get("source_filename", ""),
            "sha256": full,
            "expected_brand": p.get("expected_brand", ""),
            "expected_line": p.get("expected_line", ""),
            "expected_vitola": p.get("expected_vitola", ""),
            "expected_slug": p.get("expected_slug", ""),
            "wrapper": p.get("wrapper", ""),
            "notes": p.get("notes", ""),
        }

    with open(LABELS, "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=FIELDS)
        w.writeheader()
        for pid in sorted(records):
            w.writerow(records[pid])

    print(f"renamed={renamed} deduped={deduped} unchanged={unchanged} "
          f"total={len(records)}")


if __name__ == "__main__":
    sys.exit(main())
