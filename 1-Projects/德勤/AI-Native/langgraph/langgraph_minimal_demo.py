#!/usr/bin/env python3
"""
德勤 AI-Native MVP — LangGraph 最小 Demo
=========================================

何大人 2026-07-06 00:02 让测试已装但未实战的 3 个项目：LangGraph / Langfuse / FastEmbed。

本 demo 演示 LangGraph 核心概念：
- StateGraph：状态机
- Nodes：处理节点
- Edges：流程控制（含条件分支）
- Memory：checkpoint 持久化

**德勤 MVP 价值**：把"组织 / 角色 / 任务"建模成 StateGraph，每个节点 = 一个 Agent 决策。
"""
import os
import sys
import json
from typing import TypedDict, Literal
from datetime import datetime

# ============== 1. LangGraph 基础 ==============
print("=== 1️⃣ LangGraph 基础 ===")
from langgraph.graph import StateGraph, START, END
from langgraph.checkpoint.memory import InMemorySaver

print(f"  ✓ langgraph 已装")
print(f"  ✓ StateGraph + END/START + InMemorySaver import OK")

# ============== 2. 定义 State ==============
print("\n=== 2️⃣ 定义 State ===")


class DeloitteTaskState(TypedDict):
    """德勤 MVP 任务状态。"""
    task: str                    # 任务描述
    assigned_role: str           # 当前处理角色
    result: str                  # 处理结果
    history: list                # 处理历史
    status: Literal["pending", "in_progress", "done", "escalate"]


print("  ✓ DeloitteTaskState（TypedDict）已定义")

# ============== 3. 定义 Nodes（每个节点 = 一个 Agent 角色） ==============
print("\n=== 3️⃣ 定义 Nodes ===")


def receive_task(state: DeloitteTaskState) -> DeloitteTaskState:
    """Step 1: 接收任务（PM 角色）"""
    state["assigned_role"] = "PM"
    state["history"].append({
        "role": "PM", "action": "receive_task",
        "timestamp": datetime.now().isoformat(),
        "task": state["task"][:50]
    })
    state["status"] = "in_progress"
    print(f"  [PM] 接收任务: {state['task'][:60]}")
    return state


def analyze_task(state: DeloitteTaskState) -> DeloitteTaskState:
    """Step 2: 分析任务（Architect 角色）"""
    state["assigned_role"] = "Architect"
    state["history"].append({
        "role": "Architect", "action": "analyze",
        "timestamp": datetime.now().isoformat(),
        "result": f"任务分析: {state['task'][:30]} 涉及3个子任务"
    })
    print(f"  [Architect] 分析任务")
    return state


def implement_task(state: DeloitteTaskState) -> DeloitteTaskState:
    """Step 3: 实现任务（Dev 角色）"""
    state["assigned_role"] = "Developer"
    state["history"].append({
        "role": "Developer", "action": "implement",
        "timestamp": datetime.now().isoformat(),
        "code_lines": 250,
    })
    state["result"] = f"已实现 {state['task'][:30]}"
    print(f"  [Developer] 编写代码")
    return state


def review_task(state: DeloitteTaskState) -> DeloitteTaskState:
    """Step 4: 审核（QA 角色）"""
    state["assigned_role"] = "QA"
    approved = "urgent" not in state["task"].lower()  # 简化判断
    state["history"].append({
        "role": "QA", "action": "review",
        "timestamp": datetime.now().isoformat(),
        "approved": approved,
    })
    state["status"] = "done" if approved else "escalate"
    print(f"  [QA] {'✅ 通过' if approved else '⚠ 上报'}")
    return state


print("  ✓ 4 个 nodes 已定义（PM / Architect / Developer / QA）")

# ============== 4. 条件分支 ==============
print("\n=== 4️⃣ 条件分支（edges）===")


def should_escalate(state: DeloitteTaskState) -> Literal["escalate", "finish"]:
    """判断是否需要上报。"""
    return "escalate" if state["status"] == "escalate" else "finish"


def escalate(state: DeloitteTaskState) -> DeloitteTaskState:
    """上报路径（总监审核）"""
    state["assigned_role"] = "Director"
    state["history"].append({
        "role": "Director", "action": "escalation_review",
        "timestamp": datetime.now().isoformat(),
    })
    state["status"] = "done"
    print(f"  [Director] 紧急审核 → 完成")
    return state


print("  ✓ 条件分支函数已定义")

# ============== 5. 构建 StateGraph ==============
print("\n=== 5️⃣ 构建 StateGraph ===")

workflow = StateGraph(DeloitteTaskState)

# 添加节点
workflow.add_node("receive", receive_task)
workflow.add_node("analyze", analyze_task)
workflow.add_node("implement", implement_task)
workflow.add_node("review", review_task)
workflow.add_node("escalate", escalate)

# 添加边（流程）
workflow.add_edge(START, "receive")
workflow.add_edge("receive", "analyze")
workflow.add_edge("analyze", "implement")
workflow.add_edge("implement", "review")

# 条件分支
workflow.add_conditional_edges(
    "review",
    should_escalate,
    {
        "finish": END,
        "escalate": "escalate"
    }
)
workflow.add_edge("escalate", END)

# 编译 + 加 memory（checkpoint）
memory = InMemorySaver()
app = workflow.compile(checkpointer=memory)
print("  ✓ StateGraph 编译完成 + InMemorySaver 集成")

# ============== 6. 跑 2 个任务对比 ==============
print("\n=== 6️⃣ 跑 2 个任务（验证 graph 工作）===")

# Task 1: 普通任务
print("\n--- Task 1: 普通任务 ---")
result1 = app.invoke(
    {"task": "实现德勤 MVP 的 User Memory 模块", "history": [], "status": "pending",
     "assigned_role": "", "result": ""},
    config={"configurable": {"thread_id": "task-1"}}
)
print(f"  → 最终状态: {result1['status']} (assigned to {result1['assigned_role']})")
print(f"  → Result: {result1['result']}")

# Task 2: 紧急任务（会触发 escalate 路径）
print("\n--- Task 2: 紧急任务 ---")
result2 = app.invoke(
    {"task": "URGENT: 修复生产环境 AgentSpace 登录 bug", "history": [], "status": "pending",
     "assigned_role": "", "result": ""},
    config={"configurable": {"thread_id": "task-2"}}
)
print(f"  → 最终状态: {result2['status']} (assigned to {result2['assigned_role']})")
print(f"  → History length: {len(result2['history'])}")

# ============== 7. Memory / Checkpoint 验证 ==============
print("\n=== 7️⃣ Checkpoint 验证 ===")
state = app.get_state({"configurable": {"thread_id": "task-1"}})
print(f"  ✓ task-1 state 重新加载 OK: status={state.values.get('status')}")

# ============== 8. 输出总结 ==============
print("\n=== 8️⃣ 输出总结 ===")
print("  ✓ LangGraph 最小 workflow 跑通")
print("  ✓ StateGraph + 5 nodes + 条件分支 + checkpoint 都工作")
print("  ✓ 德勤 MVP 可直接套用（每个 node = 一个 Agent 角色）")

# 写一个 graph 可视化
graph_viz = {
    "nodes": ["receive", "analyze", "implement", "review", "escalate", "END"],
    "edges": [
        ("START", "receive"),
        ("receive", "analyze"),
        ("analyze", "implement"),
        ("implement", "review"),
        ("review", "END", "if approved"),
        ("review", "escalate", "if not approved"),
        ("escalate", "END"),
    ],
    "demo_results": {
        "task-1": {"status": result1["status"], "final_role": result1["assigned_role"]},
        "task-2": {"status": result2["status"], "final_role": result2["assigned_role"]},
    },
}
summary_path = "/root/vault/1-Projects/德勤/AI-Native/langgraph/langgraph_demo_result.json"
os.makedirs(os.path.dirname(summary_path), exist_ok=True)
with open(summary_path, "w", encoding="utf-8") as f:
    json.dump(graph_viz, f, indent=2, ensure_ascii=False)
print(f"  ✓ Graph 可视化: {summary_path}")

print("\n=== 🎉 LangGraph 测试完成 ===")
print("\n下一步：")
print("  1. 把 Hermes adapter 接入 LangGraph（用 StateGraph 包装）")
print("  2. 把每个 node 接到 Paperclip 的 agent（PM → paperclip PM agent）")
print("  3. 加可视化（LangGraph Studio 或自研 React Flow）")