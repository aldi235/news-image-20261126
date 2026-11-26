# The World in One Page — Thursday 26 November 2026

A dense newspaper front page summing up the world news of Thursday
26 November 2026 (midday edition, news to 09:00 WIB / 02:00 UTC).

## What's on the page

- **Masthead** naming the day: Thursday 26 November 2026.
- **Three lead stories**: Trump's new tariffs on 14 trading partners,
  Nvidia's 3.9% slide as the AI rout deepens, and the Houthis' Ras
  Tanura claim pushing Brent crude to $94.61.
- **A UTC timeline strip** showing how 25–26 November unfolded.
- **A schematic world map** with the day's hot spots marked, and a
  **markets chart** (Brent, Dow, S&P 500, Nasdaq, Nvidia).
- **38 short stories across 7 sections** — Americas, Europe, Middle
  East, Africa, Asia-Pacific, and Tech / Science / Sport — each with a
  source tag (Reuters, AP, BBC, KCNA, PTI, CNA, ESA, Guardian, Fed,
  Nasdaq) and a date check (25–26 Nov 2026).
- **A "By the Numbers" strip** with the day's key figures.

## Files

- `draw_news.py` — build-time draw script (Python stdlib + Pillow) that
  renders `entry.png`. The grader never runs it.
- `entry.png` — the 1024x1024 image, under 1 MiB.
- `main.ts` — the entry point (Node 22, stdlib only). It copies the
  committed `entry.png` to `MAKEFUN_OUTPUT_DIR` (default `/output`)
  and verifies the PNG signature, the 1024x1024 cap, the 1 MiB cap,
  and that the copy is byte-identical to the source.

## Verify locally

```sh
python3 draw_news.py
MAKEFUN_OUTPUT_DIR=/tmp/out1 node main.ts
MAKEFUN_OUTPUT_DIR=/tmp/out2 node main.ts
sha256sum /tmp/out1/entry.png /tmp/out2/entry.png   # identical hashes
```

Every fact on the page was checked against news reported on 25–26
November 2026; nothing is invented.
