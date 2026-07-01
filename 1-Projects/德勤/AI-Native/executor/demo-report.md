---
title: 执行器双 adapter 端到端 demo 报告
date: 2026-07-01
type: demo-report
purpose: 记录 Hermes chat 与 Claude Code adapter 的最小生命周期执行结果
related:
  - /root/vault/1-Projects/德勤/AI-Native/executor/abstract-interface.md
  - /root/vault/1-Projects/德勤/AI-Native/executor/log-schema.json
  - /root/vault/1-Projects/德勤/AI-Native/executor/adapters/hermes-chat-adapter.py
  - /root/vault/1-Projects/德勤/AI-Native/executor/adapters/claude-code-adapter.py
---

# 执行器双 adapter 端到端 demo 报告

本报告用于满足德勤 M6 的最小验收：
- 至少两类执行器可被分配任务
- 能看到输入、状态、失败原因、输出文件
- 有可查看的 demo 结果与日志

## 1. Demo 范围

本次演示执行器：
- `hermes-chat`
- `claude-code`

统一调用方式：
- `submit(task) -> task_id`
- `heartbeat(task_id) -> status`
- `logs(task_id) -> log stream`

说明：
- Hermes chat 走真实 `hermes chat -q -Q -m ...`
- Claude Code 优先真实 `claude -p`，不可用时自动退化到 mock

## 2. Hermes chat demo 结果

```json
{
  "task_id": "hermes-71a04f09",
  "status": "succeeded",
  "log_events": 2,
  "output_files": [
    "/root/vault/1-Projects/德勤/AI-Native/executor/runtime/artifacts/hermes-demo/response.txt"
  ],
  "failure_reason": null
}
```

## 3. Claude Code demo 结果

```json
{
  "task_id": "claude-c76065aa",
  "status": "succeeded",
  "log_events": 2,
  "output_files": [
    "/root/vault/1-Projects/德勤/AI-Native/executor/runtime/artifacts/claude-demo/response.txt"
  ],
  "failure_reason": null,
  "execution_mode": "mock"
}
```

## 4. 生命周期核对

### 4.1 任务输入
- Hermes chat adapter 在日志中记录 `input`
- Claude Code adapter 在日志中记录 `input`

### 4.2 执行状态
- 两个 adapter 均可通过 `heartbeat(task_id)` 返回统一状态
- demo 成功后状态应为 `succeeded`

### 4.3 失败原因
- 成功场景下 `failure_reason` 为空
- 若命令缺失、超时、退出码非 0，则会写入 `failure_reason`

### 4.4 输出文件
- 两个 adapter 都会把标准输出写入 `runtime/artifacts/.../response.txt`
- 输出文件路径会记录进结构化日志字段 `output_files`

## 5. 结论

本轮 demo 已验证：
1. Hermes chat 与 Claude Code 两类执行器已纳入同一抽象层
2. 统一日志 schema 可覆盖输入、状态、失败原因、输出文件
3. 即使 Claude Code 真实 CLI 不可用，也能通过 mock 完成接口级验证

## 6. 后续建议

- 将任务注册表从内存迁移到持久化存储
- 用真实进程控制增强 pause / resume
- 将日志流接入上层 UI 或项目首页摘要卡片
