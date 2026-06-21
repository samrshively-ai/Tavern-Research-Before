---
name: poll-graphic
description: Use when producing a single-stat poll-result graphic for social. Takes a number, a claim, and source info; outputs a square SVG ready for export.
---

# Poll Result Graphic

Generates a 1080x1080 social card showing one finding from a survey. Use when the user has a poll result to share and wants it in a clean, on-brand graphic.

## Rules

- **One stat per card.** Don't try to fit two numbers. If they ask for a comparison, suggest a bar chart skill instead.
- **The number is the hero.** It should take up the top third of the canvas, at roughly 280-340pt. Everything else supports it.
- **Claim line under the stat.** Max 14 words. If it runs longer, two lines max, never three. Push back if the claim is fuzzy or unsupported.
- **Source line at the bottom.** Pollster name, sample description (e.g., "likely voters, n=812"), date. This is non-negotiable — a card without sourcing is a liability.
- **Palette:** stick to the locked Tavern palette unless explicitly told otherwise. Bg #0E1116, accent #E8B948, text #F4F1EA. White text on the accent color does not have enough contrast for accessibility — don't use it.
- **Don't:** add decorative graphics, candidate photos, or party logos to this card. It's a research product, not an ad.

## Template

```svg
<svg viewBox="0 0 1080 1080" xmlns="http://www.w3.org/2000/svg">
  <rect width="1080" height="1080" fill="#0E1116"/>
  <text x="540" y="420" font-family="Inter, sans-serif" font-weight="800"
        font-size="300" fill="#E8B948" text-anchor="middle">{{STAT}}</text>
  <text x="540" y="600" font-family="Inter, sans-serif" font-weight="500"
        font-size="48" fill="#F4F1EA" text-anchor="middle">{{CLAIM}}</text>
  <text x="540" y="1000" font-family="Inter, sans-serif" font-weight="400"
        font-size="24" fill="#9A9690" text-anchor="middle">{{SOURCE}}</text>
</svg>
```

Inputs: `STAT` (e.g., "62%"), `CLAIM` (short sentence), `SOURCE` (e.g., "Tavern Research / MI likely voters / May 2026").
