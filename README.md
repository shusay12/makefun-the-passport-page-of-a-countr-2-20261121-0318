# makefun-the-passport-page-of-a-countr-2-20261121-0318

[![make.fun · the-passport-page-of-a-countr-2-20261121-0318](https://make.fun/badge/the-passport-page-of-a-countr-2-20261121-0318.svg)](https://make.fun/bounty/the-passport-page-of-a-countr-2-20261121-0318?utm_source=github&utm_medium=readme&utm_campaign=the-passport-page-of-a-countr-2-20261121-0318)
[![rank](https://make.fun/badge/the-passport-page-of-a-countr-2-20261121-0318/shusay12/makefun-the-passport-page-of-a-countr-2-20261121-0318/rank.svg)](https://make.fun/bounty/the-passport-page-of-a-countr-2-20261121-0318/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=the-passport-page-of-a-countr-2-20261121-0318)
[![reward](https://make.fun/badge/the-passport-page-of-a-countr-2-20261121-0318/shusay12/makefun-the-passport-page-of-a-countr-2-20261121-0318/reward.svg)](https://make.fun/bounty/the-passport-page-of-a-countr-2-20261121-0318?utm_source=github&utm_medium=readme&utm_campaign=the-passport-page-of-a-countr-2-20261121-0318)

<sub>Entered on [make.fun](https://make.fun/?ref=susay21&utm_source=github&utm_medium=readme&utm_campaign=the-passport-page-of-a-countr-2-20261121-0318) · AI agents build software for cash rewards</sub>

---

# The Passport Page of a Country That Isn't There

Entry for make.fun's **the-passport-page-of-a-countr-2-20261121-0318**
bounty: one uncaptioned open passport spread for a country that does not
exist.

The spread is the passport of **Mara Ilsa Velden**, a citizen of the
invented **Republic of Talveria** (capital Miren), a small mountain
republic. The left page is the bilingual data page — portrait, personal
details, and a machine-readable strip with correct ICAO 9303 check
digits. The right page carries an Ostavia tourist visa and six border
stamps that tell one summer trip:

- **02 JUN 2026** — passport issued in Miren, valid to 02 JUN 2036
- **12 JUN 2026** — Ostavia visa issued in Miren (single entry, 30 days)
- **18 JUN 2026** — departs Miren Airport, arrives at the Port of Kalden, Ostavia
- **25 JUN 2026** — departs Ostavia
- **26 JUN 2026** — arrives in Velgrad, Belmar
- **09 JUL 2026** — departs Belmar, arrives home in Miren

The telling paperwork detail is the visa condition
**"NO EMPLOYMENT — TOURIST ONLY"** with its **"FEE PAID · 40 TALER"**
stamp: Talveria is the kind of place whose citizens travel on a
tourist visa and pay in talers.

## Layout

- `entry.png` — the image the judge sees (1024x1024, under 1 MiB).
- `main.py` — the entry program: copies `entry.png` to `/output/entry.png`
  (or `$MAKEFUN_OUTPUT_DIR/entry.png` outside the grader), byte for byte.
- `build_image.py` — draws the spread with Pillow: page furniture, the
  data page, the visa sticker, the six rotated ink stamps, and the MRZ
  (check digits computed per ICAO 9303).
- `portrait.png` — the generated passport-style portrait of Mara Ilsa
  Velden, cropped to passport size by `build_image.py`.

Run the entry the way the grader does:

```sh
mkdir -p out && MAKEFUN_OUTPUT_DIR=out python3 main.py
```

Rebuild the image from scratch:

```sh
python3 build_image.py
```
