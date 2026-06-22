---
name: ppt-production-engine
description: Use when slides.json, deck specs, page plans, or structured slide content
  must be compiled into an editable PPTX with native PowerPoint objects, reusable
  layouts, theme tokens, charts, speaker notes, and generation scripts.
title: PPT Production Engine
type: note
tags:
- PPT
---
# PPT Production Engine

Use this skill after `consulting-deck-os` has produced a slide plan, or whenever structured slide data must become an editable PowerPoint deck.

This skill is a compiler, not a strategist. Do not rewrite the storyline unless the slide spec is impossible to render.

## Inputs

Preferred:

- `slides.json`
- theme or brand tokens
- optional image assets
- optional template PPTX

Acceptable:

- Markdown page plan
- table of slide titles and bullets
- existing PPT to update

## Outputs

- `*-editable.pptx`
- `*-generate-deck.js` or equivalent script
- optional `*-preview.html`
- `*-production-notes.md` with assumptions and verification

## Workflow

1. **Validate slide spec**
   - Check deck title, audience, objective, and slide list.
   - Confirm every slide has a type, title, message, content, and visual plan.
   - Reject vague page specs such as "make this pretty" without content.

2. **Select layouts**
   - Map each slide type to a layout pattern.
   - Use consistent margins, title zones, footer zones, and visual grids.
   - Use dense diagram layouts only when content requires them.

3. **Generate PPTX**
   - Use native text boxes for all text.
   - Use native shapes for cards, connectors, arrows, badges, and charts where feasible.
   - Use images for background visuals, logos, screenshots, or generated concept art only.
   - Keep speaker notes when provided.

4. **Preserve editability**
   - Do not flatten slides into images.
   - Do not place important text inside images.
   - Avoid one giant SVG when the user needs to edit individual text blocks.

5. **Verify**
   - Check package structure.
   - Extract text from slide XML.
   - Count shapes and pictures.
   - Render screenshots if local tools allow it.

## Tooling

Preferred:

- `PptxGenJS` for scripted editable PPTX generation.

Fallbacks:

- `python-pptx`
- Office MCP / OfficeCLI when available

See `references/layout-library.md` and `references/theme-tokens.md`.
See `scripts/generate-deck-template.js` for a starter compiler.
