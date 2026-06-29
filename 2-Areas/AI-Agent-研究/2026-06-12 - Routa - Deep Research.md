---
type: research-report
okf_metadata:
  schema: okf-v0.1-inspired
  added_by: okf-batch-2026-06-16
title: Routa — Deep Research Report
description: Routa is a workspace-first multi-agent coordination platform for software
  delive...
tags:
- Agent
---
# Routa — Deep Research Report

**Date:** 2026-06-12
**Subject:** https://github.com/phodal/routa
**Latest Release:** v0.18.0 (April 28, 2026)
**License:** MIT

---

## 1. Project Overview

Routa is a **workspace-first multi-agent coordination platform for software delivery**. It was created by [Phodal](https://github.com/phodal) (a prolific open-source author known for IoT and developer tooling projects) to solve the problem of keeping complex multi-agent work visible, traceable, and quality-gated — rather than burying everything in a single long-running chat thread.

The project is written in TypeScript (Next.js frontend + React) and Rust (Axum backend via Tauri), and ships in three deployment forms:

| Surface | Best For | Start Command |
|---|---|---|
| **Desktop** | Full product experience, visual workflows, local-first | Download from GitHub Releases |
| **CLI** | Terminal-first workflows, scripting | `npm install -g routa-cli` |
| **Web** | Self-hosting or browser-first access | `npm run dev` |

The project is actively developed — the GitHub releases page shows desktop releases every 2–4 days and npm/Rust package updates on a similar cadence through April–June 2026. Version 0.18.0 (April 22, 2026) was a major release introducing task-adaptive intelligence, JIT context system, global flow learning, and Kanban CLI enhancements.

**Repository stats (as of research date):**
- ~16 open issues, 4 open PRs
- Monorepo with TypeScript (src/) and Rust (crates/) workspaces
- 7 Rust crates, 15 npm packages published
- Desktop installers for macOS (Intel + Apple Silicon), Windows (.msi + .exe), Linux (.deb + .AppImage)

---

## 2. Technical Architecture

### 2.1 Dual-Backend Design

Routa's most distinctive architectural decision is its **dual-backend semantic parity** model (ADR-0001). Web (Next.js) and Desktop (Tauri + Axum/Rust) are **not** two separate products — they are two deployment surfaces for the same domain model.

Both runtimes must:
- Preserve identical domain vocabulary (workspace, session, task, kanban board, specialist, worktree, etc.)
- Expose the same API shape, governed by `api-contract.yaml`
- Pass API contract parity tests in CI (`npm run api:check`)
- Wire the same stores, event buses, and domain services

| Layer | Web Runtime | Desktop Runtime |
|---|---|---|
| **Assembly point** | `src/core/routa-system.ts` | `crates/routa-core/src/state.rs` |
| **Transport** | Next.js route handlers | Axum routers |
| **Storage** | Postgres (DATABASE_URL) or SQLite | SQLite (local-first) |
| **Agent execution** | ACP runtime over HTTP | ACP runtime in-process |

The TypeScript web runtime selects storage based on environment: `DATABASE_URL` → Postgres; `ROUTA_DB_DRIVER=sqlite` or local Node → SQLite; fallback → in-memory.

The Rust desktop backend owns: local SQLite persistence, ACP runtime management, Docker-assisted agent execution, sandbox management, and local file/worktree operations.

### 2.2 Repository Structure

```
src/app/          Next.js App Router pages and API routes
src/client/       React components, hooks, view models, A2UI helpers
src/core/         TypeScript domain: ACP/MCP, Kanban, workflows, traces, review, harness, stores

apps/desktop/      Tauri shell and desktop packaging

crates/routa-core/         Shared Rust domain/runtime: stores, ACP, sandbox, skills, events
crates/routa-server/       Axum HTTP API (used by desktop + local server mode)
crates/routa-cli/           CLI entrypoints and ACP serving commands
crates/routa-rpc/           RPC contract helpers
crates/routa-scanner/       Codebase scanning utilities
crates/harness-monitor/     Run observation, evaluation, operator-facing harness monitor
crates/entrix/              Fitness execution engine (fitness rules CLI)

docs/             Architecture, design intent, plans, fitness guidance
resources/specialists/      YAML specialist prompts and workflows
```

### 2.3 Key Domain Objects

- **Workspace**: Top-level coordination boundary. Owns sessions, kanban boards, notes, tasks, codebases, worktrees, memories. Users navigate by workspace first.
- **Codebase**: Models repo identity (path, branch, label, default status). A workspace can own multiple codebases.
- **Worktree**: Ephemeral or semi-persistent execution copies tied to a workspace and codebase. File search, sandbox resolution, and repo selection flow through worktree context.
- **Session**: Represents a live or historical agent execution thread. Workspace-scoped. Powers session detail, trace views, and automation status. Stored in DB rows and/or JSONL trace files.
- **Task**: Durable work units. Kanban is not just a UI projection — column transitions can trigger fresh ACP sessions and enrich tasks with provider/role/session metadata.
- **Board/Kanban**: Drives lane-based automation and queueing. Per-board concurrency enforced by the TypeScript queue in `src/core/kanban/kanban-session-queue.ts`.

### 2.4 Protocol Stack

Routa supports multiple integration surfaces as first-class interfaces:

| Protocol | Primary Endpoints | Role |
|---|---|---|
| **REST** | `/api/*` | CRUD and product-facing operations |
| **MCP** | `/api/mcp`, `/api/mcp/tools` | Tool execution, collaborative agent capabilities |
| **ACP** | `/api/acp` + runtime/registry/docker routes | Spawn, prompt, stream, install, warm up, manage agent runtimes |
| **A2A** | `/api/a2a/*` | Agent-to-agent interoperability |
| **AG-UI** | `/api/ag-ui` | UI-facing agent stream protocol |
| **A2UI** | `/api/a2ui/*` | Dashboard-oriented UI protocol surfaces |
| **SSE** | ACP, notes, AG-UI, related endpoints | Incremental UI updates |

### 2.5 Provider Normalization

ACP is the primary execution protocol for coding agents, but different providers behave differently. The normalization pattern:

```
Provider process or bridge
  → provider-specific output / notifications
  → adapter normalization
  → unified session updates
  → persistence, traces, and UI streaming
```

Current concerns include: standard ACP-compatible CLIs, Claude Code-style stream-json flows (must be translated into ACP-like updates), Docker-backed OpenCode execution paths, and runtime installation/warmup/registry discovery.

Provider normalization means provider-specific behavior is isolated in adapter layers and never leaks into the product.

---

## 3. Kanban Workflow — Deep Dive

Routa's Kanban is the **primary coordination bus**, not just a status visualization layer. Each lane is backed by a different specialist prompt, and each downstream lane is deliberately stricter than the previous one.

### 3.1 The Six Lanes

| Lane | Specialist | What Gets Written | Handoff Rule |
|---|---|---|---|
| **Backlog** | Backlog Refiner | Canonical YAML story: problem statement, acceptance criteria, constraints, dependencies, out-of-scope, INVEST checks | Move to Todo only when story parses and is independently executable |
| **Todo** | Todo Orchestrator | Execution Plan, Key Files/Entry Points, Dependency Plan, Risk Notes | Move to Dev only when implementation can start within minutes |
| **Dev** | Dev Crafter | Dev Evidence: changed files, work summary, tests run, per-AC verification, caveats | Move to Review only after commit exists and worktree is clean |
| **Review** | Review Guard | Review Findings: verdict, per-AC status, issues found, reviewer notes | Move to Done only with APPROVED verdict |
| **Done** | Done Reporter | Completion Summary: what shipped, key evidence, completion date | Stay in Done (terminal) |
| **Blocked** | Blocked Resolver | Blocker Analysis: blocker type, root cause, resolution, routing decision | Return to Backlog/Todo/Dev/Review or remain Blocked |

### 3.2 The Strictness Ratchet

The card becomes stricter over time:
- **Backlog** produces the canonical story YAML
- **Todo** adds the execution brief
- **Dev** adds evidence of implementation and verification
- **Review** adds a formal verdict and findings
- **Done** adds a completion summary

This means each column changes what the next specialist is **allowed to trust**. Downstream specialists distrust upstream output and re-validate independently.

### 3.3 Core Role Triad

Beyond the lane specialists, three core roles drive the system:

- **ROUTA Coordinator**: Plans first, never edits files directly, writes the spec, waits for approval, delegates work in waves, calls GATE for verification after implementation.
- **CRAFTER Implementor**: Stays within task scope, avoids refactors and scope creep, coordinates with other agents when files overlap, runs verification steps, commits in small units.
- **GATE Verifier**: Verifies against acceptance criteria only, treats evidence as mandatory, does not allow partial approval, reports explicit verdicts.

### 3.4 Lane Specialist Prompts

The built-in lane prompts live under `resources/specialists/workflows/kanban/*.yaml`, and core role prompts under `resources/specialists/core/{routa,crafter,gate}.yaml`. These are Markdown+YAML prompt contracts, making them inspectable and editable.

### 3.5 Kanban Automation

The TypeScript queue (`src/core/kanban/kanban-session-queue.ts`) enforces per-board concurrency and prevents stale auto-run entries from re-firing incorrectly. Column transitions can trigger fresh ACP sessions. The v0.18.0 release added:
- `routa kanban status` — board status overview
- `routa kanban list` — card list with filters
- `routa kanban card-detail` — detailed card inspection
- GitHub issue workflow integration
- Global Flow Learning: AI specialist-driven analysis, automatic bottleneck detection, evidence-backed improvement suggestions
- Lane automation with A2A handoffs, automatic delegation for blocked cards

---

## 4. The Review Gate Mechanism

The delivery gate is a **stacked decision path**, not a single reviewer persona. Three specialist layers work together:

### 4.1 Harness Monitor
**Answers: "What happened?"**

Surfaces traces, changed files, commands, git state, and attribution. This is the run observation layer — it records what the agent did. Part of the `crates/harness-monitor` subsystem, which implements a four-layer harness loop: **Context → Run → Observe → Govern**.

### 4.2 Entrix Fitness
**Answers: "What should be true?"**

Enforces hard gates, evidence requirements, and policy checks against a defined fitness model. This is the validation engine. Executed via the `entrix` CLI:

```bash
# Fast check (<30s)
entrix run --tier fast

# Standard check (fast + normal, <5min)
entrix run --tier normal

# Full check (all tiers, <15min)
entrix run
```

The fitness model is weighted across dimensions:

| Dimension | Weight | Description |
|---|---|---|
| code_quality | 18% | File/function budget, lint/typecheck/clippy, duplication, complexity |
| testability | 20% | Coverage ≥80%, pass rate 100% |
| security | 20% | Critical=0, high≤threshold |
| api_contract | 10% | Rust API tests pass, contract sync |
| design_system | 10% | CSS contract, component visual regression, accessibility |
| evolvability | 8% | Breaking changes=0, parity=100% |
| ui_consistency | 8% | Shell component coverage, token接入 |
| engineering_governance | 6% | Blast radius, external link reachability, TODO/FIXME monitoring |

**Score = Σ(Weight_i × Score_i) / 100**
- **< 80**: Hard gate blocks (fails CI)
- **80–90**: Strong warning
- **≥ 90**: Pass

Observability (0%) and Performance (0%) are tracked but don't affect the score.

### 4.3 Gate Specialist
**Answers: "Can the card move?"**

Verifies acceptance criteria and routes to Done, Dev, or human escalation. Issues explicit APPROVED/REJECTED verdicts, not vague confidence scores. Rejects scope creep, dirty git state, broken lint/type checks, and missing evidence.

### 4.4 Fitness Evidence System

Fitness rules are declarative YAML frontmatter in `docs/fitness/*.md` files. The `crates/entrix/` engine parses frontmatter, executes shell commands, and scores results. Example frontmatter:

```yaml
---
dimension: testability
weight: 20
threshold:
  pass: 80
  warn: 70
metrics:
  - name: ts_test_pass
    command: npm run test:run:fast 2>&1
    pattern: "Tests\\s+passed"
    hard_gate: true
---
```

The system enforces that:
- Each new/modified endpoint must have at least 1 positive case, 1 negative case, and 1 critical invariant assertion
- All critical entries must be VERIFIED before a PR can be approved
- Negative-path gaps block the critical qualification criteria

### 4.5 Harness Fluency & Harnessability

Two related concepts:
- **Harness Fluency**: Internal maturity model + scoring engine (calculates level, readiness, blocking criteria, recommendations)
- **Harnessability**: External framing of the same results — answers "is this repo/workspace suitable for high-autonomy coding agents?"

`routa fitness fluency` runs the assessment; `--framing harnessability` projects it to an external baseline report.

---

## 5. ACP/MCP/A2A Integration Details

### 5.1 ACP (Agent Communication Protocol)

ACP is the primary execution transport for agent CLIs. The Rust ACP subsystem lives under `crates/routa-core/src/acp/`, while the web runtime has corresponding logic under `src/core/acp/` and `src/app/api/acp/`.

Key ACP operations:
- `POST /api/acp` — ACP JSON-RPC endpoint
- `GET /api/acp` — ACP SSE stream
- `POST /api/acp/install` — Install an ACP agent
- `GET /api/acp/registry` — List agents in registry
- `POST /api/acp/runtime` — Start ACP runtime
- `POST /api/acp/warmup` — Trigger ACP warmup
- Docker routes: container start/stop, image pull, daemon status

ACP registry discovery, binary warmup, and runtime management are all first-class APIs.

### 5.2 MCP (Model Context Protocol)

MCP is exposed at `/api/mcp` and `/api/mcp/tools`. MCP tools in Routa include:
- `AgentTools` — agent execution surfaces
- `NoteTools` — collaborative note management
- `WorkspaceTools` — workspace-scoped operations
- Feature tree preload tools
- File session summary tools
- History analyst capabilities (from v0.18.0 JIT context system)

The `routa-cli acp list` command can list available agents.

### 5.3 A2A (Agent-to-Agent Protocol)

Routa implements the A2A protocol at `/api/a2a/*`:
- `GET /api/a2a/card` — A2A agent card
- `POST /api/a2a/message` — Send A2A message
- `GET/POST /api/a2a/rpc` — A2A SSE stream and JSON-RPC
- `GET /api/a2a/sessions` — List A2A sessions
- `GET/POST /api/a2a/tasks` — Task management

A2A is used for lane automation handoffs in the Kanban workflow.

### 5.4 AG-UI and A2UI

- **AG-UI** (`/api/ag-ui`): UI-facing agent stream protocol (SSE)
- **A2UI** (`/api/a2ui/*`): Dashboard-oriented protocol surfaces; v0.10 dashboard data at `GET /api/a2ui/dashboard`

### 5.5 Real-Time Mechanisms

Two real-time layers:
1. **Transport-level streaming**: SSE for session, note, and protocol updates
2. **In-process eventing**: `EventBus` in both TypeScript and Rust runtimes

These support: agent lifecycle tracking, Kanban auto-run queue draining, note change propagation, workflow/background-task coordination, and UI refresh triggers.

---

## 6. Comparison with Other Multi-Agent Coordination Tools

### 6.1 Positioning

Most multi-agent frameworks fall into three categories:

| Framework | Paradigm | Key Characteristic |
|---|---|---|
| **LangGraph** (LangChain) | Graph-based workflow | Best for graph-representable workflows; strong visualization |
| **CrewAI** | Role-based | Organizational structure; efficient multi-agent interactions |
| **AutoGen** (Microsoft/AG2) | Conversational collaboration | Best for conversational workflows between agents |
| **Google ADK** | Task decomposition | Hierarchical task decomposition |
| **OpenAI Agents SDK** | Handoff-based | Native A2A support; straightforward orchestration |
| **Mastra** | Agent dev framework | Type-safe; good for production JS/TS apps |
| **Agno** | Team-based | Field-oriented, lightweight |

### 6.2 How Routa Differs

**Routa's unique differentiators:**

1. **Kanban-as-coordination-bus**: Most frameworks model agent workflows as pipelines or graphs. Routa models work as a Kanban board where lane transitions are the coordination mechanism, making human-readable task state a first-class concept.

2. **Dual-backend parity**: No other framework ships a native desktop app with the same domain model as the web version. The api-contract.yaml enforcement is unique.

3. **Fitness-based governance**: The `entrix` fitness engine with weighted dimensions, hard gates, and evidence-based scoring is more rigorous than typical "unit test pass" gates in other frameworks.

4. **Local-first execution**: Desktop mode uses SQLite, local agent binaries, local worktrees, and JSONL trace files — no cloud dependency required.

5. **Multi-protocol first-class**: ACP, MCP, A2A, AG-UI, A2UI, REST, SSE — all treated as equal integration surfaces. Most frameworks are built around one or two protocols.

6. **Specialist prompt contracts**: Lane specialists are defined as YAML prompt contracts with explicit evidence requirements — inspectable, editable, versionable.

### 6.3 Comparative Weaknesses

- **Ecosystem maturity**: LangGraph, CrewAI, and AutoGen have massive community adoption and many more third-party integrations. Routa is a smaller, more specialized project.
- **Documentation**: An open issue (GitHub #574) calls the documentation "跟屎一样" (crap) — setup and onboarding documentation has significant usability issues.
- **Cross-platform stability**: Open issues around macOS provider configuration (opencode not recognizing models, path issues with multica) and web panel Git staging not working.
- **Scope**: Routa targets software delivery workflows specifically; general-purpose frameworks like LangGraph are more broadly applicable.

---

## 7. Strengths, Weaknesses, and Known Limitations

### Strengths

1. **Visible, durable work state**: Kanban board + session traces + review findings mean work never gets lost in a chat thread.
2. **Strict lane handoffs**: The distrust model (each downstream specialist re-validates upstream output) enforces real quality gates, not rubber-stamp approvals.
3. **Fitness-based governance**: The weighted multi-dimensional fitness model with hard gates is more rigorous than typical CI.
4. **Local-first**: Desktop mode with SQLite means no cloud dependency; everything runs locally.
5. **Multi-protocol integration**: ACP/MCP/A2A/AG-UI/A2UI all first-class; Routa is designed to be part of a larger agent ecosystem, not a silo.
6. **Task-adaptive intelligence** (v0.18.0): JIT context system, history memory snapshots, and session transcript analysis reduce repeated friction.
7. **Active development**: Rapid release cadence (desktop every 2–4 days), active issue resolution.

### Weaknesses

1. **Documentation quality**: Setup and onboarding documentation is flagged as poor by users (GitHub #574).
2. **Cross-platform provider support**: macOS provider configuration issues, opencode model recognition problems.
3. **Git features in web panel**: Git staging and commit UI in the web panel doesn't work reliably (GitHub #570).
4. **Workspace-centric redesign incomplete**: Some APIs still fall back to "default" workspace when workspaceId is absent. Bootstrap flows still assume default workspace exists.
5. **Learning curve**: The Kanban specialist + fitness gate + review gate system is more complex than simple agent chat.

### Known Open Issues (Selected)

| # | Issue | Type |
|---|---|---|
| #575 | opencode doesn't recognize model; path shows multica path instead | Bug |
| #574 | macOS environment unusable; both codex and claude providers error; documentation called "跟屎一样" | Bug/Docs |
| #570 | Git staging/commit in web panel UI not working | Bug |
| #572 | Proposal: Complete Hermes ACP Integration for Routa (external contributor with code ready) | Feature |
| #565 | Show active SSH key in settings (for Docker deployment) | Feature |

---

## 8. Production Readiness Assessment

### 8.1 What "Production-Ready" Means for Routa

Routa is actively used and developed, but there are important caveats:

**Evidence for maturity:**
- Version 0.18.0 with significant features shipped
- API contract parity tests enforced in CI
- Fitness hard gates block <80 score in CI
- Rust + TypeScript dual-backend with well-defined boundaries
- Auto-generated feature tree (`docs/product-specs/FEATURE_TREE.md`) for tracking shipped vs. evolving features
- ADRs (Architecture Decision Records) document design rationale

**Evidence against full production readiness:**
1. **Workspace-centric redesign incomplete**: Some APIs fall back to "default" workspace when workspaceId is absent; bootstrap flows still assume default workspace; not every persistence-backed implementation is symmetric across TypeScript and Rust.
2. **Open bugs in core flows**: Git staging UI broken in web panel (#570), provider configuration issues on macOS (#574, #575) — these are not edge cases.
3. **Small community**: 16 open issues, 4 open PRs, Slack channel exists but no public metrics on active users.
4. **Active transition state**: The project is explicitly in a transition from older patterns to workspace-centric models. "Treat 'default' as transition scaffolding, not as the target domain model."

### 8.2 Readiness Verdict

**Not yet production-ready for general audience**, but **worth evaluating for technical teams** who:
- Have complex multi-agent workflows that are currently managed in chat
- Need visible, auditable delivery state rather than opaque agent threads
- Are comfortable with bleeding-edge tooling and can work around documentation gaps
- Have use cases that map well to Kanban-style task routing

The fitness gate system and the lane specialist architecture are the most mature aspects. The areas that need more hardening are: provider configuration (especially macOS), web panel Git features, and the workspace fallback cleanup.

---

## 9. Best Use Cases and Target Users

### 9.1 Ideal Use Cases

1. **Complex feature delivery with quality gates**: When a feature requires decomposition, implementation, independent review, and evidence collection — the Kanban lane system shines.
2. **Multi-agent coordination where attribution matters**: When you need to know "which agent changed what, when, and why" — Routa's trace-first design makes this explicit.
3. **Local-first AI coding environments**: Teams that want AI coding agents running locally without cloud dependency.
4. **Fitness-conscious development**: Organizations that want AI coding to respect file budgets, test coverage thresholds, and lint gates rather than just "write code and hope."
5. **Specialist-separable workflows**: Work that naturally decomposes into Backlog Refiner → Todo Orchestrator → Dev Crafter → Review Guard → Done Reporter.

### 9.2 Less Ideal Use Cases

1. **Simple single-task agent invocation**: If you just want to ask one agent to do one thing, a simpler tool (Claude Code, Cursor, Copilot) is more appropriate.
2. **Non-developer teams**: Routa assumes developer context (git, repos, codebases, worktrees).
3. **Broad ecosystem dependency**: If you need the largest community, plugins, and third-party integrations, CrewAI or LangGraph are more mature choices.
4. **Windows-focused teams**: Some open issues around Windows terminal handling; documentation quality issues affect all platforms but disproportionately impact first-time setup.

### 9.3 Target User Profile

- **Technical lead or senior developer** evaluating or running AI-augmented delivery workflows
- **Team working on complex multi-agent systems** where coordination overhead is the bottleneck
- **Developer who wants local-first AI coding** with visible quality gates and traceable execution
- **Organization building internal agent platforms** that need multi-protocol integration (ACP/MCP/A2A)

---

## 10. Additional Notable Features

### 10.1 Feature Explorer

Workspace-scoped surface for inspecting feature surfaces and session-backed file activity. Routes through Rust CLI for consistency. Agent-driven feature tree generation workflow with preflight/commit routes and multi-root scanning. Security: validates scanRoot inside repoRoot and resolves symlink traversal.

### 10.2 Session Recovery

Restore, inspect, and continue workspace-scoped agent sessions. Supports transcript recovery, context resumption, reposlide result generation. Full session lifecycle API: create, prompt, cancel, reconnect, streaming, trace inspection.

### 10.3 Team Runs

Multi-agent team orchestration within a workspace. Orchestrate and inspect team runs at `/workspace/:workspaceId/team`.

### 10.4 Harness Console

Inspect repo signals, governance surfaces, and fitness-related runtime status. Routes: `/settings/harness`, `/workspace/:workspaceId/spec`.

### 10.5 Background Tasks & Workflows

Background tasks model durable async work (scheduled runs, polling-triggered actions, workflow fan-out). Schedules, webhooks, and polling adapters all enqueue background tasks rather than invoking execution inline.

### 10.6 Docker Integration

ACP Docker routes for container lifecycle: start/stop containers for OpenCode agents, pull images, check daemon status. Docker-assisted agent execution supported in the Rust backend.

---

## 11. Summary

Routa is a well-architected, actively-developed multi-agent coordination platform with some genuinely novel ideas — particularly the Kanban-as-coordination-bus model, the stacked specialist lane system with explicit distrust-and-revalidate semantics, and the fitness-gate governance model.

Its technical foundations (dual-backend semantic parity, multi-protocol first-class, workspace-first domain model, fitness-based quality enforcement) are sound and well-documented in ADRs.

The main risks for potential adopters are: incomplete workspace-centric cleanup (some default-fallbacks remain), documentation quality that makes onboarding difficult, and cross-platform stability issues that are still being worked out.

For technical teams with complex AI-augmented delivery workflows, Routa is worth a serious evaluation. For general-purpose multi-agent orchestration, more mature alternatives like CrewAI or LangGraph offer broader ecosystem support.

---

*Research compiled 2026-06-12. Sources: GitHub repository, docs site (phodal.github.io/routa), ARCHITECTURE.md, fitness/README.md, releases page, open issues, ADRs, feature tree, contributing guide, design docs.*