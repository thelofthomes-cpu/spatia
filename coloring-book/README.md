# Cozy Little World: 24 Cute & Easy Coloring Pages

An original kawaii coloring book for adults and teens, ready for Amazon KDP and Etsy.

## Deliverables (`output/`)

| File | Use |
|---|---|
| `CozyLittleWorld_KDP_Interior_8.5x11.pdf` | KDP paperback interior: 56 pages, 8.5 x 11 in, no bleed, every illustration on a right-hand page with a blank back |
| `CozyLittleWorld_KDP_Cover_Wraparound.pdf` | KDP full cover: 17.376 x 11.25 in (0.125 in bleed, 0.1261 in spine) |
| `CozyLittleWorld_Front_Cover.png` / `.pdf` | Front cover for listings, mockups and Etsy thumbnail |
| `CozyLittleWorld_Printable_US-Letter.pdf` | Etsy digital download: title, color test, 24 pages and thank-you, no blank backs |
| `previews/` | 300 dpi-wide PNGs of every page, plus `all-24-pages.png` and `cover-wraparound.png` |

Brand: the **Diamond Spade** logo (faceted gold spade with a serif wordmark) is in `brand/diamond-spade/` as SVG, PNG and PDF in stacked, horizontal and icon-only versions, including on-navy, black and white variants. Regenerate it with `python3 brand/logo.py`. Fonts: Baloo 2 and Cormorant Garamond (both SIL OFL).

Marketing copy (title/subtitle, KDP description, 7 keywords, Etsy listing, 10 social posts) is in [`MARKETING.md`](MARKETING.md).

## Pages

1. Morning Latte · 2. Fresh From the Bakery · 3. The Bookshop Nook · 4. Rainy Day Cocoa · 5. Picnic in the Park · 6. Campfire Marshmallows · 7. Little Garden Helper · 8. Sweet Dreams · 9. Cupcake Day · 10. Strawberry Patch · 11. Puddle Splash · 12. Garden Tea Party · 13. Pancake Sunday · 14. Cozy Knitting Corner · 15. The Little Flower Shop · 16. Stargazing · 17. Soup Simmering · 18. Plant Parent · 19. Mushroom Cottage · 20. Lemonade Stand · 21. Birthday Surprise · 22. Pumpkin Patch · 23. Blanket Fort Sleepover · 24. Goodnight, Cozy World

## How it's made

Everything is vector line art drawn with code, so lines are crisp at any print size and every character is original:

- `src/ink.py` is a tiny SVG engine. It uses white-filled shapes with constant-width bold outlines, so foreground shapes cleanly hide what's behind them.
- `src/critters.py` holds the cast: 18 chibi animals with expressions, poses and outfits.
- `src/props.py` holds about 80 cozy props (food, plants, furniture, weather and more).
- `src/scenes.py` holds the 24 scene compositions.
- `src/cover.py` builds the full-color cover and wraparound.
- `src/build.py` renders and assembles all the PDFs and previews.

Rebuild:

```bash
pip install cairosvg pypdf pillow fonttools
mkdir -p ~/.fonts && cp fonts/Baloo2.ttf ~/.fonts/ && fc-cache -f   # Baloo 2 (SIL OFL)
cd src && python3 build.py
```

Author and copyright holder: Diamond Spade (set in `src/build.py`).
