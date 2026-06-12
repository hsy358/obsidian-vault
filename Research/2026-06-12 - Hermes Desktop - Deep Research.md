# Hermes Desktop — Deep Research Report
**Date:** 2026-06-12
**Subject:** Hermes Desktop (https://github.com/fathah/hermes-desktop)
**Current Version:** v0.6.0 (released 2026-06-10)
**Upstream:** NousResearch/hermes-agent

---

## 1. Project Overview

### What is Hermes Desktop?

Hermes Desktop is a native cross-platform desktop application (macOS, Windows, Linux) that serves as the official GUI front-end for **Hermes Agent** — a self-improving AI agent built by [Nous Research](https://nousresearch.com). It is maintained in the `fathah/hermes-desktop` GitHub repository, not by Nous Research directly.

The desktop app wraps the Hermes Agent CLI/gateway with a full React-based UI, providing chat, session management, skill browsing, model configuration, tool management, cron scheduling, messaging gateway controls, and the "Hermes Office" (Claw3d) visual 3D interface. It is another surface over the same agent core — conversations started in the desktop can be resumed in the CLI and vice versa.

**Repository:** https://github.com/fathah/hermes-desktop
**License:** MIT
**Status:** Active development — features may change and break; issues welcome; contributions accepted.

---

## 2. Relationship to Hermes Agent (Upstream)

Hermes Desktop is a thin desktop shell over the upstream **Hermes Agent** project (`NousResearch/hermes-agent`). Key facts about the relationship:

- **Same agent core:** The desktop reuses the Hermes Agent core unchanged. Configuration, API keys, sessions, skills, and memory are all shared with the CLI.
- **Installation:** The app runs the official Hermes install script (`install.sh` on Linux/macOS, `install.ps1` on Windows) with `--SkipSetup`, then completes provider configuration through the GUI.
- **Not a fork:** The desktop is an officially sanctioned, community-built wrapper. Nous Research publishes it on the Hermes website and documentation.
- **Hermes Agent version bundled:** The latest release (v0.6.0 of the desktop) ships with Hermes Agent v0.15.x. The upstream agent is at v0.16+ as of mid-June 2026, indicating the desktop may trail the CLI by a minor version cycle.
- **Messaging gateway:** Both the CLI gateway and the desktop gateway use the same Hermes gateway process (`hermes gateway`), so platform adapters (Telegram, Discord, etc.) work identically.

---

## 3. Technical Architecture

### 3.1 Tech Stack

| Layer | Technology |
|---|---|
| Desktop shell | Electron 39.2.6 |
| UI framework | React 19.2.1 + TypeScript 5.9 |
| Styling | Tailwind CSS 4.2.2 |
| Build tool | Vite 7.2.6 + electron-vite 5.0.0 |
| Session storage | better-sqlite3 12.8.0 (FTS5 full-text search) |
| Internationalization | i18next 25.6.0 + react-i18next 15.7.3 |
| Testing | Vitest 4.1.4 + Playwright 1.60.0 |
| Auto-update | electron-updater 6.3.9 |
| Analytics | PostHog (opt-in, disclosed in Settings) |
| 3D interface | Three.js 0.183 + React Three Fiber 9.5 |
| Markdown rendering | react-markdown 10 + remark-gfm 4.0 |
| Syntax highlighting | highlight.js 11 |

### 3.2 Local vs. Remote Modes

Hermes Desktop supports two backend modes, selected on first launch:

**Local mode:**
- Checks for existing Hermes installation in `~/.hermes`; if absent, runs the official installer (Git, uv, Python 3.11+ required).
- Launches Hermes as a local subprocess on `http://127.0.0.1:8642`.
- Chat requests flow through `127.0.0.1:8642` with SSE streaming.
- The desktop parses the SSE stream in real time, rendering tool progress, markdown content, and token usage as data arrives.

**Remote mode:**
- Prompts for remote API URL and API key.
- Validates connection before proceeding.
- Skips local Hermes installation entirely.
- All streaming and API calls go to the configured remote URL with the same SSE protocol.

### 3.3 File Layout (Hermes Agent side)

```
~/.hermes/
├── .env                          # API keys and secrets
├── config.yaml                   # Provider config, display settings
├── hermes-agent/                 # The agent installation
├── profiles/                     # Named profile directories (isolated config)
├── state.db                      # SQLite session history + FTS5
├── cron/
│   └── jobs.json                 # Scheduled tasks
└── logs/
    └── gateway.log               # Gateway process logs
```

### 3.4 Architecture Diagram (Messaging Gateway)

The Hermes messaging gateway is a long-running background process that connects to multiple messaging platforms simultaneously. The desktop provides a GUI control panel for it.

```
[Platforms: Telegram, Discord, Slack, WhatsApp, Signal, Email, etc.]
         │
         ▼
┌─────────────────────────────────────┐
│  Gateway Process (hermes gateway)   │
│  ─────────────────────────────────  │
│  • Platform adapters (20+ platforms)│
│  • SessionStore (per-chat history)  │
│  • AIAgent (message → LLM → tools) │
│  • Cron scheduler (60s tick)        │
│  • Circuit breaker per platform     │
│  • Delivery layer (outbound msgs)   │
└─────────────────────────────────────┘
         │
         ▼
┌─────────────────────────────────────┐
│  AIAgent (run_agent.py)            │
│  ─────────────────────────────────  │
│  • Prompt Builder (system prompt)   │
│  • Provider Resolution              │
│  • Tool Dispatch (70+ tools)       │
│  • Compression & Caching            │
│  • Session persistence (SQLite)    │
└─────────────────────────────────────┘
         │
         ▼
┌─────────────────────────────────────┐
│  Model Providers (OpenAI-compatible)│
│  Nous Portal, OpenRouter,          │
│  Anthropic, OpenAI, Google, xAI,   │
│  HuggingFace, Groq, local endpoints │
└─────────────────────────────────────┘
```

Each platform adapter receives messages, routes them through a per-chat session store, and dispatches them to the AIAgent. The gateway also runs the cron scheduler, ticking every 60 seconds to execute due jobs.

---

## 4. Features in Detail

### 4.1 First-Run Setup
- Guided install wizard with dependency resolution (Git, uv, Python 3.11+).
- Mode selection: Local or Remote backend.
- Provider selection: OpenRouter, Anthropic, OpenAI, Google (Gemini), xAI, Nous Portal, Qwen, MiniMax, Hugging Face, Groq, or custom local endpoint.
- Local presets for LM Studio, Atomic Chat, Ollama, vLLM, and llama.cpp.
- Atlas Cloud integration as a pre-configured OpenAI-compatible provider.

### 4.2 Chat
- SSE streaming with real-time tool progress indicators, markdown rendering, and syntax highlighting.
- Live token usage tracking (prompt/completion tokens + cost) displayed in chat footer.
- 22 slash commands: `/new`, `/clear`, `/fast`, `/web`, `/image`, `/browse`, `/code`, `/shell`, `/usage`, `/help`, `/tools`, `/skills`, `/model`, `/memory`, `/persona`, `/version`, `/compact`, `/compress`, `/undo`, `/retry`, `/debug`, `/status`.
- Reasoning steps and tool calls are surfaced live in the chat (collapsible in history).
- Right-click context menu: copy/paste/select-all and copy-entire-chat.
- Per-conversation context folder: pin a local folder to a conversation for project-specific context.
- Image support: compress oversized images and set Content-Length on chat POSTs.
- CJK IME composition handling to prevent Enter from sending truncated text.

### 4.3 Sessions
- Full-text search via SQLite FTS5.
- Date-grouped history browsing.
- Session resume and cross-conversation search.
- Per-row delete button on session list.
- Auto-refresh while the Sessions tab stays open.
- Session title sync and model sync on cache refresh.

### 4.4 Profiles (Multi-Agent)
- Create, delete, and switch between separate Hermes environments.
- Each profile has isolated config, memory, sessions, and gateway PID.
- Full profile management UI in the "Agents" screen.

### 4.5 Models
- CRUD management for saved model configurations per provider.
- Live model discovery autocomplete from provider's `/v1/models` endpoint.
- OAuth provider model list support (ChatGPT, xAI Grok, Qwen, Gemini CLI, MiniMax).
- Context window mappings for various models (recently added: agnes, deepseek).

### 4.6 Tools (14 Toolsets)
- Web search, browser, terminal, file, code execution, vision, image generation, TTS, skills, memory, session search, clarify, delegation, MoA, and task planning.
- Per-toolset enable/disable UI.
- Exposed through Hermes Agent's 70+ built-in tools.

### 4.7 Skills
- Browse, install, and manage bundled and installed skills.
- Compatible with agentskills.io open standard.
- Discover tab for finding new skills.
- Skill uninstall and install fixups.

### 4.8 Memory System
- View/edit memory entries, user profile, and capacity tracking.
- Discoverable memory providers: Honcho, Hindsight, Mem0, RetainDB, Supermemory, ByteRover.
- Pluggable memory architecture (one active provider at a time).

### 4.9 Persona Editor (SOUL.md)
- Edit and reset the agent's SOUL.md personality file.
- Per-profile persona isolation.

### 4.10 Scheduled Tasks (Cron)
- Cron job builder with minutes, hourly, daily, weekly, and custom cron expressions.
- 15 delivery targets (any messaging platform, email, webhook, etc.).
- Jobs stored in `~/.hermes/cron/jobs.json`.
- Background task notifications with configurable verbosity (all / result / error / off).

### 4.11 Messaging Gateways (16 platforms)
- Telegram, Discord, Slack, WhatsApp, Signal, Matrix/Element, Mattermost, Email (IMAP/SMTP), SMS (Twilio & Vonage), iMessage (BlueBubbles), DingTalk, Feishu/Lark, WeCom, WeChat (iLink Bot), Webhooks, Home Assistant.

**Platform comparison matrix:**

| Platform | Voice | Images | Files | Threads | Reactions | Typing | Streaming |
|---|---|---|---|---|---|---|---|
| Telegram | ✅ | ✅ | ✅ | — | ✅ | ✅ | ✅ |
| Discord | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| Slack | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| WhatsApp | — | ✅ | ✅ | — | ✅ | ✅ | ✅ |
| Signal | — | ✅ | ✅ | — | ✅ | ✅ | — |
| Email | — | ✅ | ✅ | — | — | — | — |
| Mattermost | ✅ | ✅ | ✅ | — | ✅ | ✅ | ✅ |
| Matrix | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| DingTalk | — | ✅ | ✅ | — | ✅ | — | ✅ |
| Feishu/Lark | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| WeCom | ✅ | ✅ | — | — | — | — | — |
| Weixin | ✅ | ✅ | ✅ | — | ✅ | ✅ | — |
| BlueBubbles | — | ✅ | ✅ | — | ✅ | ✅ | — |
| Microsoft Teams | — | ✅ | — | ✅ | — | ✅ | — |

Gateway features:
- Automatic circuit breaker per adapter (auto-pauses on repeated failures).
- `/platform list/pause/resume` commands for runtime control.
- Per-platform reset policies (daily at specific hour, idle after N minutes, or combined).
- User allowlist + DM pairing with cryptographic one-time codes (OWASP/NIST SP 800-63-4 compliant).
- Admin vs. regular user tier split per platform/scope.
- Tool progress notifications as chat status messages.

### 4.12 Hermes Office (Claw3d)
- Visual 3D interface with dev server and adapter management.
- Built on Three.js + React Three Fiber.
- Claw3D HQ board available as a read-only Kanban view alongside the local board.

### 4.13 Backup & Diagnostics
- Full data backup/restore from Settings.
- System diagnostics export (hermes-diag zip).
- Log viewer for gateway and agent logs.
- Import backup file path resolution fix.

### 4.14 Auto-Updater
- electron-updater for automatic updates on macOS and Windows.
- Check for and install updates from within the app.
- Note: Fedora .rpm builds do not support auto-update (limitation of electron-updater with unsigned .rpm); manual reinstall required.

### 4.15 i18n
- Internationalization framework with English locale complete.
- Community translations in progress: Chinese (zh-CN, zh-TW), Japanese, Spanish LATAM, Turkish.
- Framework ready for additional community translations.

---

## 5. Messaging Gateway Architecture (Deep Dive)

### 5.1 How It Works

The gateway is a single long-running process (`hermes gateway start`) that loads all configured platform adapters. Each adapter:
1. Maintains a persistent connection to its platform's API (Telegram Bot API, Discord WebSocket, etc.).
2. Receives incoming messages and forwards them to `GatewayRunner._handle_message()`.
3. The runner authorizes the user (allowlist or DM pairing), resolves the session key, creates an `AIAgent` with session history, runs the conversation, and delivers the response back through the adapter.

### 5.2 Session Management
- Sessions persist across messages until reset.
- Reset policies: daily (at a configurable hour), idle (after N minutes), or combined.
- Per-platform overrides supported in `~/.hermes/gateway.json`.
- Session ID header (`X-Hermes-Session-Id`) used to resume sessions across gateway restarts.

### 5.3 Security Model
Seven security layers:
1. **User authorization** — per-platform allowlists, DM pairing codes, global allow/deny.
2. **Dangerous command approval** — three modes (manual / smart LLM-assisted / off/YOLO).
3. **Container isolation** — Docker with hardened flags, Singularity, Modal, Daytona, Vercel Sandbox.
4. **MCP credential filtering** — only approved env vars passed to MCP subprocesses; Tirith pre-exec scan.
5. **Context file scanning** — checks project files for prompt-injection patterns before processing.
6. **Cross-session isolation** — sessions cannot access other sessions' data; cron paths hardened.
7. **Input sanitization** — working directory parameters validated against allowlists.

### 5.4 Circuit Breaker
Each adapter is wrapped in an automatic circuit breaker. Repeated retryable failures cause the adapter to auto-pause. An operator notification is sent to the home channel of another live platform when configured. The breaker does not auto-resume — manual `/platform resume <name>` required.

---

## 6. Comparison to Similar Tools

### 6.1 Hermes Agent vs. OpenClaw

| Dimension | Hermes Agent + Desktop | OpenClaw |
|---|---|---|
| **Origin** | Nous Research (AI research lab) | Cole Steinberger → OpenAI → foundation |
| **License** | MIT | MIT |
| **Commercial model** | None (Nous Portal is optional, not required) | SaaS platform (openclawai.io) + ClawHub marketplace |
| **Primary entry point** | CLI-first, gateway is optional layer | Gateway daemon is central, web dashboard |
| **Self-improving loop** | Yes — skill self-improvement, autonomous curator, Honcho dialectic modeling | Skills are hot-reloadable but not autonomously improved |
| **Tool count** | 70+ tools, 28 toolsets | 100+ built-in AgentSkills |
| **Messaging platforms** | 20+ | 15+ |
| **Browser automation** | Camofox Anti-Detection Browser (from v0.7.0) | Playwright-based |
| **MCP support** | Yes — acts as MCP server and client, MCP OAuth 2.1 | Yes |
| **Security model** | 7-layer design from day one | Reactive — multiple CVEs in early versions (CVE-2026-25253, CVE-2026-25891, CVE-2026-26102, CVE-2026-35650) |
| **Supply-chain incidents** | None documented | ClawHavoc (1,184 malicious packages), MCP proxy campaign |
| **Release cadence** | Extremely fast (6 releases in first 50 days) | Less frequent but architecturally larger steps |
| **Learning curve** | Moderate (CLI requires some comfort with terminal) | Lower for GUI-first users |
| **Desktop GUI** | Hermes Desktop (Electron, actively developed) | OpenClaw web app + native macOS app |

**Summary:** OpenClaw is a better control plane with a mature marketplace and lower CLI barrier. Hermes is a better self-improving runtime with stronger security-by-design and a more modular architecture. Many users run both: OpenClaw as the customer-facing multi-platform routing layer and Hermes as the backend specialist for complex recurring tasks. The SwarmClaw project explicitly bridges both.

### 6.2 Hermes Desktop vs. Raw Hermes Agent CLI

| Feature | Hermes Desktop | Hermes Agent CLI |
|---|---|---|
| **Setup complexity** | GUI wizard, beginner-friendly | Manual CLI commands |
| **Chat interface** | Web-style with streaming UI, markdown, tool progress | Terminal TUI |
| **Session browsing** | Visual, searchable, date-grouped | hermes sessions list |
| **Model switching** | GUI picker with live autocomplete | `hermes model` command |
| **Messaging gateway** | Visual control panel + start/stop | `hermes gateway` commands |
| **Cron management** | Visual job builder with 15 delivery targets | JSON editing in `jobs.json` |
| **Memory editing** | GUI view/edit | `hermes memory` commands |
| **Skill browsing** | Discover tab + install/uninstall UI | `hermes skills` CLI |
| **Backup** | One-click backup/restore | Manual file copy |
| **System dependency** | Electron (heavy) | Python 3.11+ (lightweight) |

---

## 7. Installation and Setup Experience

### 7.1 Requirements
- Node.js and npm
- A Unix-like shell environment for the Hermes installer (Linux, macOS, WSL2)
- Network access for downloading Hermes during first-run
- Git, uv, Python 3.11+ (auto-installed by the Hermes installer)

### 7.2 Installation Methods

**Download installers (recommended):**
- macOS: `.dmg` installer
- Windows: `.exe` NSIS installer (unsigned — SmartScreen warning on first launch, click "More info" → "Run anyway")
- Linux: `.AppImage`, `.deb`, `.rpm` (unsigned on .rpm)

**From source:**
```bash
npm install
npm run dev       # development
npm run build     # production build
npm run build:mac / build:win / build:linux
```

**WSL2 note:** If the installer stalls at "Switching to root user to install dependencies...", Playwright is waiting for a sudo password that has no TTY. Grant passwordless sudo temporarily:
```bash
echo "$USER ALL=(ALL) NOPASSWD: ALL" | sudo tee /etc/sudoers.d/hermes-install
# ...re-run installer; revert after:
sudo rm /etc/sudoers.d/hermes-install
```

**Fedora .rpm note:** The .rpm is not GPG-signed. Append `--nogpgcheck` if your system enforces signature checking. Auto-update is not supported for .rpm builds.

### 7.3 First-Run Flow
1. Choose Local or Remote mode.
2. **Local:** Installer runs official Hermes install script with dependency resolution.
3. **Remote:** Enter API URL + key, validate connection.
4. Select provider (OpenRouter, Anthropic, OpenAI, etc.).
5. Configure API keys.
6. Launch workspace.

---

## 8. Open Issues and Known Limitations

### Critical / High Priority

1. **Gateway crash + lock file zombie (Issue #648, reported 2026-06-12)**
   - Gateway restarts 4 times in 20 minutes with `signal=UNKNOWN` (non-normal exit).
   - `gateway.lock` and `gateway.pid` point to a dead PID, causing subsequent restart failures.
   - Affects Windows primarily.
   - **Impact:** Messaging platforms go offline without auto-recovery.

2. **Auto-update progress is coarse (Issue #647)**
   - UI only receives rounded percentage from electron-updater.
   - Windows `latest.yml` lacks `blockMapSize` entry, possibly preventing differential updates.
   - Users may download the full ~157 MB installer on every update.
   - Progress appears "stuck" during slow downloads.

3. **Hermes Agent update progress is coarse (Issue #646)**
   - The `runHermesUpdate` path emits `step: 1, totalSteps: 1` throughout the entire subprocess — no granular phases.
   - Remote SSH update path runs update, gateway restart, tunnel restart, and API key refresh without intermediate progress events.
   - Progress bar tied to regex matching against installer output, which can lag.

### Medium Priority

4. **Windows SmartScreen blocks installer**
   - The Windows `.exe` installer is not code-signed.
   - SmartScreen flags it on first launch.
   - Expected behavior but a friction point for new users.

5. **Fedora .rpm auto-update not supported**
   - electron-updater does not support signed .rpm updates.
   - Users must manually reinstall for each update.

6. **WSL password TTY issue**
   - Known, documented in README, but still a friction point.
   - Requires granting passwordless sudo temporarily.

7. **Sessions loading hang on Intel macOS (Issue #202, partially fixed)**
   - Some users still experience hangs; fix was merged but may not cover all cases.

8. **Chat reconciliation duplicate split turns (Issue #376, fixed in v0.5.2)**
   - Stream-to-DB reconciliation produced duplicate messages in some cases.
   - Fixed but worth monitoring for regression.

### Lower Priority / Feature Gaps

9. **No Linux native build format aside from AppImage/deb**
   - No Flatpak or native package for most distros.

10. **Nous Portal OAuth not fully surfaced in Desktop**
    - OAuth sign-in works for model selection but not all portal features are accessible via GUI.

11. **Hermes Office (Claw3d) is early-stage**
    - Visual 3D interface is present but primarily a dev server and adapter management tool.

12. **Remote SSH mode less featured**
    - Remote SSH update path lacks granular progress events.
    - Some features behave differently in SSH mode vs. local mode.

---

## 9. Production Readiness Assessment

**Verdict: Conditionally production-ready, with caveats.**

### Strengths
- Actively maintained with rapid release cadence (latest release 2026-06-10).
- Large and active contributor community (550+ PRs merged in a single release cycle for upstream Hermes Agent).
- Strong security-by-design (7 layers, no documented CVEs in Hermes Agent itself).
- Self-improving capabilities make it increasingly capable over time without user intervention.
- Cross-platform messaging gateway with 20+ platforms from a single process.
- Proven upgrade path from OpenClaw via `hermes claw migrate`.

### Weaknesses / Risks
1. **Active development = API churn:** The project explicitly warns that features may change and things may break.
2. **Unsigned Windows installer:** Corporate IT policies may block unsigned executables.
3. **Recent crash bugs:** Issue #648 (gateway crashes + lock file zombies) was reported 2 days ago and is unfixed as of this writing.
4. **Large update payload:** ~157 MB per update on Windows with no differential download confirmed.
5. **Limited enterprise features:** No SSO, no audit logging, no team management, no centralized management console.
6. **Memory provider ecosystem still maturing:** Honcho integration is recent; other providers are in early stages.

### Recommended Production Checklist
- [ ] Use a process supervisor (systemd/launchd) to auto-restart the gateway on crash.
- [ ] Monitor `~/.hermes/logs/gateway.log` for crash signals.
- [ ] Manually clear stale `gateway.lock` / `gateway.pid` files if restart failures occur.
- [ ] Use allowlists (not open access) for all messaging platforms.
- [ ] Keep API keys in `~/.hermes/.env`, not in config files.
- [ ] Use Nous Portal or a reputable provider — avoid free-tier-only configurations for production.
- [ ] Test backup/restore before relying on it.

---

## 10. Best Use Cases

### ✅ Ideal For

1. **Power users who want GUI + CLI flexibility**
   - Use the desktop for day-to-day chat, session management, and configuration.
   - Drop to CLI for advanced operations, scripting, or SSH into a remote instance.

2. **Self-hosted personal AI assistant**
   - Run Hermes on a home server or VPS.
   - Connect to Telegram/Discord for natural language control.
   - Schedule nightly reports, weekly summaries, and automated backups.

3. **Multi-platform presence management**
   - Single agent instance serving Telegram, Discord, Slack, and email simultaneously.
   - Circuit breaker protects against one platform taking down the others.

4. **Development teams wanting AI coding assistance**
   - MCP server integration for IDE connectivity (VS Code, Zed, JetBrains).
   - Skills system for project-specific automation.
   - ACP (Agent Communication Protocol) for sub-agent spawning.

5. **Researchers doing trajectory collection and training**
   - Batch trajectory generation with ShareGPT export.
   - RL training integration via Atropos.
   - Multiple model provider support for comparative experiments.

6. **Advanced users who value self-improvement**
   - The agent autonomously creates skills from complex tasks.
   - Skill self-improvement during use means the agent gets better the more you use it.
   - "The Curator" (v0.12+) removes unused skills and consolidates redundant ones automatically.

### ⚠️ Less Ideal For

1. **Non-technical users who want plug-and-play**
   - The Hermes installer and configuration still require some terminal comfort.
   - Windows SmartScreen warnings and unsigned executables create friction.

2. **Enterprise deployments requiring compliance**
   - No audit logging, SSO, or role-based access control.
   - No commercial support options.

3. **Mission-critical systems requiring guarantees**
   - Recent crash bugs (gateway instability) make it unsuitable for unattended critical automation without careful monitoring.

---

## 11. Key Source Files Reference

| File | Purpose |
|---|---|
| `package.json` | Electron app definition, all dependencies |
| `src/main/index.ts` | Electron main process, window management, IPC |
| `src/main/installer.ts` | Hermes Agent install/update logic, progress tracking |
| `src/renderer/src/screens/Layout/Layout.tsx` | Main UI layout, sidebar, auto-updater UI |
| `src/renderer/src/screens/Install/Install.tsx` | First-run install wizard UI |
| `src/renderer/src/screens/Chat/` | Chat UI with SSE streaming |
| `src/renderer/src/screens/Sessions/` | Session browsing and search |
| `src/renderer/src/screens/Gateway/` | Messaging gateway control panel |
| `src/renderer/src/screens/Settings/` | Provider config, backup, log viewer |
| `electron-builder.yml` | Build configuration for all platforms |

---

## 12. Summary

Hermes Desktop is a well-architected Electron wrapper around the capable Hermes Agent framework. Its primary strengths are:
- **A genuine self-improving agent** with autonomous skill creation, skill improvement during use, and dialectic user modeling.
- **Comprehensive messaging gateway** with 20+ platforms, circuit breakers, and per-user access control.
- **Strong security model** built in from the ground up (vs. OpenClaw's reactive fixes after CVEs).
- **Excellent multi-provider flexibility** — works with OpenRouter, Anthropic, OpenAI, Nous Portal, or any OpenAI-compatible endpoint.
- **Active development** with rapid releases and a large, engaged contributor community.

Its main weaknesses are:
- **Active development means instability** — recent crash bugs, unsigned executables, and coarse progress UI are real friction points.
- **Not yet enterprise-ready** — lacks SSO, audit logging, and centralized management.
- **Heavy desktop app** — Electron is resource-hungry compared to the lightweight CLI.

For developers and power users comfortable with some terminal work, Hermes Desktop represents one of the most capable open-source AI agent platforms available in 2026. For non-technical users or mission-critical deployments, approach with caution and ensure monitoring is in place.

---

*Research conducted by: Subagent | Sources: GitHub README, Hermes Agent docs (hermes-agent.nousresearch.com/docs), package.json, release notes, open issues (#646, #647, #648), architecture docs, third-party comparisons (innfactory.ai, petronellatech, flowtivity.ai, Reddit r/LocalLLM, YouTube reviews).*