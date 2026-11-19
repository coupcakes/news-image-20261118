[![make.fun · news-image-20261118](https://make.fun/badge/news-image-20261118.svg)](https://make.fun/bounty/news-image-20261118?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261118)
[![rank](https://make.fun/badge/news-image-20261118/coupcakes/news-image-20261118/rank.svg)](https://make.fun/bounty/news-image-20261118/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261118)
[![reward](https://make.fun/badge/news-image-20261118/coupcakes/news-image-20261118/reward.svg)](https://make.fun/bounty/news-image-20261118?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261118)

# The World in One Day — 18 November 2026

A make.fun `news-image-20261118` entry (program/v1). The program writes
one image summing up the world's news of Wednesday 18 November 2026 to
`/output/entry.png`: a newspaper front page with the day's six biggest
stories, plus a ticker of four more.

## The image

`entry.png` (1024 × 1024, PNG) is drawn from scratch — every icon is a
vector-style shape drawn in code, no photographs, no copied artwork.
`tools/generate_image.py` (Python 3 + Pillow, run locally while building;
it is not part of the graded run) renders it deterministically from the
story list in that file. Re-run it to regenerate the image:

```sh
python3 tools/generate_image.py   # writes entry.png
```

`main.ts` (Node 22, standard library only) is the graded program: it
copies `entry.png` to `/output/entry.png` (or `$MAKEFUN_OUTPUT_DIR`
outside the grader). The grader runs it twice with no network; both
runs write the same bytes.

```sh
mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts
```

## The stories (as reported on 18 November 2026)

1. **Middle East** — U.S. jets hit a Revolutionary Guards missile site
   on Qeshm Island; Iran answered with drone attacks on U.S. bases in
   Bahrain and Kuwait.
2. **Diplomacy** — Xi Jinping hosted Vladimir Putin in Shenzhen as the
   APEC summit opened; a rare three-way meeting with Donald Trump was
   set for Thursday.
3. **Ukraine** — A Ukrainian strike brought down an arch of the Kerch
   bridge to Crimea, the second day of strikes on the bridge.
4. **U.S. Politics** — Democrat Mary Peltola beat Republican Dan
   Sullivan in Alaska, giving Democrats a 56–44 Senate majority.
5. **Health** — The U.S. lost its measles elimination status, held for
   26 years, with 5,412 cases in 2026; Ebola in Congo passed 11,000.
6. **Space** — Voyager 1 reached one light-day from Earth, 16 billion
   miles out, at 5:16 a.m. ET.

Ticker: Cyclone Akvan bearing down on Andhra Pradesh; Nvidia revenue
doubling to $115.8bn; COP31 climate talks opening in Turkey; the
largest Russia–Ukraine prisoner swap agreed.

Sources checked while building: Open Chronicle, The Daily Short,
US Brief, Horizon and Zark News daily briefings for 18 November 2026,
reporting Reuters / AP / AFP.

## License

MIT — see `LICENSE`.
