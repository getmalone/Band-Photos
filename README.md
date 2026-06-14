# Band-Photos

Real-world cigar **band photos** captured for testing AuHoya / PalateSage scan
identification. These are the held-out evaluation set for the scan pipeline's
**visual band-matching** path (pHash + HSV + CLIP) — the strategies that rescue
an identification when text/OCR/barcode matching fails.

## Contents

- `photos/` — phone photos of cigar bands (Pixel `PXL_*.jpg`, incl. `.MP.jpg`
  motion photos). Captured at shop visits starting 2026-04. Unlabeled by
  filename (timestamps only).
- `labels.csv` — ground-truth template, one row per photo. Fill
  `expected_slug` (and brand/line/vitola/wrapper) to score the scan harness.
  Until labeled, the set is still useful for **no-match / variance** checks and
  qualitative review; accuracy scoring needs the labels.

## How these are used

Run the set through the deployed `identifyCigar` Cloud Function:

```
# from the PalateSage repo
node scripts/scanner/run-photos-against-cf.mjs \
  --photos ~/Projects/Band-Photos/photos \
  --expected ~/Projects/Band-Photos/labels.csv
```

This produces per-photo top-match + confidence + the vision brand/line trace,
and (with labels) auto-match / no-match rates. It is the before/after gate for
band-matching changes — e.g. enabling the CLIP visual-first rescue.

## Notes

- **Not user data.** These are first-party test captures, safe to store here.
  Real end-user scan photos live in Firebase Storage and must NOT be committed
  to this repo (privacy).
- Photos may be added over time. If the set grows into the multi-GB range,
  migrate binaries to Git LFS to keep clones fast.
