---
title: AgentSpace 深度研究笔记（2026-06-29）
date: 2026-06-29
type: research-notes
purpose: AgentRouter 7 runtime 设计借鉴
related:
  - /root/vault/1-Projects/德勤/AI-Native/笔记/2026-06-29-开源研究部署笔记.md
  - /root/vault/1-Projects/德勤/AI-Native/笔记/2026-06-29 - 德勤项目完整深度分析报告（hermes 风格）.md
---

# 🛸 AgentSpace 深度研究笔记 — AdapterRouter 7 runtime 设计

> **写于 2026-06-29 00:14**（Hermes 卡在 cc-vibe.com 期间，我（OpenClaw）继续研究）
> **研究方法**：GitHub Contents API 读 `packages/daemon` + `packages/services/src/clihub/` 关键文件
> **借鉴价值**：AgentRouter 7 runtime 设计 = 德勤 R3 执行器抽象层的**最佳模板**

---

## 🎯 AgentRouter 核心结构

### 7 Runtime 全名单

`packages/daemon/README.md` 明确列出支持的 provider CLI：

```bash
codex         # OpenAI Codex
claude        # Claude Code (Anthropic)
gemini        # Google Gemini
opencode      # OpenCode
openclaw      # OpenClaw ← 我们正在用的
nanobot       # 另一个 agent
hermes        # Hermes ← 已装！直接能用
```

### 环境变量覆盖（运行时选模型）

```bash
CLAUDE_MODEL        # 覆盖 Claude 模型
GEMINI_MODEL        # 覆盖 Gemini 模型
OPENCODE_MODEL      # 覆盖 OpenCode 模型
OPENCLAW_PROFILE    # 覆盖 OpenClaw profile
NANOBOT_MODEL       # 覆盖 Nanobot 模型
HERMES_MODEL        # 覆盖 Hermes 模型
HERMES_INFERENCE_MODEL
```

### packages/daemon/ 设计（远程执行底座）

**核心定位**：数字员工的远程执行层（不是孤立运维组件）

```
agent-space-daemon/
├─ daemon HTTP client         # 远程通信
├─ input bundle 解包           # 接任务
├─ output bundle 打包         # 回收产物
├─ provider CLI 执行 glue     # 调用上述 7 个 runtime
├─ 日志 / PID / 轮询 / 重试 / 优雅退出
└─ HttpDaemonClient (library)  # server-side 调用方复用
```

**关键 invariant**：
- **不依赖** AgentSpace 仓库 checkout
- **不依赖** `Target.md` / `apps/web` / `packages/db` / `packages/services`
- 独立可分发（`npm install -g agent-space-daemon`）

**借鉴德勤 R3**：
- 我们应该有一个 `deloitte-executor-daemon` 独立包
- 远程机器接入德勤工作区
- 提供 long-horizon agent 独立执行环境

---

## 🔧 packages/services/src/clihub/ 核心实现

### `runtime-apps.ts` — 操作路由核心

```ts
export interface RuntimeAppOperationRequestResult {
  operation: RuntimeAppOperationRecord;  // 操作记录
  installPlan: RuntimeAppInstallPlan;    // 安装计划
}

export function requestRuntimeAppOperationSync(input: {
  workspaceId: string;        // 工作区隔离
  runtimeId: string;           // 哪个 daemon
  source: RuntimeAppCatalogSource;  // 来自哪个 registry
  name: string;
  operation: RuntimeAppOperationType;  // install/uninstall/update/enable/disable
  actorUserId?: string;
  confirmHighRisk?: boolean;   // 高风险需要二次确认
}): RuntimeAppOperationRequestResult
```

**核心操作流程**：

```
1. maybeRefreshCliHubCatalogBeforeMutation()  ← 先同步目录
2. assertCanManageRuntimeAppsSync()          ← 权限检查
3. readAgentRuntimeSync(runtimeId)           ← 找 daemon
4. if (runtime.status !== "online") throw   ← 检查 daemon 在线
5. readRuntimeAppCatalogItemSync()           ← 找 catalog 项
6. readCliHubReadinessForRuntimeSync()       ← 检查 cli_hub 状态
7. buildRuntimeAppInstallPlan()              ← 生成安装计划
8. if (risk === "high" && !confirmHighRisk) throw  ← 高风险检查
9. createRuntimeAppOperationSync()          ← 写入操作记录
10. tryRecordWorkspaceAuditEventSync()       ← 审计日志
```

**借鉴德勤 R3 + R7**：
- **R3 执行器抽象层**：清晰的操作流程
- **R7 安全审批**：高风险必须 `confirmHighRisk`
- **审计**：每次操作都有 audit event

### `catalog.ts` — Registry-based 设计

**关键 URL**：
```ts
export const CLIHUB_HARNESS_REGISTRY_URL = 
  "https://hkuds.github.io/CLI-Anything/registry.json";
export const CLIHUB_PUBLIC_REGISTRY_URL = 
  "https://hkuds.github.io/CLI-Anything/public_registry.json";
```

**设计**：
- AgentRouter **不写死** 7 个 runtime（不像 Paperclip 那样硬编码 adapter）
- 而是从**官方 registry URL** 同步 runtime 列表
- 任何新 runtime 只要发布到 registry，AgentSpace 自动支持

**借鉴价值**：**德勤可以借鉴"Registry-based adapter"模式**——不必在德勤源码里写死 4 个 adapter，可以从德勤自家 registry 拉。

### `install-plan.ts` — 风险评估 + 安装策略

**危险命令检测**（`UNSAFE_COMMAND_PATTERN`）：
```regex
/(\||&&|;|`|\$\(|<\(|>\(|\bcurl\b|\bwget\b|\bsudo\b|\bsu\b|
 \bchmod\b|\bchown\b|\bsystemctl\b|\blaunchctl\b|\btee\s+-a\b|
 >>|~\/\.(?:bash|zsh|profile|config))/i
```

**关键词检测（medium risk）**：
```regex
/\b(api key|token|credential|login|account|gui|desktop|
 server running|running|installed locally|local app)\b/i
```

**风险等级**：
- `high` — 含危险命令 OR 涉及凭证关键词 OR `installStrategy === "manual"`
- `medium` — 仅含凭证关键词
- `low` — 其他

**安装策略**：
```ts
strategy = cliHubAvailable 
  ? "cli_hub"      // 默认用 CLI Hub 安装
  : operation === "install"
    ? "pip"        // 不可用时用 pip 安装
    : "cli_hub"
```

**借鉴德勤 R7 安全审批**：
- **正则检测危险命令** → 德勤沙箱应该有的"command whitelist/blacklist"
- **关键词检测凭证泄露风险** → sandbox 应该阻止 prompt 含 "api key" 等
- **3 级风险评估** → 借鉴到德勤 `RuntimeAppInstallPlan`

---

## 📊 AgentSpace vs Paperclip vs 德勤 R3 对比

| 维度 | **AgentSpace** | **Paperclip** | **德勤 R3 借鉴** |
|---|---|---|---|
| **adapter 数量** | 7（hermes/openclaw/codex/claude/gemini/opencode/nanobot）| 13（更多 variant）| 4 起步（h/o/c/claude）|
| **adapter 注册** | Registry URL（动态拉）| 硬编码 `packages/adapters/` | **推荐：Registry + 硬编码双轨** |
| **风险评估** | regex 检测 + risk 等级 | 无（trust based）| **借鉴 AgentSpace** |
| **审计日志** | `tryRecordWorkspaceAuditEventSync()` | 无统一 | **借鉴 AgentSpace** |
| **权限检查** | workspace owner/admin | paperclip 隐含 | **借鉴 AgentSpace** |
| **心跳机制** | `daemon.status === "online"` | 显式 heartbeat | **借鉴 Paperclip** |
| **接口契约** | `RuntimeAppOperationRequestResult` | `AdapterExecutionContext` | **融合两者** |
| **远程执行** | `agent-space-daemon` 独立包 | paperclip-fork 内部 | **借鉴 AgentSpace（更轻）**|

---

## 🎯 AgentRouter 给德勤的 6 大设计原则

```
1. ✅ Registry-based adapter（不写死，可扩展）
2. ✅ Workspace 隔离（每个项目独立）
3. ✅ Risk-aware operation（high risk 二次确认）
4. ✅ Audit-event-driven（每次操作有日志）
5. ✅ Permission-check first（admin/owner 才能改）
6. ✅ Remote daemon 独立可分发（不依赖主仓库）
```

---

## 🐍 德勤 Adapter 6 类方法（借鉴接口）

基于 Paperclip + AgentSpace 融合，德勤执行器抽象层应包含：

```python
class AbstractExecutor(ABC):
    """德勤执行器抽象接口（R3 + R7 融合）"""

    @abstractmethod
    def submit(self, task: Task) -> TaskHandle:
        """提交任务，返回 task_id"""

    @abstractmethod
    def heartbeat(self, task_id: str) -> HeartbeatStatus:
        """查任务状态: pending/running/completed/failed"""

    @abstractmethod
    def logs(self, task_id: str, since: datetime) -> List[LogEntry]:
        """拉取增量日志"""

    @abstractmethod
    def pause(self, task_id: str) -> bool:
        """暂停任务"""

    @abstractmethod
    def resume(self, task_id: str) -> bool:
        """恢复任务"""

    @abstractmethod
    def terminate(self, task_id: str) -> bool:
        """终止任务"""

    # —— AgentSpace 借鉴的安全审计 ——
    @abstractmethod
    def audit_log(self, task_id: str) -> List[AuditEvent]:
        """审计日志（AgentSpace 风格）"""

    # —— Paperclip 借鉴的运行时检查 ——
    def check_runtime_online(self) -> bool:
        """Runtime 在线检查"""
```

---

## ⚠️ Hermes 执行观察（卡在 cc-vibe.com 7 分钟）

```
22:39 - dispatcher claim t_4f8c27c9 ✅
22:43 - dispatcher 标 blocked（任务描述模糊）
23:56 - chat -q 触发，Hermes 写 414 行 LangGraph adapter ✅
00:07 - 异步触发 Hermes 写 4 个 adapter
00:14 - Hermes 卡在 run_agent._interruptible_streaming_api_call
       （cc-vibe.com 第三方代理对 gpt-5.4 streaming 无响应）

# 进程详情
PID 1635247, State: S (sleeping) 
Stack: futex_wait → 线程在等 LLM streaming
```

**结论**：
- Hermes dispatcher ✅ 工作
- Hermes chat ✅ 工作（之前已验证）
- Hermes chat -Q --max-turns 50 大任务 ⚠️ **卡在 cc-vibe.com 第三方代理**
- 解决方法：换 provider 或换模型，或把任务拆小

---

## 📁 下一步行动

| # | 行动 | 时间 |
|---|---|---|
| 1 | 我（OpenClaw）直接写 4 个 adapter（避开 cc-vibe.com 卡住问题）| 30 分钟 |
| 2 | 写德勤 AdapterRouter 7 runtime registry schema | 1 小时 |
| 3 | 写德勤沙箱风险评估（借鉴 UNSAFE_COMMAND_PATTERN）| 2 小时 |
| 4 | 让 Hermes 跑"小任务"测试是否还卡 | 5 分钟 |
| 5 | 安全审查 cc-vibe.com 代理 + OPENAI_API_KEY | 1 小时 |

---

## 🔗 相关文件

- `/root/vault/1-Projects/德勤/AI-Native/笔记/2026-06-29-开源研究部署笔记.md`
- `/root/vault/1-Projects/德勤/AI-Native/executor/langgraph-adapter.py`（Hermes 写的）
- `/root/vault/1-Projects/德勤/AI-Native/笔记/2026-06-29 - 德勤项目完整深度分析报告（hermes 风格）.md`
- Hermes 配置：`~/.hermes/config.yaml`（含 OPENAI_API_KEY + cc-vibe.com 代理）
- Hermes dispatcher 卡住证据：`/proc/1635247/stack`（futex_wait 状态）

---

**作者**：OpenClaw (小助) — 手动接力，因 Hermes 卡在 cc-vibe.com 第三方代理  
**写于**：2026-06-29 00:14  
**PARA 位置**：`1-Projects/德勤/AI-Native/笔记/`