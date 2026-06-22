---
name: consulting-deck-os
description: Use when the user wants a consulting-style PPT, strategy deck, client
  proposal, executive briefing, business case, product plan, roadmap, or any presentation
  that needs strong storyline, page planning, editability, and repeatable delivery.
title: Consulting Deck OS
type: note
tags:
- AI
- Vault
---
# Consulting Deck OS

Use this skill to turn a topic, notes, vault, report, or brief into a consulting-grade deck workflow.

The focus is not only slide generation. It is **storyline first, page spec second, rendering third, QA last**.

## Output Contract

Prefer these artifacts:

- `deck-brief.md` - audience, objective, constraints, tone, delivery format.
- `storyline.md` - key message, logic chain, evidence points, recommendations.
- `slides.json` - slide-by-slide spec.
- `preview.html` - optional visual preview for dense or high-stakes pages.
- `editable.pptx` - final editable PowerPoint.
- `process.md` - decisions, assumptions, validation, limitations.

If the task is only a single complex figure, delegate to `editable-architecture-ppt`.

## Workflow

1. **Classify the deck**
   - Decide whether this is strategy, proposal, executive update, product story, business case, training, or architecture.
   - Decide whether it is an **outbound deck** (fast, polished) or a **refinement deck** (iterative, editable, heavily reviewed).

2. **Write the storyline**
   - Start with the decision the deck should support.
   - Use one main line of argument.
   - Break the story into 3-5 sections.
   - Make slide titles communicate conclusions, not topics.

3. **Build the page plan**
   - Assign a job to each slide: opener, diagnosis, framework, evidence, recommendation, roadmap, risk, appendix.
   - Keep dense information in diagrams or matrices, not bullet overload.
   - Use `editable-architecture-ppt` for single-page system diagrams, lifecycle flows, capability maps, and high-density visual pages.

4. **Choose the rendering route**
   - Consulting proposal with many editable pages: build a structured slide spec and generate native PPTX.
   - One-page system visual: use the architecture skill path.
   - Visual-heavy public-facing deck: generate a preview and use image assets only where they improve clarity.

5. **Generate and review**
   - Make the deck editable by default.
   - Verify the PPTX package, text extraction, and whether the deck reads as a consulting story rather than a pile of slides.
   - Record assumptions, unresolved points, and source coverage.

## Working Rules

- Prefer conclusion titles over section labels.
- Limit each slide to one primary message.
- Separate logic, evidence, and visuals.
- Default to editability unless the user explicitly asks for a pictorial deck.
- Do not confuse a good visual with a good deck. The storyline is the product.

## Delegation

- For dense one-page system visuals, use `editable-architecture-ppt`.
- For file-format ingestion, use document parsing skills or vault notes as sources.
- For final PPT object generation, use the local generation engine or `PptxGenJS`-based scripts.

## Common Failure Modes

- Starting with slide aesthetics before the argument is clear.
- Making every slide a diagram.
- Producing a beautiful but uneditable deck.
- Writing topic titles instead of takeaway titles.
- Skipping the review of slide order and logic flow.
