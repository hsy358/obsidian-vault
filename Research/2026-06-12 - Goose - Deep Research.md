---
type: research-report
okf_metadata:
  schema: okf-v0.1-inspired
  added_by: okf-batch-2026-06-16
---

# Goose — Deep Research Report

**Date:** 2026-06-12  
**Prepared for:** Internal Research  
**Sources:** https://goose-docs.ai/ · https://github.com/aaif-goose/goose · AAIF.io · Linux Foundation press releases · Community discussions

---

## Table of Contents

1. [Project Overview](#1-project-overview)
2. [Technical Architecture](#2-technical-architecture)
3. [All Major Features](#3-all-major-features)
4. [The MCP Ecosystem](#4-the-mcp-ecosystem)
5. [ACP Integration](#5-acp-integration)
6. [Comparison to Similar Tools](#6-comparison-to-similar-tools)
7. [The AAIF Governance Model](#7-the-aaif-governance-model)
8. [Strengths, Weaknesses & Known Limitations](#8-strengths-weaknesses--known-limitations)
9. [Production Readiness](#9-production-readiness)
10. [Best Use Cases](#10-best-use-cases)

---

## 1. Project Overview

### What Is Goose?

Goose is a **general-purpose, open-source AI agent** that runs on the user's local machine. It is not limited to code tasks — it handles research, writing, automation, data analysis, and any workflow the user delegates to it. It was originally developed at **Block** (Jack Dorsey's company, formerly Square) and released as open source in January 2025.

### Current Status (mid-2026)

| Metric | Value |
|---|---|
| GitHub Stars | **~47.8k** (global rank ~#478) |
| Contributors | **500+** |
| MCP Extensions | **70+** |
| License | **Apache 2.0** |
| Repository | `aaif-goose/goose` |
| Language | **Rust** (core), TypeScript/React (Desktop UI) |

Goose completed its **move from `block/goose` to the `aaif-goose` GitHub organization** in April 2026, coinciding with its donation to the **Agentic AI Foundation (AAIF)** at the Linux Foundation. The project is now a **Series of LF Projects, LLC**, with trademark policies managed by the Linux Foundation.

### Founding Timeline

- **Late 2024** — Internal project at Block
- **January 2025** — Public launch as open source (`block/goose`)
- **December 2025** — AAIF announced at Linux Foundation; MCP, goose, and AGENTS.md contributed as founding projects
- **April 2026** — Official move to AAIF; new `goose-docs.ai` domain; repository transferred to `aaif-goose`

---

## 2. Technical Architecture

### Built in Rust

Goose is built in **Rust** for performance, memory safety, and portability. The rewrite with MCP support landed in late January 2025. The Rust core handles:
- Agent orchestration and session management
- Tool execution framework
- Extension system integration
- LLM provider abstraction
- ACP protocol handling

### Three Interfaces

Goose ships in three delivery forms that share the same Rust core and configuration:

#### Desktop App (Electron + React/TypeScript)
- Cross-platform: macOS, Linux, Windows
- Native desktop experience with interactive chat UI
- Extension browser and toggle UI
- Session management, recipe library, scheduler
- MCP Apps render directly inside the Desktop chat window

#### CLI (`goose-cli`)
- Full-featured terminal interface
- `goose run` — single prompt mode for scripting
- `goose session` — interactive terminal session
- `goose configure` — interactive setup wizard
- `goose acp` — ACP server mode for IDE integration
- `goose review` — local code review command
- `goose serve` — HTTP API server mode
- Built-in TUI (`npm start` in `ui/text/`) for terminal-native chat

#### API / Embeddable
- `goose serve` exposes an HTTP API
- ACP over stdio for IDE/client integration (e.g., Zed, VS Code)
- WebSocket support for real-time interaction
- `GOOSE_SERVER__SECRET_KEY` for optional authentication

### Configuration

YAML-based configuration at `~/.config/goose/config.yaml` (macOS/Linux) or `%APPDATA%\Block\goose\config\config.yaml` (Windows). Shares settings across Desktop and CLI. Supports environment variable overrides.

Key config areas:
- Provider and model selection
- Extension enablement and timeout
- Permission mode (`auto`, `approve`, `smart_approve`, `chat`)
- Search paths for extension commands
- Observability (OpenTelemetry / OTLP export)
- Recipe paths and slash command aliases

### Session Model

Sessions are single, continuous conversations. Multiple concurrent sessions are supported, each with isolated state. Sessions can be saved, resumed, and forked. ACP session IDs differ from goose's internal session IDs (limitation noted in ACP provider docs).

---

## 3. All Major Features in Detail

### 3.1 Multi-Provider LLM Support (15+ Providers)

Goose is provider-agnostic. Recommended model family: **Claude 4** (best tool-calling performance). The Berkeley Function-Calling Leaderboard is cited as a guide for model selection.

**Direct API Providers:**
- Anthropic (Claude via `ANTHROPIC_API_KEY`)
- OpenAI (`OPENAI_API_KEY`) — also connects to OpenAI-compatible endpoints (vLLM, LLaMA, KServe, self-hosted)
- Google Gemini (`GOOGLE_API_KEY`)
- Azure OpenAI
- Amazon Bedrock (AWS credentials or bearer token)
- GitHub Copilot (device flow OAuth)
- ChatGPT Codex (browser-based OAuth for Plus/Pro subscribers)
- Groq, Mistral, Cerebras, xAI, Perplexity, Databricks, Snowflake, GCP Vertex AI, VMware Tanzu, and many more

**Gateway/Aggregator Providers:**
- OpenRouter (200+ models, single API key)
- Tetrate Agent Router (automatic failover, $10 free credits for new users)
- LiteLLM proxy
- Routstr
- FuturMix, Novita AI, SaladCloud, Scaleway, oMLX, Vercel AI Gateway, and others

**Local Model Providers:**
- Ollama (localhost:11434, no API key needed)
- LM Studio (localhost:1234)
- Docker Model Runner
- Atomic Chat
- Ramalama (OCI container runtime)
- Ollama Cloud

**ACP Providers (use external CLI subscriptions):**
- **Claude ACP** — Claude Code subscription via `claude-agent-acp` npm package
- **Codex ACP** — ChatGPT/Codex subscription via `codex-acp` npm package
- **Amp ACP** — Amp (Sourcegraph) subscription
- **Pi ACP** — Pi CLI subscription

**Prompt Caching:** Automatically enabled for Claude models via Anthropic, Bedrock, Databricks, OpenRouter, and LiteLLM providers. Reduces costs for long conversations.

### 3.2 Recipes

Recipes are **portable YAML workflow configurations** that capture:
- AI instructions (goal/purpose)
- Suggested activities (clickable prompt bubbles)
- Enabled extensions and their configurations
- Project folder or file context
- Initial prompt (optional — auto-starts the session)
- Model and provider overrides (optional)
- Retry logic with success validation
- Structured JSON output schema for automation
- Subrecipes (nested recipe calls)

**Core Recipe Components:**
- `instructions` — Required if no prompt; defines the agent's mission
- `prompt` — Optional; auto-submits on session start
- `activities` — Example tasks shown as clickable bubbles
- `parameters` — Dynamic values users fill in at launch time
- `extensions` — Which MCP tools are available
- `response.json_schema` — Enforces structured JSON output

**Sharing:**
- Deep links (`goose://` URL scheme)
- `.yaml` file export/import
- Slash commands in any session (`/recipe-name`)

**Scheduling:**
- Recipes can be scheduled via cron expressions
- Execution modes: foreground (opens window) or background (no window, results saved)
- Scheduled runs appear in Scheduler UI with run history

**Automated Retry Logic:**
```yaml
retry:
  max_retries: 3
  checks:
    - type: shell
      command: "test -f output.txt"
      on_failure: "rm -f temp_files*"
```

**Structured Output for Automation:**
Recipes can enforce JSON schema output — useful for CI/CD pipelines, scripts, and data processing. The agent must call `final_output` with valid JSON matching the schema, or correct its output until valid.

### 3.3 Subagents

Subagents are **independent goose instances** spawned to handle tasks in parallel or offload complex work, keeping the main conversation clean. Two types:

#### Internal Subagents
Spawn from the current goose session's context and extensions. Configured via:
- **Direct prompts** — natural language, one-off tasks
- **Recipe files** — structured, reusable configurations

Supports sequential (default) and parallel execution:
```
"Create three HTML templates in parallel"
```

Each subagent has:
- Configurable max turns (default 25, set via `GOOSE_SUBAGENT_MAX_TURNS` or prompt)
- 5-minute default timeout (customizable in prompt)
- Inherited or restricted extensions
- Return mode control: full details or summary only

#### External Subagents
Bring in agents from other providers. Example: Codex as a subagent via MCP server configuration in `config.yaml`:
```yaml
subagent:
  args: ["mcp-server"]
  bundled: true
  cmd: codex
  description: OpenAI Codex CLI Subagent
  enabled: true
  env_keys: ["OPENAI_API_KEY"]
  name: subagent
  timeout: 300
  type: stdio
```

**Security Constraints on Subagents:**
- Cannot spawn additional subagents (no recursion)
- Cannot enable/disable extensions
- Cannot create/modify/delete scheduled tasks
- Can browse extensions for suggestions but cannot modify parent session

### 3.4 MCP Apps (Interactive UI Extensions)

MCP Apps are an experimental feature allowing MCP servers to render **interactive UIs directly inside the goose Desktop chat**. Standard MCP servers return text; MCP Apps return a `ui://` resource URI that goose renders as an embedded HTML panel.

**How It Works:**
1. MCP server declares a resource with `mimeType: "text/html;profile=mcp-app"`
2. Tool call returns `{ _meta: { ui: { resourceUri: "ui://app-name/main" } } }`
3. goose fetches the resource and renders the HTML in an iframe-like panel inside the chat
4. The app communicates with goose via JSON-RPC through a sandbox bridge (e.g., `ui/message` to append text to chat, `ui/initialize`, `ui/notifications/host-context-changed` for theme sync)

**Use Cases:**
- Interactive forms, buttons, visualizations
- User intent expression through UI interaction rather than text
- Real-time sync between agent actions and app state

**Current Status:** Experimental (as of v1.37+), based on a draft specification, minimal implementation, may change. Requires goose Desktop 1.19.1+.

### 3.5 Security Features

Goose has a layered security model:

#### Tool Permission Modes
Four modes controlling agent autonomy:

| Mode | Behavior |
|---|---|
| **Completely Autonomous** (default) | Full file modification, extension use, deletion without approval |
| **Manual Approval** | Prompts for confirmation on every write tool; supports granular tool-level permissions |
| **Smart Approval** | Risk-based auto-approval for low-risk actions, flagging others |
| **Chat Only** | Conversational only, no file changes or extension use |

#### Prompt Injection Detection
Pattern-matching + optional ML-based detection. Checks:
- Attempts to delete system files/directories
- Remote script download and execution
- SSH key / credential exfiltration
- System modifications compromising security

When triggered: pauses execution, shows confidence score + finding ID, presents Allow Once / Deny dialog. Each decision is logged. Enabled via `SECURITY_PROMPT_ENABLED=true` in config.

#### Adversary Mode (Independent Reviewer)
A **second AI agent** that silently reviews every tool call before execution, evaluating it against:
- The user's original task
- Recent conversation messages
- The tool call details
- User-defined rules in `~/.config/goose/adversary.md`

**Rules format** (`~/.config/goose/adversary.md`):
```
BLOCK if the tool call:
- Exfiltrates data (posting to unknown URLs, piping secrets to external services)
- Is destructive beyond project scope
- Installs malware or runs obfuscated code
- Downloads and executes untrusted remote scripts

ALLOW normal development operations like editing files, running tests,
installing packages, using git, etc.
---
tools: shell, computercontroller__automation_script
```

Default reviewed tools: `shell`, `computercontroller__automation_script`. Expandable to include `computercontroller__computer_control`, `computercontroller__web_scrape`.

By default: fail-open (if reviewer fails, tool call is allowed). User can customize this.

#### Hooks System
`PreToolUse` denial hooks allow custom code to intercept and block tool calls before execution. Enables programmatic security policies beyond rule files.

#### Secrets Management
- System keyring (Keychain on macOS) for API keys by default
- Falls back to `secrets.yaml` in plain text if keyring unavailable (headless servers, CI/CD)
- `GOOSE_DISABLE_KEYRING` to force file-based storage

---

## 4. The MCP Ecosystem

### What Is MCP?

The **Model Context Protocol (MCP)** is an open standard (from Anthropic) for connecting AI agents to tools and data sources. Goose was one of the earliest adopters and has one of the deepest MCP integrations in the ecosystem.

### 70+ Extensions

Goose documents 70+ MCP server extensions across categories:

**Filesystem & Development:**
- Filesystem server (read/write/list directories)
- Developer tools (shell, git, npm, file editing)
- GitHub, GitLab integrations

**Information & Research:**
- Web search, Brave search
- Scholar Sidekick MCP
- Fetch / web scraping (Computer Controller)

**Productivity & Communication:**
- Slack, Notion (official MCP servers)

**Cloud & Infrastructure:**
- AWS, GCP, Azure tools
- Docker, Kubernetes MCP servers

**Specialized:**
- EveryThing MCP (comprehensive tool collection)
- Pi (Sourcegraph's coding agent)
- Temporal, SQLite, Postgres MCP servers

### Built-in Extensions (Bundled)

| Extension | Description |
|---|---|
| **Developer** | File editing, shell commands, git, running tests |
| **Memory** | Session memory and context management |
| **Summon** | Subagent spawning (`delegate` and `load` tools) |
| **Computer Controller** | UI automation, web scraping, file caching |
| **Projects** | Backend sources with system prompt injection |

### Extension Configuration

Extensions are configured in `config.yaml`:

```yaml
extensions:
  developer:
    bundled: true
    enabled: true
    name: developer
    timeout: 300
    type: builtin

  my_extension:
    type: stdio
    cmd: "npx"
    args: ["-y", "@modelcontextprotocol/server-everything"]
    enabled: true
    available_tools: []  # empty = all tools available
```

**Tool Filtering:** `available_tools: []` loads all tools; specifying names limits to only those tools, reducing token overhead.

### MCP in ACP Context

When goose runs as an ACP server (e.g., in Zed), MCP servers configured in the ACP client's `context_servers` are automatically available to goose — no additional goose-side configuration needed. goose also automatically enables network access for Codex when HTTP MCP servers are detected.

---

## 5. ACP Integration

### What Is ACP?

The **Agent Client Protocol (ACP)** is a standard for communicating with coding agents. Developed initially by **Zed** and now maintained by the Agent Client Protocol organization.

### Goose as ACP Server

Goose can act as an ACP agent server, allowing IDE clients to connect natively. ACP sessions are saved to goose's session history.

**Setup in Zed (example):**
```json
{
  "agent_servers": {
    "goose": {
      "command": "goose",
      "args": ["acp"],
      "env": {}
    }
  }
}
```

**Clients that support ACP:**
- Zed (original ACP creator)
- JetBrains (via plugin)
- VS Code (via `vscode-goose` extension — reference implementation)
- TUI client (`ui/text/`)

**ACP Server Features:**
- Multiple concurrent sessions with isolated state
- Model and mode switching mid-session
- File operations handled by client (native diffs, unsaved file visibility)
- MCP server passthrough from client context
- Slash commands (built-in, skill, recipe) over ACP
- Session list pagination
- `GOOSE_SERVER__SECRET_KEY` for authentication on the endpoint

**TUI Client:**
Full terminal UI (`npm start` in `ui/text/`) communicating with goose via ACP:
- Real-time streaming responses
- Tool call visualization with expand/collapse
- Inline permission dialogs
- Markdown rendering
- Keyboard navigation
- Message queuing while goose is processing

### Goose as ACP Client (ACP Providers)

Goose can use other ACP agents as providers. Extensions are passed through as MCP servers so the agent can use goose's configured tools.

**Available ACP Providers:**
- **Claude ACP** — Uses Claude Code subscription. Requires `npm install -g @agentclientprotocol/claude-agent-acp` and authenticated `claude` CLI. Known models: `default` (Opus), `sonnet`, `haiku`.
- **Codex ACP** — Uses ChatGPT Plus/Pro or OpenAI API credits via Codex CLI. Requires `npm install -g @zed-industries/codex-acp`. Known models: `gpt-5.2-codex`, `gpt-5.2`, `gpt-5.1-codex-max`, `gpt-5.1-codex-mini`.
- **Amp ACP** — Uses Amp (Sourcegraph) subscription.
- **Pi ACP** — Uses Pi CLI subscription.

**Notable ACP Provider Limitation:** No session fork/resume support yet. ACP session IDs don't correlate with goose internal session IDs for telemetry.

---

## 6. Comparison to Similar Tools

### Positioning

Goose occupies a **broad, open-source, local-first agent** position. It competes at the intersection of:
- General-purpose AI agents (not just coding)
- Open-source extensibility
- Local/private execution
- Multi-provider flexibility

### Comparison Table

| Feature | **Goose** | **OpenHands** | **Claude Code** | **Cursor** | **Aider** | **Devin** |
|---|---|---|---|---|---|---|
| **License** | Apache 2.0 | MIT | Proprietary (Anthropic) | Proprietary | MIT | Proprietary |
| **Stars** | ~47.8k | ~70k+ | N/A (closed) | N/A | ~9k | N/A |
| **Language** | Rust | Python | Proprietary | Proprietary | Python | Proprietary |
| **Desktop UI** | ✅ Electron | ❌ | ❌ | ✅ | ❌ | Web-based |
| **CLI** | ✅ | ✅ | ✅ | Via plugin | ✅ | ❌ |
| **API/Server** | ✅ | ✅ (A2A) | ❌ | ❌ | Partial | ✅ (SaaS) |
| **MCP Support** | 70+ extensions | Yes | Native (MCP) | Native (MCP) | Partial | Limited |
| **ACP Support** | ✅ server + client | ❌ | ❌ | ❌ | ❌ | ❌ |
| **Recipes/YAML** | ✅ | Partial | ❌ | ❌ | ❌ | ❌ |
| **Subagents** | ✅ parallel/sequential | ❌ | ❌ | ❌ | ❌ | ✅ |
| **Local Models** | ✅ Ollama, LM Studio | ✅ | ❌ | ❌ | ✅ | ❌ |
| **Built-in Security** | Adversary mode, prompt injection detection | Basic sandbox | Limited | N/A | Limited | Unknown |
| **Governance** | AAIF/Linux Foundation | All-hands open | Anthropic | Proprietary | Independent | Cognition |
| **Windows Support** | ✅ | ✅ | ✅ | ✅ | ✅ | N/A |

### Key Differentiators for Goose

1. **Most hackable agent** — Open governance, editable prompt templates, editable recipes, open roadmap, customizable subagent system prompts
2. **Best-in-class extensibility** — 70+ MCP extensions, ACP server + client, recipes, subagents, hooks
3. **Local-first focus** — Roadmap explicitly targets built-in inference, open model downloads, peer-to-peer compute (no external runtimes needed)
4. **AAIF/Linux Foundation backing** — Neutral governance, long-term sustainability guarantee, co-governed with MCP and AGENTS.md
5. **Desktop + CLI + API from one codebase** — Single Rust core, three interfaces
6. **Recipes and scheduling** — Unique workflow portability and automation layer other agents lack

### Where Goose Lags

- **Coding benchmark performance** — Proprietary agents (Claude Code, Cursor) outperform on SWE-bench-style tasks
- **IDE integration depth** — Claude Code is native to Anthropic's ecosystem; Cursor has deep IDE embedding
- **Local model optimization** — Currently works best with Claude 4; roadmap for open model optimization is in progress (Feb–Apr 2026 roadmap)
- **Production enterprise features** — No audit logs, compliance certifications, or managed cloud offering yet
- **Mature mobile support** — Desktop-first; TUI client is terminal-only

---

## 7. The AAIF Governance Model

### What Is AAIF?

The **Agentic AI Foundation (AAIF)** is a new open-source foundation under the **Linux Foundation**, announced December 9, 2025 and officially operational by April 2026. It provides vendor-neutral, community-driven governance for agentic AI infrastructure.

**Founding Contributions:**
1. **Anthropic's Model Context Protocol (MCP)** — The open standard for AI-to-tool connections
2. **Block's goose** — The open source AI agent
3. **OpenAI's AGENTS.md** — The open specification for agent instruction files

**Stated Mission:** Advance open-source agentic AI by fostering shared protocols, libraries, and best practices under neutral governance.

### Governance Structure

goose follows a **lightweight technical governance model**:

#### Roles

| Role | Responsibilities |
|---|---|
| **Community** | Issues, PRs, discussions — all contributions valued |
| **Maintainers** | PR review, domain expertise, community health within their component |
| **Core Maintainers** (3–7, odd number preferred) | Overall technical direction, dispute resolution, appointment/removal of Maintainers, strategic decisions |

#### Decision-Making

- Most decisions via **consensus in PRs, GitHub discussions, Discord**
- Core Maintainers can fast-track with clear benefit
- Major architectural changes: 1-week open review + majority Core Maintainer approval + public announcement
- Disputes: majority vote among Core Maintainers; tiebreaker: Bradley Axen (goose creator)
- Removal of Maintainers/Core Maintainers: majority vote, publicly documented

#### Merit-Based Membership

- No employer affiliation requirement
- No term limits (inactivity → emeritus status)
- Nomination by existing Maintainers/Core Maintainers based on sustained high-quality contributions + constructive participation

#### Key Governance Values

1. **Open** — Plans and build in the open; roadmap, recipes, extensions, and prompts are editable and shareable
2. **Flexible** — Open and proprietary models equally supported
3. **Choice** — No lock-in to any model, protocol, or stack

### What AAIF Membership Means for Long-Term Sustainability

- **Neutral home** — No single vendor controls goose, MCP, or AGENTS.md
- **Linux Foundation backing** — Legal structure, trademark policies, trademark enforcement via `lfprojects.org/policies/`
- **Predictable funding** — Foundation model with corporate members (Anthropic, Block, OpenAI are founding members)
- **No copyright assignment required** — Contributors retain their copyright; Apache 2.0 license applies
- **Transparent process** — Meeting notes, key decisions, roadmap published on GitHub
- **Appeals process** — Any governance dispute can be escalated and appealed

---

## 8. Strengths, Weaknesses & Known Limitations

### Strengths

✅ **Truly open source** — Apache 2.0, no vendor lock-in  
✅ **Exceptional extensibility** — MCP, ACP, recipes, subagents, hooks, prompt templates  
✅ **Multi-interface** — Desktop app, CLI, API, TUI from one codebase  
✅ **70+ MCP extensions** — Deep MCP ecosystem integration  
✅ **Local-first** — Works with Ollama, LM Studio, Ramalama; roadmap for zero-external-runtime inference  
✅ **Security-conscious design** — Adversary mode, prompt injection detection, permission modes, secrets keyring  
✅ **AAIF/Linux Foundation governance** — Long-term neutral stewardship  
✅ **Recipe portability** — Share workflows as YAML, schedule them, use slash commands  
✅ **Subagent parallelism** — True multi-agent execution with isolation  
✅ **ACP dual role** — Acts as both server (for Zed/VS Code) and client (for Claude Code, Codex)  
✅ **Highly customizable** — Prompt templates, subagent system prompts, adversary rules, slash commands  
✅ **Active development** — Weekly releases, 500+ contributors, roadmap-driven  
✅ **Good onboarding** — Quickstart in 5 minutes, Tetrate free credits, OAuth providers  

### Weaknesses & Known Limitations

❌ **Performance on hard coding tasks** — SWE-bench benchmarks lag behind Claude Code and Cursor; best suited for general automation rather than competitive coding performance  
❌ **Local model experience** — Currently works best with Claude 4; smaller open models need prompt/tuning investment (roadmap item for Feb–Apr 2026)  
❌ **ACP provider gaps** — No session fork/resume for ACP providers; session IDs don't correlate between goose and ACP agent  
❌ **MCP Apps experimental** — Interactive UIs are draft-spec, minimal, may change  
❌ **No enterprise audit/compliance** — No SOC 2, HIPAA, or similar compliance certifications  
❌ **Desktop-first UX** — Some features (MCP Apps, desktop extension toggle) require Electron app; TUI is terminal-only  
❌ **Keyring fallback** — Headless servers fall back to plain-text `secrets.yaml` without explicit opt-in  
❌ **Goose-lang/goose archived** — The old `goose-lang/goose` repository (TypeScript version) was archived in April 2026; current development is Rust-based  
❌ **Rust rewrite relative immaturity** — The Rust rewrite with MCP landed January 2025; some rough edges remain (documentation gaps noted in community reviews)  
❌ **Limited mobile support** — No native mobile app; not a first-class mobile experience  

### Open Issues & Community Pain Points

From community discussions and the Feb–Apr 2026 roadmap:

1. **Setup and documentation shortcomings** — Community feedback (e.g., $10 budget test on Medium) noted documentation gaps and setup friction
2. **Local model optimization** — Needed before local inference is a first-class experience
3. **Built-in inference** — Roadmap item to eliminate external runtimes entirely
4. **Multi-agent task tracking** — Roadmap item for clear progress/debugging UI for multi-agent workflows
5. **Protocol clarity** — Current `goosed` protocol is ad-hoc; needs stable ACP-based replacement

---

## 9. Production Readiness

### Is Goose Production-Ready?

**For personal use and developer workflows: YES**  
**For enterprise mission-critical deployments: PARTIALLY** (with caveats)

#### What Works Well in Production

- ✅ **CLI automation** — Scriptable, schedulable recipes with structured JSON output for CI/CD
- ✅ **MCP extension ecosystem** — Stable for major extensions (filesystem, developer, GitHub)
- ✅ **Desktop app** — Stable for day-to-day use on macOS, Linux, Windows
- ✅ **ACP server in Zed/VS Code** — Production-ready IDE integration
- ✅ **Permission modes** — Fine-grained control over agent autonomy
- ✅ **Session persistence** — Resumable sessions, session history
- ✅ **OpenTelemetry observability** — OTLP export for monitoring
- ✅ **No vendor lock-in** — Apache 2.0, no proprietary dependencies

#### What Needs Enterprise Hardening

- ⚠️ **No managed/cloud offering** — Self-hosted only; no SaaS option for teams
- ⚠️ **No role-based access control** — All users have same permissions; no team-level policies
- ⚠️ **No audit trail UI** — Logs exist but no polished compliance dashboard
- ⚠️ **No SSO/SAML** — Authentication is per-user API key only
- ⚠️ **ACP session correlation** — Telemetry gaps when using ACP providers
- ⚠️ **Subagent failure handling** — Failed parallel subagents return no output (only successful ones); silent failures possible

#### Recommendation

Goose is production-ready for **individual developers, small teams, and automation pipelines**. For enterprise deployments requiring compliance, SSO, and audit trails, evaluate alongside OpenHands (more mature for enterprise) or wait for goose's enterprise features (not yet on the public roadmap as of June 2026).

---

## 10. Best Use Cases

### 🏆 Ideal Use Cases

1. **Personal coding assistant** — Code editing, debugging, code review via subagents, testing
2. **Workflow automation** — Scheduled recipes for repetitive tasks (daily standups, CI reporting, data processing)
3. **Research and summarization** — Spawn research subagents, compile findings
4. **File processing pipelines** — Parallel subagents processing multiple files simultaneously
5. **IDE integration** — Use goose in Zed or VS Code as the agent backend
6. **Multi-provider experiments** — Compare model outputs across Claude, GPT, Gemini, Ollama on the same task
7. **Local/private workflows** — Ollama/LM Studio for fully offline execution with local models
8. **Team workflow sharing** — Export recipes as YAML, share via GitHub recipe repo (`GOOSE_RECIPE_GITHUB_REPO`)
9. **Learning agentic AI** — Most hackable agent; edit prompts, subagent system templates, adversary rules
10. **Integration testing** — MCP Apps for building interactive UIs powered by agents

### 📊 Use Cases Where Alternatives May Be Better

| Use Case | Better Alternative |
|---|---|
| Competitive coding benchmarks | Claude Code, Cursor |
| Enterprise compliance/SOX/HIPAA | Cognite, Palantir AIP, or internal build |
| Deep VS Code IDE embedding | Cline (VS Code native), Cursor |
| Git-native workflows | Aider (git-native diff editing) |
| Fully managed SaaS agent | Devin, Augment |
| Simple chat-only use | ChatGPT, Claude.ai |

---

## Appendix: Key Links

- **Docs:** https://goose-docs.ai/
- **GitHub:** https://github.com/aaif-goose/goose
- **AAIF:** https://aaif.io/
- **Discord:** https://discord.gg/goose-oss
- **YouTube:** https://www.youtube.com/@goose-oss
- **Roadmap (Feb–Apr 2026):** GitHub Discussion #6973
- **Governance:** https://github.com/aaif-goose/goose/blob/main/GOVERNANCE.md
- **ACP Registry:** https://github.com/agentclientprotocol/registry
- **MCP Docs:** https://modelcontextprotocol.io/

---

*Report compiled from public documentation, GitHub repository, AAIF/Linux Foundation announcements, and community discussions. Data current as of 2026-06-12.*
