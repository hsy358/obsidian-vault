---
name: ppt-quality-review
description: Use when a PPTX, deck, slide image, generated presentation, consulting
  deck, or editable PowerPoint must be reviewed for storyline quality, editability,
  visual layout, text overflow, rendering issues, source coverage, and delivery readiness.
title: PPT Quality Review
type: note
tags:
- AI
- PPT
---
# PPT Quality Review

Use this skill before claiming a deck is ready, before sending it to a client, or after generating/editing PPTX files.

The goal is to catch the problems AI PPT generation usually hides: weak logic, uneditable slides, visual overlap, clipped text, inconsistent style, and unsupported claims.

## Review Layers

1. **Storyline review**
   - Does the deck answer the audience's decision question?
   - Are slide titles conclusion-style?
   - Does each slide have one main message?
   - Is the slide order logical?

2. **Content review**
   - Are claims supported by sources, assumptions, or evidence?
   - Are numbers, names, dates, and technical terms credible?
   - Are there duplicated slides or repeated points?

3. **Editability review**
   - Extract text from PPTX XML.
   - Count native shapes and pictures.
   - Flag slides that are mostly full-page images when editability was required.

4. **Visual review**
   - Check alignment, spacing, margins, hierarchy, and color consistency.
   - Check text clipping, overlap, excessive wrapping, and low contrast.
   - Render slides to images if tools are available.

5. **Delivery review**
   - Confirm output files exist.
   - Confirm process notes state assumptions and limitations.
   - Confirm unresolved issues are visible to the user.

## Required Evidence

Before saying a deck is ready, report at least:

- PPTX path and file size.
- Number of slides.
- Text extraction status.
- Shape/picture ratio or counts.
- Rendering status: passed, failed, or unavailable with reason.
- Remaining risks.

## PowerShell PPTX Checks

```powershell
Add-Type -AssemblyName System.IO.Compression.FileSystem
$zip=[System.IO.Compression.ZipFile]::OpenRead((Resolve-Path .\deck.pptx))
$slides=$zip.Entries | Where-Object { $_.FullName -match '^ppt/slides/slide[0-9]+\.xml$' }
$slides.Count
$zip.Dispose()
```

## Common Findings

- `P1`: Required editability broken because slide is a flattened image.
- `P1`: Key title or chart text is clipped.
- `P2`: Slide title is a topic label, not a takeaway.
- `P2`: Source or assumption missing for major claim.
- `P3`: Minor alignment or spacing inconsistency.
