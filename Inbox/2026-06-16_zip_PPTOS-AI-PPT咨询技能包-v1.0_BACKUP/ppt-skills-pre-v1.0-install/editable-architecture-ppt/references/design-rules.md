---
title: Design Rules for Editable Architecture PPTs
type: note
tags:
- AI
- PPT
---
# Design Rules for Editable Architecture PPTs

## One-Page Dense Diagram Rules

- Use 5-9 main sections. Eight stages is ideal for end-to-end process diagrams.
- Keep repeated cards equal size.
- Use one dominant flow direction. Left-to-right is best for lifecycle/process diagrams.
- Add feedback loops only when they communicate a real system behavior.
- Use a bottom implementation layer for "How to Build" or "Operating Model" when the top flow is product-facing.

## Visual Hierarchy

- Title: one clear product/system name plus diagram category.
- Subtitle: short mechanism statement, not a second title.
- Stage cards: numbered, titled, and internally grouped.
- Accent colors: use semantic meaning.
  - Blue: primary structure and flow.
  - Orange: execution/runtime/risk/automation.
  - Green: learning, evaluation, growth, teaching assets.
  - Purple: product/page/configuration assets.

## Editable PPT Rules

- Text must be real text boxes.
- Cards must be PowerPoint shapes.
- Arrows must be PowerPoint lines or arrow shapes.
- Use images only for logos, screenshots, or complex decorative assets.
- If icons are inserted as images, keep text and containers editable.
- Better: draw simple line icons from PPT shapes when feasible.

## Typography

- Prefer system fonts with strong CJK support:
  - Microsoft YaHei on Windows.
  - PingFang SC on macOS.
  - Noto Sans CJK when available.
- Keep body text readable when projected.
- Use `fit/shrink` cautiously; if text shrinks too much, shorten the copy.

## QA Targets

Check:

- No overlapping text.
- No text clipped at box boundaries.
- No arrows crossing important text.
- Similar elements align consistently.
- Footer and bottom principle bars do not crowd the slide edge.
- Icons share stroke weight and visual style.
- The PPT is not mostly pictures if editability is required.
