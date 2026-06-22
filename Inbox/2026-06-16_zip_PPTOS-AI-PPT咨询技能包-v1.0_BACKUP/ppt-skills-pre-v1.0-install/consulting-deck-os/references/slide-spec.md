---
title: Slide Spec Reference
description: Use slides.json to make deck generation repeatable.
type: note
tags:
- AI
- PPT
---
# Slide Spec Reference

Use `slides.json` to make deck generation repeatable.

## Minimal Schema

```json
{
  "deck_title": "AI Native Education Platform Strategy",
  "audience": "executives / investors / client team",
  "objective": "decision the deck should support",
  "style": {
    "tone": "consulting / executive / technical / product",
    "palette": "enterprise blue",
    "editability": "native-pptx"
  },
  "slides": [
    {
      "slide_no": 1,
      "type": "cover",
      "title": "Conclusion-style title",
      "message": "One sentence key point",
      "content": ["short point 1", "short point 2"],
      "visual": {
        "kind": "hero / matrix / flow / architecture / chart / roadmap",
        "description": "what the page should show",
        "asset_prompt": "optional image prompt; avoid embedded text"
      },
      "notes": "speaker notes or delivery intent"
    }
  ]
}
```

## Common Slide Types

- `cover` - title, client/context, date.
- `executive_summary` - 3-5 conclusions.
- `issue_tree` - problem decomposition.
- `current_state` - diagnosis and evidence.
- `opportunity` - market or business opening.
- `solution_overview` - recommended answer.
- `architecture` - system or operating model.
- `capability_map` - grouped capabilities.
- `process_flow` - lifecycle or workflow.
- `comparison` - options, tradeoffs, vendor/product comparison.
- `roadmap` - phases, milestones, dependencies.
- `business_case` - value, cost, benefit.
- `risk_governance` - risks, controls, owners.
- `next_steps` - actions, owners, dates.
- `appendix` - supporting evidence.

## Title Rule

Bad: `Market Trends`

Good: `AI-native workflows are shifting budget from tools to operating systems`

Each title should answer: "What should the audience believe after seeing this slide?"
