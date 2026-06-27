# Labeling the band-photo eval set

**File to edit:** `results/labeling-worksheet-2026-06-27.csv` (350 rows, one per real photo)

## The one rule
Correct the **`expected_slug`** column to a **canonical catalog slug**.

- ✅ Confirm or fix `expected_slug`. It is **prefilled with the scanner's current
  guess**, which is always a real catalog slug — a valid starting point.
- ❌ Do **not** invent slugs. Exact-slug scoring joins against the live catalog,
  so a made-up slug (e.g. `arturo-fuente-god-of-fire-double-robusto` when the
  catalog has a different canonical form) always reads as a miss.
- ❌ Do **not** add/remove rows or edit `photo_id`. One row per real photo; the
  `photo_id` (`band-<12 hex>.jpg`) is the join key to `photos/`.

## How to label a row
1. Open the photo: `photos/<photo_id>`.
2. Compare to `cf_top_slug` (the prefilled guess) and `cf_brand` / `cf_line`.
   - Right cigar? Leave `expected_slug` as-is.
   - Wrong? Replace with the **correct catalog slug**. Find it by brand + line
     + vitola; the scanner's top-5 (in `results/baseline-2026-06-26.json`) lists
     nearby real slugs you can copy.
   - Band genuinely not in the catalog? **Blank** `expected_slug` and say so in a
     note. (Don't force a wrong slug.)

## Where to start
Rows with **`flag = CHECK`** (20 of them): an earlier human read disagreed with
the scanner's brand. The `prior_brand` / `prior_line` / `prior_vitola` /
`prior_notes` columns carry that earlier read as a hint. Review these first —
they're the most likely real corrections.

## Scoring (after labeling) — run from the PalateSage repo
These scripts live in PalateSage on the `app/beta-hardening-2026-06-04` branch:

```
node scripts/scanner/band-photos-labels.mjs \
  --build-expected ~/Projects/Band-Photos/results/labeling-worksheet-2026-06-27.csv \
  --out ~/Projects/Band-Photos/results/expected.json
node scripts/scanner/score-band-photos.mjs \
  --run ~/Projects/Band-Photos/results/baseline-2026-06-26.json \
  --expected ~/Projects/Band-Photos/results/expected.json \
  --scorecard ~/Projects/Band-Photos/results/scorecard-2026-06-27.json
```

Scoring reuses the existing baseline run — **no Cloud Function re-run, no cost.**

## Note on `results/batches.hallucinated-2026-06-27`
Superseded. An earlier automated labeling pass fabricated **206 photos that
don't exist** (their `photo_id`s aren't valid content hashes — they contain
non-hex letters) and invented slugs. Only 51 rows mapped to real photos; those
51 human reads are folded into the 2026-06-27 worksheet as `prior_*` hints. **Do
not use the fabricated file for scoring.**
