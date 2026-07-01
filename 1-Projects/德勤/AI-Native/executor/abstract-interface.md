---
title: 执行器抽象接口（德勤 M6 执行与日志）
date: 2026-07-01
type: interface-spec
purpose: 定义 Hermes chat 与 Claude Code 两类执行器的统一抽象边界，满足“至少接入两类执行器并记录输入、状态、失败原因、输出文件”的 MVP 验收
related:
  - /root/vault/1-Projects/德勤/AI-Native/executor/langgraph-adapter.py
  - /root/vault/1-Projects/德勤/AI-Native/executor/log-schema.json
  - /root/vault/1-Projects/德勤/AI-Native/executor/adapters/hermes-chat-adapter.py
  - /root/vault/1-Projects/德勤/AI-Native/executor/adapters/claude-code-adapter.py
---

# 执行器抽象接口（MVP）

本文档定义德勤 AI Native MVP 的“执行器抽象层”。
目标不是一次性做完整调度平台，而是先收敛出一套最小可跑、可换后端、可统一记日志的接口。

当前范围：
- 至少 2 类执行器：Hermes chat、Claude Code adapter
- 统一任务生命周期：提交、心跳、查看日志、暂停、恢复、终止
- 统一日志字段：输入、执行状态、失败原因、输出文件
- 面向 demo 与后续集成，暂不覆盖复杂 trace / 持久化 / 前端展示

---

## 1. 设计目标

上层系统不应该关心底层到底是：
- `hermes chat -q ...`
- `claude -p ...`
- 未来的 LangGraph / OpenHands / 内部 agent runtime

上层只关心：
1. 如何提交任务
2. 如何知道任务还活着
3. 如何查看日志
4. 如何暂停 / 恢复 / 终止
5. 如何拿到结构化结果和输出文件

因此，这里定义统一接口，而把每种执行器差异封装进 adapter。

---

## 2. 核心对象

### 2.1 ExecutorTask

任务对象建议最少包含以下字段：

| 字段 | 类型 | 必填 | 说明 |
|---|---|---:|---|
| `task_id` | string | 否 | 提交后生成；未提交前可为空 |
| `title` | string | 是 | 任务标题，便于日志与 UI 展示 |
| `prompt` | string | 是 | 执行器实际要处理的输入 |
| `executor` | string | 是 | 执行器标识，如 `hermes-chat` / `claude-code` |
| `workspace` | string | 否 | 任务工作目录 |
| `context` | object | 否 | 补充上下文，如项目、阶段、标签 |
| `artifacts_dir` | string | 否 | 产物输出目录 |
| `timeout_seconds` | integer | 否 | 超时阈值 |
| `metadata` | object | 否 | 自定义扩展字段 |

建议约束：
- `prompt` 不为空
- `executor` 必须在注册表中可识别
- `workspace` 与 `artifacts_dir` 最好使用绝对路径

### 2.2 ExecutorStatus

统一状态枚举：

- `queued`：已提交，尚未开始
- `running`：执行中
- `paused`：已暂停
- `succeeded`：执行成功
- `failed`：执行失败
- `terminated`：被主动终止
- `unknown`：无法识别或底层未返回明确状态

### 2.3 LogEvent

日志事件建议遵守 `/root/vault/1-Projects/德勤/AI-Native/executor/log-schema.json`：

- `task_id`
- `executor`
- `started_at`
- `finished_at`
- `status`
- `input`
- `output_files`
- `failure_reason`
- `token_cost`

可选增强字段：
- `event_type`
- `heartbeat_at`
- `raw_output_excerpt`
- `exit_code`
- `duration_ms`

---

## 3. 统一接口定义

以下是上层系统应该依赖的 5 个接口。

### 3.1 `submit(task) -> task_id`

职责：
- 接收标准化任务对象
- 完成底层执行器调用
- 分配统一 `task_id`
- 初始化首条日志记录

输入：
- `ExecutorTask`

输出：
- `task_id: string`

最小行为：
1. 记录任务输入
2. 标记状态为 `queued` 或 `running`
3. 返回可用于后续轮询的任务 id

错误码建议：
- `E_INVALID_TASK`：任务字段不合法
- `E_EXECUTOR_NOT_FOUND`：执行器不存在
- `E_SUBMIT_FAILED`：底层进程启动失败

### 3.2 `heartbeat(task_id) -> status`

职责：
- 查询任务是否仍在活跃执行
- 返回当前统一状态
- 可顺手更新时间戳与最近活动信息

输入：
- `task_id: string`

输出：
- `status: ExecutorStatus`

最小行为：
1. 如果底层进程存在且在运行，返回 `running`
2. 如果任务已完成，返回 `succeeded` / `failed`
3. 如果任务 id 未知，返回 `unknown` 或抛出标准错误

错误码建议：
- `E_TASK_NOT_FOUND`
- `E_HEARTBEAT_FAILED`

### 3.3 `logs(task_id) -> log stream`

职责：
- 返回该任务的结构化日志或可迭代日志流
- 支持查看输入、状态变化、失败原因、输出文件

输入：
- `task_id: string`

输出：
- `list[LogEvent]` 或可流式对象

最小行为：
1. 至少返回最新状态
2. 如果失败，必须能读到 `failure_reason`
3. 如果成功，必须能读到 `output_files`

错误码建议：
- `E_TASK_NOT_FOUND`
- `E_LOG_READ_FAILED`

### 3.4 `pause(task_id) -> status`

职责：
- 尝试暂停任务
- 如果底层执行器不支持真正暂停，也必须显式返回“不支持”或退化策略

输入：
- `task_id: string`

输出：
- `status: ExecutorStatus`

退化策略：
- MVP 可返回 `paused`（逻辑暂停）
- 或返回 `unknown` + 注明当前执行器不支持真实进程冻结

错误码建议：
- `E_TASK_NOT_FOUND`
- `E_PAUSE_UNSUPPORTED`
- `E_PAUSE_FAILED`

### 3.5 `resume(task_id) -> status`

职责：
- 恢复被暂停任务
- 与 `pause` 对应

输入：
- `task_id: string`

输出：
- `status: ExecutorStatus`

错误码建议：
- `E_TASK_NOT_FOUND`
- `E_RESUME_UNSUPPORTED`
- `E_RESUME_FAILED`

### 3.6 `terminate(task_id) -> status`

职责：
- 主动终止任务
- 写入统一失败 / 终止日志

输入：
- `task_id: string`

输出：
- `status: ExecutorStatus`

最小行为：
1. 向底层进程发送终止信号
2. 更新日志 `status=terminated`
3. 保留已有输出与失败信息

错误码建议：
- `E_TASK_NOT_FOUND`
- `E_TERMINATE_FAILED`

---

## 4. 错误模型

建议所有 adapter 统一返回下面这类错误结构：

```json
{
  "error_code": "E_SUBMIT_FAILED",
  "message": "failed to start hermes chat process",
  "retryable": true,
  "details": {
    "executor": "hermes-chat",
    "raw_error": "..."
  }
}
```

字段说明：

| 字段 | 类型 | 说明 |
|---|---|---|
| `error_code` | string | 机器可判定的标准错误码 |
| `message` | string | 人可读说明 |
| `retryable` | boolean | 是否适合重试 |
| `details` | object | 原始错误、命令、退出码等 |

推荐错误码清单：
- `E_INVALID_TASK`
- `E_EXECUTOR_NOT_FOUND`
- `E_SUBMIT_FAILED`
- `E_TASK_NOT_FOUND`
- `E_HEARTBEAT_FAILED`
- `E_LOG_READ_FAILED`
- `E_PAUSE_UNSUPPORTED`
- `E_PAUSE_FAILED`
- `E_RESUME_UNSUPPORTED`
- `E_RESUME_FAILED`
- `E_TERMINATE_FAILED`
- `E_TIMEOUT`
- `E_INTERNAL`

---

## 5. 执行器注册模型

推荐保留一个简单注册表：

```text
executor_name -> adapter instance
```

当前 MVP 注册：
- `hermes-chat`
- `claude-code`

后续可扩展：
- `langgraph`
- `openhands`
- `custom-python-agent`

好处：
- 上层只传 `executor="hermes-chat"`
- 不必知道底层命令、参数差异、mock 策略

---

## 6. 日志最小验收要求

为满足本次德勤验收，任一执行器的单次任务至少要能留下：

1. 任务输入 `input`
2. 当前状态 `status`
3. 失败原因 `failure_reason`（若失败）
4. 输出文件 `output_files`（若成功）
5. 开始 / 结束时间 `started_at`, `finished_at`

这 5 项是本轮 MVP 的最低交付线。

---

## 7. 与 Hermes Proxy 的关系

本任务说明中的“关键：用 hermes proxy”，这里解释为：

- Hermes 作为统一执行入口层 / 网关层
- Hermes chat adapter 封装 Hermes CLI 的任务发起能力
- Claude Code adapter 通过同样的抽象层被调用，从而与 Hermes chat 共享同一套日志与状态口径

也就是说：
- Hermes 是统一入口
- Claude Code 是被桥接的一类执行器
- 统一抽象层负责屏蔽二者差异

---

## 8. MVP 边界

本接口故意不覆盖：
- 完整 trace / span / cost 追踪
- 数据库持久化
- Web 前端状态页
- 多租户权限与审批系统
- 分布式调度

这些属于下一阶段问题，不应在本次 M6 里膨胀。

---

## 9. 对应实现文件

- Hermes chat adapter：`/root/vault/1-Projects/德勤/AI-Native/executor/adapters/hermes-chat-adapter.py`
- Claude Code adapter：`/root/vault/1-Projects/德勤/AI-Native/executor/adapters/claude-code-adapter.py`
- 日志 schema：`/root/vault/1-Projects/德勤/AI-Native/executor/log-schema.json`
- 端到端 demo 报告：`/root/vault/1-Projects/德勤/AI-Native/executor/demo-report.md`

---

## 10. 下一步建议

在不扩大范围的前提下，后续最自然的演进顺序是：
1. 把当前内存态任务注册表替换成持久化存储
2. 给 pause / resume 接入更真实的进程控制
3. 给 output_files 增加 artifact 元数据（大小、类型、路径）
4. 让 Hermes chat adapter 真正走 Hermes gateway / proxy 入口，而不只是 CLI 包装
5. 接入 LangGraph 作为第三类执行器
