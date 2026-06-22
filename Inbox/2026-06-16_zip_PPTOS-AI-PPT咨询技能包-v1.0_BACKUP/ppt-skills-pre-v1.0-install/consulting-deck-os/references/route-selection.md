---
title: Route Selection
description: Choose the production route before generating slides.
type: note
tags:
- PPT
---
# Route Selection

Choose the production route before generating slides.

## Route A: Consulting Native PPTX

Use when:

- The deck will be edited by clients, leaders, or teams.
- The user asks for consulting, strategy, proposal, business case, roadmap, or executive briefing.
- Accuracy, wording, and structure matter more than instant visual impact.

Artifacts:

- `deck-brief.md`
- `storyline.md`
- `slides.json`
- `editable.pptx`
- `process.md`

## Route B: Dense One-Page Architecture Diagram

Use when:

- The task is a complex flowchart, platform architecture, capability map, operating model, or lifecycle diagram.
- The page has many modules and needs precise alignment.

Delegate to `editable-architecture-ppt`.

Artifacts:

- `structure.json`
- `preview.html`
- `editable.pptx`
- generation script
- process report

## Route C: Visual-First Deck

Use when:

- The goal is public speaking, media sharing, launch visuals, or strong mood.
- The user values visual impact more than deep editability.

Rules:

- Image models may create backgrounds, hero images, or concept art.
- Keep titles, body text, charts, and data as editable PPT objects.
- Avoid image-generated text.

## Route D: Fast Draft / Outbound Draft

Use when:

- The user needs an initial draft quickly.
- The deck is for internal alignment or early discussion.

Rules:

- Generate outline and slides quickly.
- Mark it as a draft.
- Do not over-invest in pixel-level design before storyline approval.

## Decision Rule

If the deck is for consulting delivery, customer proposal, board/executive review, fundraising, or product strategy, default to Route A.

If the most important slide is a high-density system picture, combine Route A with Route B.
