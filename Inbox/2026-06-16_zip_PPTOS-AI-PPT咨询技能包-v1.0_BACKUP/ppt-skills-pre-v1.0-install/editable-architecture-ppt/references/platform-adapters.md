# Platform Adapters

Use the same conceptual workflow across agents. Only the tool names change.

## Universal Steps

1. Read the user's theme, image, PRD, or vault notes.
2. Produce a structured model of the diagram.
3. Generate a preview artifact when the visual is complex.
4. Generate editable PPTX with native objects.
5. Verify output files and record evidence.

## Codex

Recommended:

- Use shell/file tools for repo inspection.
- Use `apply_patch` for skill, script, and document edits.
- Use bundled Node or workspace Node for `PptxGenJS`.
- Use browser tooling for local visual QA when allowed.
- Use PowerShell zip inspection for PPTX package checks on Windows.

Typical verification:

```powershell
Get-Item .\output.pptx
Add-Type -AssemblyName System.IO.Compression.FileSystem
$zip=[System.IO.Compression.ZipFile]::OpenRead((Resolve-Path .\output.pptx))
$zip.GetEntry('ppt/slides/slide1.xml')
$zip.Dispose()
```

## Claude Code

Recommended:

- Put this folder under `~/.claude/skills/editable-architecture-ppt`.
- Use Read/Grep/Glob for context gathering.
- Use Write/Edit for artifacts.
- Use Bash for Node or Python generation.
- Use Playwright or screenshots for visual QA when available.

## opencode / Hermes / Other CLI Agents

Recommended:

- Copy this skill folder into the agent's skill or prompt library directory.
- If the agent does not support skills, paste `SKILL.md` as a system or project instruction.
- Keep `scripts/pptxgenjs-template.js` available as a reusable file.
- Ask the agent to output:
  - preview HTML
  - editable PPTX
  - generation script
  - process report

## Xiaolongxia / Local Agent Wrappers

If the environment supports tool plugins:

- Register this folder as a skill/plugin.
- Expose file read/write, shell execution, and optional browser preview.
- Provide a Node runtime with `pptxgenjs`.

If the environment does not support plugins:

- Add the `SKILL.md` body to the agent's long-term prompt.
- Store the script template in a reusable snippets folder.

## Dependency Fallbacks

Preferred:

- Node.js + `pptxgenjs`

Fallback:

- Python + `python-pptx`

Last resort:

- Generate SVG/HTML and ask the user whether a high-fidelity non-editable PPT image slide is acceptable.

Do not silently fall back to a flattened image when the user requested editable PPT.
