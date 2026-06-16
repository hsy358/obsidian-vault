---
type: research-report
okf_metadata:
  schema: okf-v0.1-inspired
  added_by: okf-batch-2026-06-16
---

# Harnss — Deep Research Report

**Date:** 2026-06-12
**Subject:** Harnss (https://github.com/OpenSource03/harnss)
**Prepared by:** Subagent Research Task

---

## 1. Project Overview & Current Status

**Harnss** (stylized as "harnss") is an open-source, cross-platform desktop application that serves as a unified UI/shell for running, managing, and switching between AI coding agents. Its tagline is "Harness your AI coding agents."

The project is maintained by **OpenSource03** and licensed under **MIT**. It is built with a strong emphasis on the **Agent Client Protocol (ACP)** as the foundational interoperability layer.

### Current Version
- **Latest stable:** v0.22.0-beta.2 (released April 14, 2026)
- The project is explicitly in **early development** — the README carries a prominent warning that "issues are to be expected"
- Pre-release (beta) channel updates are opt-in, and users can downgrade to stable

### Platform Support
| Platform | Download |
|---|---|
| macOS (Apple Silicon) | .dmg (arm64) |
| macOS (Intel) | .dmg (x64) |
| Windows (x64) | .exe installer |
| Windows (ARM64) | .exe installer |
| Linux | .AppImage / .deb |

> **Note:** Pre-built binaries are unsigned. On macOS, users must right-click → Open to bypass Gatekeeper. On Windows, "Run anyway" is needed for Defender.

---

## 2. Technical Architecture

### Stack
Harnss is built using **Tauri** (Rust backend + web frontend), which gives it native performance with a small binary footprint and cross-platform support. The frontend is likely React-based given the component-level descriptions (virtualized lists, tool cards, etc.).

### Multi-Agent Execution Model

Harnss supports three execution "engines":

| Engine | Protocol | Requirements |
|---|---|---|
| **Claude Code** | Anthropic Agent SDK | Claude account (subscription or API key) |
| **Codex** | JSON-RPC app-server | Codex CLI in PATH + OpenAI API key or ChatGPT account |
| **ACP agents** | Agent Client Protocol | Agent-specific (see registry) |

Each agent runs in its own **session** with:
- Isolated state, history, and context
- Per-session model/effort/permission settings
- Independent tool drawers and scroll state
- The ability to switch between sessions instantly without losing context

**Split View (v0.22.0+):** Up to four chat sessions can be displayed side by side in a split-pane layout. Sessions can be dragged from the sidebar into the chat area or opened via right-click → "Open in Split." Each pane maintains its own engine controls, tool state, and scroll position.

### Virtualized Chat Rendering
As of v0.21.0, the chat uses a proper virtualized list — only the ~20 visible messages are rendered at any time, regardless of conversation length. Previously, a 500-message chat would keep hundreds of React components in memory. This dramatically improved scrolling smoothness, session-switching speed, and memory usage.

### Background Agent Tasks
When a session spawns a task agent (subagent), it continues running in the background tracked in a dedicated panel. Users can:
- See real-time AI-generated progress summaries
- View which tool the agent is currently using and how long it has been running
- Stop running agents at any time via a stop button
- View full transcripts of completed background agents (every tool call, result, and text response) in a detailed modal

### Project/Space Organization
- **Projects** map to folders on disk
- **Spaces** organize projects into named groups with custom icons and colors
- Sessions, history, and panel settings are all scoped per project
- Projects can be dragged and reordered in the sidebar with drop indicators
- Sessions can be organized into folders and pinned; sessions are also grouped by git branch automatically

---

## 3. ACP (Agent Client Protocol) Integration

### What is ACP?
The **Agent Client Protocol** is a standardized protocol for communication between code editors/IDEs and coding agents, analogous to how the **Language Server Protocol (LSP)** standardized language server integration.

Key goals of ACP:
- **Decoupling:** Agents work with any ACP-compatible editor; editors gain access to the entire ACP agent ecosystem
- **Local agents:** Run as subprocesses, communicating via JSON-RPC over stdio
- **Remote agents:** Communicate over HTTP or WebSocket (remote support is still a work in progress per official docs)
- **Protocol reuse:** Reuses MCP JSON representations where possible, but adds custom types for agentic UX elements (diffs, etc.)
- **Markdown-first:** User-readable text defaults to Markdown for rich formatting without requiring HTML rendering

### Harnss + ACP

Harnss is explicitly **built on ACP** and is the reference UI implementation for the protocol. It provides:

1. **Agent Store:** Browse and install agents from the ACP community registry directly in the app (Settings → ACP Agents → Agent Store tab)
2. **Custom Agents:** The "My Agents" tab lets users create custom agents by specifying:
   - Binary command and arguments
   - Environment variables
   - Icon (or paste a JSON definition to auto-fill)
3. **ACP Authentication:** End-to-end auth flow for ACP agents requiring credentials — Harnss detects when a server needs auth, shows a dialog, and completes the handshake automatically (as of v0.22.0-beta.1)
4. **Engine Picker Integration:** The engine picker groups agents by type (Engines vs. ACP Agents) with a "Manage ACPs" shortcut

### ACP-Compatible Agents Known to Work with Harnss

| Agent | Command | Notes |
|---|---|---|
| **Gemini CLI** | `gemini --experimental-acp` | Experimental ACP flag required |
| **Goose** | `goose acp` | Block's open-source agent |
| **Docker cagent** | `cagent acp agent.yml` | Container-based agents |
| Custom agents | Various | Via JSON definition or manual config |

### Connection to Claude Code & Codex
- **Claude Code** connects via the **Anthropic Agent SDK** (not ACP) — this is a built-in, native integration
- **Codex** connects via **JSON-RPC app-server** — also built-in, not ACP
- **All other agents** use ACP as the common protocol

This means Harnss serves as a unifying layer: Claude Code and Codex are supported natively, while the long tail of ACP-compatible agents extends the ecosystem.

---

## 4. MCP Server Integration

MCP (Model Context Protocol) servers are configured **per project** through the **MCP Servers panel** in the right-side toolbar.

### Supported Transports
- **stdio** (local subprocess)
- **SSE** (Server-Sent Events over HTTP)
- **HTTP** (request/response)

### Features
- **OAuth flows** are handled automatically in-app with token persistence across sessions
- **Server status** and **available tool counts** are visible at a glance in the UI
- **Jira, Confluence, and other integrations** render with dedicated UIs rather than raw JSON — these MCP tools get custom UI treatment instead of showing as generic JSON blobs
- Configuration is project-scoped, meaning each project can have its own set of MCP servers

---

## 5. Tool Call Visualization System

This is one of Harnss's **signature features** — the UI transforms raw tool calls into rich, interactive visual cards.

### What Gets Visualized
Every tool call renders as an **interactive card** with:

| Tool Type | Visualization |
|---|---|
| **File edits** | Word-level diffs with syntax highlighting, lines added/removed stats |
| **Bash output** | Inline ANSI-colored terminal output within the card |
| **Subagent tasks** | Nested step-by-step progress tracking |
| **MCP tools** | Custom UIs for Jira, Confluence, etc.; generic tool cards for others |
| **Thinking blocks** | Formatted markdown, collapsible with animated 3-line preview showing depth effect (v0.22.0+) |
| **Mermaid diagrams** | Rendered as actual visual diagrams (flowcharts, sequence diagrams, pie charts, git graphs) adapting to light/dark theme; cached on scroll |
| **Web search (Codex)** | Shows queries used, URLs opened |

### Key UX Details
- Tool cards are **collapsible** but show summary stats (e.g., "N files changed, +X lines, -Y lines") at a glance
- Large diffs use a proper viewer with **collapsible unchanged regions**
- **ANSI colors** in bash output render correctly
- A dedicated **Changes panel** summarizes file changes per turn
- **Diff stats** appear on edit/write cards (lines added/removed)
- **Tool icons** on each card use colored glyphs for quick scanning

---

## 6. Git & Terminal Integration

### Git Integration (Built into the app)
- Stage, unstage, commit, and push without leaving the app
- Browse branches and view commit history
- Manage git **worktrees** — a new bar above the composer shows active worktrees as branch chips; click to switch, or create/remove worktrees inline
- **AI-generated commit messages** available from staged diff
- Sessions are grouped by branch automatically when working across multiple git branches

### Terminal Integration
- **Multi-tab PTY terminal** backed by native shell processes (not a web-based emulation)
- ANSI color codes render properly in bash tool cards
- Terminal stays mounted while you work — doesn't reset when switching contexts
- History no longer replays garbled text after switching spaces (bug fixed in v0.21.3)

### Embedded Browser
- An embedded browser for opening URLs inline and providing additional context to the agent
- Also stays mounted while you work

### Image Attachment & Annotation
- Attach screenshots or images directly in the chat
- Built-in annotation tool: draw, highlight, and mark up images with freehand strokes before sending to the agent

---

## 7. Additional Notable Features

- **Plan Mode:** Work in plan mode to have the agent draft a plan before making any changes. Plan cards are always fully visible (not collapsible) as of v0.22.0-beta.2
- **Permission Levels:** Three modes — Ask First, Accept Edits, Allow All — control agent autonomy; switch modes at any time without interrupting context
- **Voice Input:** Via native macOS dictation or an on-device Whisper model (no API key required)
- **OS Notifications:** Configurable notifications for plan approval requests, permission prompts, agent questions, and session completion; clicking a notification takes you directly to the relevant session
- **Session Search:** Full-text search across session titles and message content
- **Claude Code CLI Import:** Import and resume conversations previously started in the Claude Code CLI
- **Deep Folder Inclusion (@#):** Use `@#foldername` in the composer to include full contents of a folder (not just the tree). Harnss warns if the folder exceeds ~50k tokens
- **/clear Command:** Type `/clear` in the composer for a quick fresh chat
- **Per-Session Settings:** Model, effort level, and permission mode are saved per session and restored when you return

---

## 8. Comparison to Similar Tools

### Positioning
Harnss is a **"harness"** — a desktop UI that wraps multiple agents — rather than an agent itself or an IDE. This places it in a distinct category:

| Category | Tools |
|---|---|
| **AI-first IDEs** | Cursor, Windsurf, Zed (AI edition), Augment Code |
| **Agent CLIs** | Claude Code, Codex CLI, Aider, Gemini CLI, OpenCode |
| **Harnesses / Multi-agent UIs** | Harnss, ForgeCode, Intent (Augment Code) |
| **IDE Extensions** | GitHub Copilot, Cody (Sourcegraph), Cline, Continue |

### Harnss vs. Specific Competitors

#### vs. Claude Code CLI
| Dimension | Harnss | Claude Code CLI |
|---|---|---|
| **Interface** | Full desktop GUI with split panes | Terminal/CLI only |
| **Multi-agent** | Claude Code + Codex + ACP agents simultaneously | Single agent per session |
| **Tool visualization** | Rich interactive cards, diffs, ANSI output | Terminal text output |
| **Sessions** | Persistent, searchable, organizable | Ephemeral unless using `--resume` |
| **Split view** | Up to 4 sessions side by side | Not applicable |
| **MCP support** | Per-project, multiple transports | Via `CLAUDE_MCP_SERVERS` env var |
| **Git UI** | Visual staging, branching, worktrees | CLI git commands |
| **Embedded terminal** | Native PTY tabs | N/A (IS the terminal) |
| **Entry barrier** | Must install app, understand ACP | Just `npm install -g @anthropic/claude-code` |

#### vs. Cursor
| Dimension | Harnss | Cursor |
|---|---|---|
| **Core product** | Agent harness/desktop shell | AI-native IDE |
| **Agent support** | Multiple engines (Claude, Codex, ACP) | Primarily Claude via own integration |
| **Tool visualization** | Rich card-based diffs + ANSI | Inline diffs in chat sidebar |
| **Learning curve** | New paradigm (harness) | Familiar IDE paradigm |
| **Context model** | Session-scoped, per-project MCP | Project-wide, rules-based |
| **Price** | Free (open-source) | $20/month (Pro) |
| **Split sessions** | 4-pane multi-agent | Single agent session |

#### vs. Cody
| Dimension | Harnss | Cody |
|---|---|---|
| **Core product** | Desktop agent harness | IDE extension + Sourcegraph backend |
| **Agent support** | Multi-engine (Claude, Codex, ACP) | Anthropic models via Sourcegraph |
| **Context** | Project files + MCP servers | Full codebase intelligence via Sourcegraph |
| **Architecture** | Local, no backend required | Requires Sourcegraph instance for full power |
| **Git integration** | Visual git tools in-app | Git context via Sourcegraph |

#### vs. Windsurf
| Dimension | Harnss | Windsurf |
|---|---|---|
| **Core product** | Agent harness | AI-first IDE |
| **Agent model** | Multi-engine (pluggable) | Cascade (own agent architecture) |
| **Price** | Free | Free tier + $15-200/mo subscriptions |
| **MCP** | Yes, per-project | Yes, via rules |

#### vs. ForgeCode
| Dimension | Harnss | ForgeCode |
|---|---|---|
| **Focus** | Unified multi-agent UI harness | Multi-agent orchestration benchmark leader |
| **Architecture** | Desktop app (Tauri) | Terminal/benchmark-focused |
| **Agent ecosystem** | ACP + Claude + Codex | Provider-agnostic |
| **Maturity** | Early development | Also early, benchmark-focused |

### Summary Comparison Table

| Feature | Harnss | Claude Code CLI | Cursor | Cody | Windsurf |
|---|---|---|---|---|---|
| **Free** | ✅ | ✅ | ❌ ($20/mo) | ✅ (free tier) | ✅ (free tier) |
| **Open source** | ✅ MIT | ❌ | ❌ | ✅ | ❌ |
| **Multi-agent in one UI** | ✅ (4 panes) | ❌ | ❌ | ❌ | ❌ |
| **Rich tool visualization** | ✅ | ❌ | Partial | ❌ | Partial |
| **ACP support** | ✅ | ❌ | ❌ | ❌ | ❌ |
| **MCP per-project** | ✅ | Manual | ✅ | ✅ | ✅ |
| **Split view sessions** | ✅ | ❌ | ❌ | ❌ | ❌ |
| **Built-in git UI** | ✅ | ❌ | Limited | ❌ | ✅ |
| **Built-in terminal** | ✅ | N/A | ✅ | ❌ | ✅ |
| **Embedded browser** | ✅ | ❌ | ❌ | ❌ | ❌ |
| **Voice input** | ✅ (macOS + Whisper) | ❌ | ❌ | ❌ | ❌ |
| **Production-ready** | ❌ (early dev) | ✅ | ✅ | ✅ | ✅ |

---

## 9. Strengths, Weaknesses & Known Limitations

### Strengths
1. **Unified multi-agent interface** — Running Claude Code, Codex, and ACP agents side by side in split panes is genuinely unique; no other tool offers this
2. **Rich tool visualization** — Word-level diffs, ANSI-colored bash output, Mermaid rendering, and interactive tool cards make agent behavior far more legible than terminal output
3. **ACP ecosystem** — Harnss is the reference implementation for ACP; as the protocol matures, Harnss users will have access to a growing registry of compatible agents
4. **Per-project MCP configuration** — Clean separation of MCP servers per project with OAuth handling
5. **Git workflow integration** — Visual staging, branching, worktrees, and AI commit messages keep the developer in the flow without touching CLI git
6. **Background agent tracking** — Subagent transparency is excellent: live progress, current tool, full transcripts
7. **No lock-in** — Open-source MIT, no account required beyond the underlying agent accounts
8. **Voice input without API keys** — On-device Whisper for macOS is a thoughtful touch

### Weaknesses & Known Limitations
1. **Early development** — The project explicitly warns of expected issues; it would be unwise to use it as a primary driver for production work without a safety net
2. **Unsigned binaries** — Gatekeeper/Defender warnings create friction, especially for non-technical users
3. **No remote agent support yet** — ACP remote agent support is described as "work in progress"
4. **Split view limited to 4 panes** — Maximum of 4 concurrent sessions may be limiting for power users who want to monitor many agents
5. **Tauri app distribution** — No auto-update mechanism mentioned; updating requires manual re-download
6. **Platform-specific features** — Voice dictation and glass tinting rely on macOS-native features; Windows/Linux get different (still functional) equivalents
7. **No mobile/remote access** — This is a desktop-only application; no web interface or remote session capability
8. **Learning curve** — The harness paradigm is new; users accustomed to IDEs or CLIs need to adapt to a different mental model

### Known Bugs (from recent release notes)
- Stopping a session could briefly flash a spurious error message (fixed v0.22.0-beta.2)
- Voice dictation could leave invisible placeholder text in the input bar (fixed v0.22.0-beta.2)
- Terminal replaying garbled text after switching spaces (fixed v0.21.3)
- Multi-hunk edits to a single file incorrectly showing as "N files" (fixed v0.21.3)
- Chat content misalignment after switching sessions (fixed v0.21.1)
- Race condition when switching spaces (fixed v0.21.1)

---

## 10. Production Readiness Assessment

**Current status: NOT production-ready for critical workflows**

Rationale:
- The project is in **early development** with an explicit warning on the README
- The beta channel had releases as recently as April 2026 with "super experimental" labels on some releases
- The changelog shows active bug-fixing across core functionality (session switching, streaming stability, terminal behavior)
- No mention of a security audit, formal testing process, or enterprise support

**When it might become production-ready:**
- A stable (non-beta) release with a clear version number
- Documentation beyond README
- A formal changelog or upgrade guide
- Community evidence of people using it reliably for real work
- Auto-update mechanism

**Workarounds for evaluation:**
- Use it alongside (not instead of) Claude Code CLI
- Don't enable "Allow All" permission mode for untrusted code
- Keep the project directory under version control so Harnss's changes are trackable

---

## 11. Best Use Cases

### Ideal For:
1. **Evaluating multiple agents simultaneously** — Developers comparing Claude Code vs. Codex vs. open-source agents like Goose or Gemini CLI can run them side by side and compare outputs on the same codebase
2. **Power users who want full visibility** — The tool visualization system makes Harnss excellent for learning how agents work, debugging unexpected behavior, or auditing agent actions
3. **Multi-agent workflows** — Using one agent for architecture planning (e.g., Claude Opus) while another handles implementation (e.g., Codex), all in one window
4. **Projects requiring MCP integrations** — Teams using Jira, Confluence, or other MCP-based tools benefit from the per-project configuration and custom UI rendering
5. **Git-heavy workflows** — Developers who prefer visual git tools (staging, branching, worktrees) without leaving the agent session
6. **Open-source enthusiasts** — The MIT license and ACP foundation mean no vendor lock-in and community-driven extension potential

### Less Ideal For:
1. **Teams needing enterprise support** — No SLA, no formal support channel
2. **Non-technical users** — Unsigned binaries, ACP concepts, and early-development instability create too much friction
3. **Minimal-footprint workflows** — If you just want a CLI agent with minimal overhead, Claude Code CLI or Aider are simpler
4. **Remote/headless workflows** — Harnss is desktop-only; for CI/CD integration or remote servers, look elsewhere

---

## 12. Key Technical Implementation Details

### How Claude Code Integration Works
Harnss uses the **Anthropic Agent SDK** to run Claude Code sessions. This is a native integration (not ACP-based), meaning:
- Claude Code sessions have full access to Claude's native tool set
- Harnss intercepts and visualizes tool calls from the SDK
- Model selection (Haiku, Sonnet, Opus, etc.) is per-session and persisted

### How Codex Integration Works
Codex sessions communicate via **JSON-RPC app-server** protocol. As of v0.21.3, Harnss properly forwards:
- Permission policies (approval/sandbox settings) from the first message onward
- Multi-file edits now display all files individually with their own diff viewers

### How ACP Agents Work
ACP agents are spawned as subprocesses with JSON-RPC over stdio (local). On Windows, the spawn uses `shell: true` to handle `.cmd` wrappers like `npx` (fixed in v0.21.4).

### Streaming Architecture
The chat uses a **virtualized list** with overlap-tolerant chunk merging for streaming responses. This handles:
- Cumulative snapshots from upstream
- Overlapping deltas
- Exact replays without duplicating text

Thinking block updates use an append-only model (the old interval-based coalescing was removed in v0.19.1 because it caused duplication under rapid updates).

### Startup Performance Optimizations (v0.20.0)
- Window starts hidden and appears only after ready-to-show (eliminates white flash)
- PostHog analytics is fire-and-forget (non-blocking)
- Model cache revalidation deferred 3 seconds to reduce startup IPC contention
- Session prefetch uses idle callbacks with relaxed timing (5s timeout vs. 1.5s previously)

---

## 13. Relationship to the ACP Ecosystem

Harnss is the most prominent **reference UI implementation** for ACP. The protocol is maintained at agentclientprotocol.com and is explicitly inspired by LSP's success in standardizing language server integration.

**ACP's design philosophy:**
- Editors and agents innovate independently
- One integration effort unlocks the entire ecosystem
- Reuses MCP JSON types where possible; extends with agentic UX types (diffs, etc.)

**Implications for Harnss:**
- As more agents adopt ACP (Gemini CLI, Goose, Docker cagent already work), Harnss users gain them for free
- The ACP registry inside Harnss means agent discovery and installation is native to the app
- The protocol is local-first (subprocess/stdio); remote agent support is the next frontier

---

## 14. Research Sources & References

- https://github.com/OpenSource03/harnss — Main repo, README
- https://github.com/OpenSource03/harnss/releases — 9 releases from v0.19.0 to v0.22.0-beta.2 (March–April 2026)
- https://agentclientprotocol.com/get-started/introduction — ACP official docs
- https://www.sitepoint.com/ai-ides-compared-cursor-claude-code-cody-2026 — AI IDE comparison (2026)
- https://www.youtube.com/watch?v=usDE1z2z_MA — Cursor vs. Claude Code video comparison
- https://thoughts.jock.pl/p/ai-coding-harness-agents-2026 — CLI harness comparison
- https://www.augmentcode.com/tools/best-ai-coding-agent-desktop-apps — Desktop agent apps ranking
- https://www.firecrawl.dev/blog/best-ai-coding-agents — Coding agents comparison
- https://openai.com/index/harness-engineering — OpenAI's harness engineering principles
- https://medium.com/spillwave-solutions/forgecode-dominating-terminal-bench-2-0-harness-engineering-beat-claude-code-codex-gemini-etc-eb5df74a3fa4 — ForgeCode deep dive

---

*Report compiled: 2026-06-12*