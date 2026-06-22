---
title: Theme Tokens
description: Define visual constants before generation.
type: note
---
# Theme Tokens

Define visual constants before generation.

## Required Tokens

```json
{
  "font": {
    "heading": "Microsoft YaHei",
    "body": "Microsoft YaHei"
  },
  "colors": {
    "primary": "0751B8",
    "deep": "071F5C",
    "ink": "10254D",
    "muted": "4A5A78",
    "surface": "F9FCFF",
    "accent1": "F26B16",
    "accent2": "0B8B52",
    "accent3": "6B35C8"
  },
  "layout": {
    "slide_width": 13.333,
    "slide_height": 7.5,
    "margin": 0.35,
    "title_y": 0.22,
    "footer_y": 7.12
  }
}
```

## Rules

- Use semantic colors, not random colors.
- Do not change palette slide-by-slide.
- Use the same title zone unless a divider/cover layout requires otherwise.
- Prefer CJK-safe fonts for Chinese decks.
