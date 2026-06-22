---
name: knowledge-to-deck
description: Use when Obsidian vaults, Markdown folders, PDF/Word/PPT files, research
  notes, WeChat article archives, or mixed knowledge sources must be converted into
  structured context, evidence, claims, and source maps for a consulting deck or editable
  PPT.
title: Knowledge To Deck
type: note
tags:
- AI
- Vault
- 知识管理
---
# Knowledge To Deck

Use this skill before `consulting-deck-os` when the user provides a knowledge base, folder, vault, article archive, or source documents.

The goal is to produce deck-ready context, not slides.

## Outputs

- `source-inventory.md` - files inspected and why they matter.
- `evidence-map.md` - claims, evidence, source paths, confidence.
- `deck-context.md` - synthesized material ready for storyline generation.
- optional `open-questions.md` - gaps or assumptions needing user confirmation.

## Workflow

1. **Inventory sources**
   - List relevant files, dates, titles, and paths.
   - Search by topic terms and synonyms.
   - Prefer local files over web copies when local paths are provided.

2. **Extract claims and evidence**
   - Pull out reusable arguments, frameworks, examples, and tool choices.
   - Keep source paths with every important claim.
   - Separate observed source content from your own inference.

3. **Normalize into deck context**
   - Group findings by theme.
   - Convert long articles into deck-ready bullets.
   - Identify decision rules, workflows, comparison tables, and reusable templates.

4. **Flag gaps**
   - Missing data.
   - Conflicting recommendations.
   - Claims that need verification before client delivery.

5. **Handoff**
   - Pass `deck-context.md` to `consulting-deck-os`.
   - Pass specific dense visual requirements to `editable-architecture-ppt`.

## Obsidian Vault Guidance

For vault paths like `D:\Obsidian\MyVault`:

- Search relevant folders first, not the whole vault blindly.
- Use file names, frontmatter, headings, and backlinks if available.
- Keep Markdown links or absolute paths in source maps.
- Do not move or rewrite the vault unless explicitly asked.

## Quality Rules

- Do not overquote source articles.
- Do not treat article opinions as facts without labeling them.
- Do not lose provenance; consulting decks need traceable claims.
- If the user asks for synthesis, synthesize. If they ask for extraction, preserve more source detail.
