---
title: Agent 管理（profile 注册 + 角色 + Skill 绑定 + 执行器绑定）
date: 2026-07-02
type: implementation-note
project: 德勤 AI-Native
status: active
tags:
  - 德勤
  - AI-Native
  - agent-management
  - hermes-sessions
---

# Agent 管理 MVP

本目录对应 v0.3 文档中“Agent 管理”条目，覆盖：
- Agent profile 注册
- 角色说明
- Skill 绑定
- 执行器绑定
- 状态查看
- `hermes sessions` 集成视图

## 文件

- `profile-schema.json`：Agent profile 最小 schema
- `registry.py`：注册表 CLI，支持 `register/list/show`
- `demo.py`：注册 3 个 Agent（`hermes-chat` / `claude-code` / `langgraph`）并输出结果
- `profiles/*.json`：demo 用 profile 样例
- `registry.db`：demo 运行后生成的 sqlite 数据库

## profile 结构

最小字段：
- `name`
- `role`
- `skills[]`
- `executor.type`
- `owner`
- `provider`
- `session_source`
- `status`

其中：
- `skills[]` 用于绑定 skill 名称
- `executor.type` 与 `/executor` 下 adapter 对齐
- `session_source` 对齐 `hermes sessions list --source <source>`

## CLI

```bash
python3 agents/registry.py register --project-id <project_id> --profile agents/profiles/hermes-chat.json
python3 agents/registry.py list --project-id <project_id>
python3 agents/registry.py show --project-id <project_id> --name hermes-chat
```

## demo

```bash
cd /root/vault/1-Projects/德勤/AI-Native
python3 agents/demo.py
```

demo 会：
1. 初始化 sqlite workspace
2. 写入 3 个 profile
3. 注册 3 个 Agent
4. 为每个 Agent 绑定 owner / skills / executor
5. 调用 `hermes sessions list --source ... --limit 3` 形成“执行可见”视图

## 与 M6 executor 的衔接

当前 registry 不直接调度执行，只做绑定与可见性层：
- `hermes-chat` → `executor/adapters/hermes-chat-adapter.py`
- `claude-code` → `executor/adapters/claude-code-adapter.py`
- `langgraph` → `executor/langgraph-adapter.py`

上层如果要真正派发任务，可直接读取：
- `agents.executor_type`
- profile 中的 `executor.adapter`
- profile 中的 `executor.workspace`

## 验收映射

对应验收点：
- 至少两个 Agent 能被分配任务：当前 demo 注册 3 个 Agent
- 有可查看输出和日志：执行器 adapter 已在 `/executor` 中提供统一日志；本目录补齐 Agent 注册与 session/source 视图
- 执行可见：通过 `hermes sessions` 输出最近 session 列表
