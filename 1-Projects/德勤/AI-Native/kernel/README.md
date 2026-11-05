# 德勤 AI Native 调度内核（原型 v0.1）

> 借鉴 [Agent Autoloop](https://github.com/KKKKhazix/agent-autoloop) 的内核纪律，用德勤口径重写。
> **只做四件事**：收事件 → 按规则分活 → 派给 Agent → 记每一步。
> 不碰 Agent 内部、不做模型决策、不做人类学治理。

执行层沿用德勤已有资产（`../executor/`）：`abstract-interface.md`（ExecutorTask / Status / LogEvent）、
`log-schema.json`（统一日志 schema）、`adapters/hermes-chat-adapter.py`。

## 特性

| # | 内核基线 | 实现位置 | 自动验收用例 |
|---|---|---|---|
| 1 | 唯一写入点 + 单事务 | `store.py::Store.apply` | `Baseline1SingleTransaction` |
| 2 | 授权不可变 + 规则版本化 | `rules.py`（version + sha256 digest） | `Baseline2ImmutableAuthorization` |
| 3 | 指令数据分离 + 字段白名单 | `events.py`（白名单/禁字段/提示词拼装） | `Baseline3InstructionDataSeparation` |
| 4 | 跳数熔断（MAX_HOPS=8，链级记忆） | `dispatch.py` + `store.py::chains` | `Baseline4HopMeltdown` |
| 5 | 事件溯源 + 一条命令查清来龙去脉 | `facts` 追加表 + `why` 命令 | `Baseline5AuditTrail` |
| 6 | 核心零出站网络 | 全包仅标准库，AST 扫描拦截网络库 | `Baseline6ZeroOutboundNetwork` |
| 7 | 厂商中立接口 | `AgentSpec{name,use,access,command}` | `Baseline7VendorNeutral` |
| 8 | 首投 observe 灰度 | `rule.mode ∈ {observe,dry,execute}` | `Baseline8ObserveGreyRelease` |

## 目录

```
kernel/
├── agent_kernel/
│   ├── __init__.py     MAX_HOPS = 8
│   ├── events.py       事件规范化、白名单、注入检测
│   ├── rules.py        规则加载、确定性匹配、提示词拼装
│   ├── store.py        SQLite 唯一写入点、单事务、审计事实、链状态
│   ├── dispatch.py     内核：收事件→分活→派活→记每一步
│   ├── executors.py    厂商中立执行器接口（dryrun / command）
│   └── cli.py          命令行
├── tests/test_kernel.py  24 个用例，8 条基线逐条覆盖
└── rules.example.json   示例规则集
```

## 用法

```bash
cd kernel
python3 -m unittest discover -s tests          # 跑全部用例

K="python3 -m agent_kernel.cli"
$K check  --rules rules.example.json --db /tmp/k.db     # 校验规则 + 登记版本
$K ingest --db /tmp/k.db --rules rules.example.json    # 收一条事件（stdin）
$K run    --db /tmp/k.db --rules rules.example.json    # 派活
$K status --db /tmp/k.db                              # 状态
$K why    1 --db /tmp/k.db                             # 审计链
$K sim    --db /tmp/k.db --rules rules.example.json --count 500 --seed 42
```

事件 JSON 格式（**只允许这些字段，多一个就整条拒收**）：

```json
{
  "source": "github",
  "type": "issue.opened",
  "subject": "issue-42",
  "text": "外部自由文本 —— 只落库，不进提示词",
  "refs": ["https://git.example.com/issue/42"],
  "fields": {"repo": "demo", "issue_number": 42}
}
```

禁止字段（出现即拒收并留痕）：`cwd` `agent` `access` `prompt` `skill` `command` `rule` `mode` `group` `hops` `permissions` `escalate` `auto_approve`。

## 已知限制（v0.1）

1. **无 ask/续跑卡片机制**：本原型只做到"派活 + 记账"，人工拍板回路（Autoloop 的 `ask`/`answer`）尚未实现。
2. **无 token/费用统计**：命令执行器拿不到 usage，需要专用 adapter 才能上报（见实跑验证记录的发现）。
3. **规则不支持通配 source**：`when.source` 目前必须全等。
4. **无心跳/看门狗**：只做熔断，不做停滞检测（Watchdog 是 Super-agent 的能力，列入 P1）。
5. **单进程假设**：SQLite 单写者，未做多节点调度。

## 下一步

- P0：补 `ask`/`answer` 卡片回路（人工拍板 → 同链续跑 → 熔断计数 +1）
- P0：接 `hermes-chat-adapter.py`，跑一次真实执行器（带 token 上报）
- P1：Policy/Mandate 治理层（授权不可变 + observe 开关下沉到规则集）
- P1：Watchdog 停滞检测
- P2：多源适配（GitHub / 飞书 / CI）与通道回写
