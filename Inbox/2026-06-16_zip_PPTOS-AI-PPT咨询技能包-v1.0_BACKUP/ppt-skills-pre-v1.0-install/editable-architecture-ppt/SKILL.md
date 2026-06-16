---
name: editable-architecture-ppt
description: Use when the user asks to create an editable PowerPoint, architecture diagram, product flow diagram, capability map, one-page strategy infographic, AI platform diagram, course/product system diagram, or to convert a complex visual/process idea into a PPTX that can be edited later.
---

# Editable Architecture PPT

Use this skill to turn a theme, rough requirement, existing image, PRD, Markdown notes, Obsidian vault content, or product idea into a polished, editable PPTX information diagram.

This skill can operate standalone, or as the dense visual page specialist inside `consulting-deck-os`.

The core principle: **do not make the final deliverable a flattened screenshot unless the user explicitly wants a high-fidelity image slide.** Build a structured model first, preview visually, then generate PPTX using native editable objects.

## Output Contract

Produce these files unless the user asks for a different format:

- `*-structure.json` or inline structured model: sections, stages, cards, labels, colors.
- `*-preview.html`: high-fidelity browser preview.
- `*-intermediate.svg` when SVG is the best bridge from visual design to PPT objects.
- `*-editable.pptx`: editable PowerPoint using text boxes, shapes, arrows, and editable layout objects.
- `*-generate-ppt.js` or equivalent script: repeatable generation.
- `*-process.md`: generation process, assumptions, verification evidence, limitations.

If time is limited, prioritize `*-editable.pptx` and `*-process.md`.

## Workflow

1. **Understand the goal**
   - Identify audience: investor, internal architecture review, product proposal, teaching, sales, operations.
   - Identify content type: process flow, platform architecture, capability map, lifecycle, governance model, comparison, roadmap.
   - If an image is provided, extract structure and style from the image.
   - If a repository or vault is provided, inspect relevant docs before inventing content.

2. **Build a structured content model**
   - Extract or design the main message.
   - Define 5-9 top-level sections for dense one-page diagrams.
   - Add subcards, responsibilities, data flows, feedback loops, and implementation layers.
   - Separate business knowledge, AI capabilities, orchestration, runtime execution, assets, publishing, feedback, and governance when relevant.

3. **Choose visual system**
   - Use a restrained enterprise palette: one dominant color, one neutral surface, 1-3 semantic accents.
   - Use consistent icon style. Prefer line icons or shape-built icons.
   - Use stable dimensions. Repeated stage cards must share size and alignment.
   - Avoid decorative blobs, random gradients, and purely atmospheric images.

4. **Create HTML preview first when visual complexity is high**
   - Use HTML/CSS Grid/Flex or SVG to test hierarchy, density, and labels.
   - Keep the preview independent of external CDNs when possible.
   - Use it as the visual source of truth for PPT generation.
   - For geometry-heavy pages, SVG can be used as an intermediate design layer before PPTX reconstruction.

5. **Generate editable PPTX**
   - Use native PowerPoint objects for text, cards, arrows, badges, dividers, and containers.
   - Use images only for true images, logos, or high-fidelity icon assets.
   - Do not flatten the full slide into one image unless explicitly requested.
   - For complex repeated layout, write a script instead of manually creating each object.
   - Image models may generate backgrounds or visual assets, but not final text-heavy pages.
   - Keep titles, labels, numbers, charts, and business text editable in PowerPoint.

6. **Verify before completion**
   - Confirm files exist and sizes are non-trivial.
   - Inspect PPTX package structure.
   - Extract slide text and check key labels.
   - Count shape objects and picture objects.
   - If rendering tools exist, render slides to images and inspect for overlap, truncation, and alignment.
   - Record verification evidence and limitations in the process document.

## Recommended Tooling

Default stack:

- `PptxGenJS` for editable PPTX generation.
- HTML/CSS/SVG for high-fidelity preview.
- PowerShell, Node, or Python for package checks and text extraction.

Alternatives:

- `python-pptx` when Node tooling is unavailable.
- Marp or Slidev for Markdown-first decks, not dense editable one-page architecture diagrams.
- Figma/Canva/Gamma only as ideation references; final editable PPTX should still be generated or reconstructed as objects.

See `references/platform-adapters.md` for Codex, Claude, opencode, Hermes, and other agent environments.
See `references/design-rules.md` for visual rules.
See `scripts/pptxgenjs-template.js` for a reusable starting script.

## Verification Checklist

Before saying the work is complete, check:

- PPTX opens structurally as a zip package.
- `ppt/slides/slide1.xml` or expected slide XML exists.
- Important text labels are extractable from XML.
- The slide is not just one full-page image unless requested.
- Process doc lists input, assumptions, steps, generated files, and verification evidence.
- Any failed visual QA path is documented honestly.

## Common Mistakes

- Starting with a picture-generation model and accepting garbled text.
- Asking an image model to generate business text that should be editable.
- Making a beautiful HTML page but forgetting the user asked for editable PPT.
- Generating a PPT where every element is an image.
- Skipping process documentation, which makes the workflow hard to reuse.
- Letting the diagram become a one-note palette with no semantic accents.
- Treating rendering failures as success. If screenshot QA cannot run, say so and provide structural verification instead.
