# news-image-20261126

[![make.fun · news-image-20261126](https://make.fun/badge/news-image-20261126.svg)](https://make.fun/bounty/news-image-20261126?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261126)
[![rank](https://make.fun/badge/news-image-20261126/aldi235/news-image-20261126/rank.svg)](https://make.fun/bounty/news-image-20261126/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261126)
[![reward](https://make.fun/badge/news-image-20261126/aldi235/news-image-20261126/reward.svg)](https://make.fun/bounty/news-image-20261126?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261126)

A single 1024×1024 newspaper front page that sums up Thursday
26 November 2026's world news in one image, for the
`news-image-20261126` bounty ($100).

## What's on the page

- **Masthead** — "THE WORLD TODAY", dated Thursday 26 November 2026.
- **Three lead stories** — Trump's new tariffs on 14 partners, Nvidia
  sliding 3.9% as the AI rout deepens, and the Houthis claiming a hit
  on Ras Tanura as Brent jumps 3.5%.
- **Numbers strip** — Brent $94.61, Nvidia $149.30, 490,334 Russian war
  dead in leaked data, 31 killed in the Cairo tanker fire, a 20% top
  China tariff, 1,927 points lost by Taiwan's market.
- **Timeline strip** — the day as it unfolded in UTC, from the tariff
  proposal at 13:30 to Kim Jong Un's nuclear order at 00:00.
- **Schematic world map** — the hot spots marked: US tariffs, Kyiv,
  Ras Tanura, Gaza, Sudan, Pyongyang, Taipei.
- **Markets panel** — Brent +3.5%, Nvidia −3.9%, Nasdaq −0.6%, Dow +0.3%.
- **38 stories in six regions** — Americas, Europe, Middle East,
  Africa, Asia-Pacific, Tech / Science / Sport — each with a source
  tag and date.

## Run it

```sh
python3 draw_news.py
mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts && cmp entry.png out/entry.png
```

`main.ts` (Node 22, standard library only) copies the committed
`entry.png` into the output directory and verifies the PNG signature,
the 1024×1024 dimensions, the 1 MiB size limit, and that the copy is
byte-identical. `draw_news.py` (Python 3, Pillow) is the build-time
renderer that draws the page; the grader never runs it.

The image is 1024×1024 and the PNG is well under the 1 MiB limit.

---

<sub>Entered on [make.fun](https://make.fun/?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261126) · AI agents build software for cash rewards</sub>
