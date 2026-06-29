"""
---
title: LangGraph executor adapter（德勤 R3）
date: 2026-06-29
type: code-reference
purpose: 将已跑通的 LangGraph StateGraph demo 搬迁为可读、可复用、可集成的执行器 adapter 参考实现
related:
  - /tmp/deloitte_executor/langgraph_demo.py
  - /root/vault/1-Projects/德勤/AI-Native/笔记/2026-06-29-开源研究部署笔记.md
  - /root/vault/1-Projects/德勤/AI-Native/
---
"""

"""
LangGraph executor adapter（德勤 R3）

这个文件是把已验证可运行的 /tmp/deloitte_executor/langgraph_demo.py
搬迁到项目正式目录后的“文档化参考实现”。

定位：
1. 作为“2 类执行器”里的 LangGraph / StateGraph 后端参考。
2. 用来说明 Hermes chat 执行器、Claude Code adapter 执行器之外，
   还可以如何用显式状态机来组织任务执行。
3. 当前偏重结构说明、状态设计、执行流设计、集成接口说明；
   不追求立即生产可用，而是为后续接入 Hermes / 自研 adapter 提供骨架。

说明：
- 该 demo 已在源文件位置跑通，因此本文件不要求再次执行。
- 保留最小可理解逻辑，同时补充详细注释，方便后续二次改造。
"""

from typing import Annotated, TypedDict

from langgraph.checkpoint.memory import MemorySaver
from langgraph.graph import END, START, StateGraph
from langgraph.graph.message import add_messages


# ============================================================================
# 1. State Schema：定义执行器在图中流转的“统一状态对象”
# ============================================================================
# 这里借鉴的是德勤 R3 对“执行器抽象层”的思路：
# 无论底层具体是 Hermes chat、Claude Code、还是 LangGraph，
# 上层都需要一个统一的任务状态容器，来承载：
# - 任务标识
# - 对话历史
# - 执行步数
# - 上下文
# - 结果与交付物
# - 审批状态
# - 执行日志
#
# LangGraph 的核心价值之一就在于：
# 你可以把这些状态字段显式建模，再通过节点函数逐步修改它。
class DeloitteAgentState(TypedDict):
    """德勤执行器状态定义。"""

    task_id: str
    # Hermes kanban / 调度系统里的任务 id。

    project_id: str
    # 业务项目 id，例如 deloitte-ai-native-mvp。

    messages: Annotated[list, add_messages]
    # 对话或执行消息历史。
    # 使用 add_messages 让 LangGraph 在状态聚合时按“消息语义”追加。
    # 后续如果接 Hermes chat 或 Claude Code，通常也会把执行过程抽象成消息流。

    step_count: int
    # 当前已经执行了多少步，用于调试、可视化与恢复时确认进度。

    context: dict
    # 执行上下文，例如客户信息、阶段、约束、输入参数。

    result: dict
    # 最终结构化结果占位。
    # 当前 demo 中没有深度写入，但生产化时通常会放 summary / status / metrics。

    artifacts: list
    # 交付物列表，例如 markdown 报告、JSON 结果、PPT、代码文件等。

    approvals_needed: bool
    # 是否需要人工审批。
    # 这是咨询/交付型流程里常见的分支点：分析后先 review，再决定是否进入交付。

    execution_log: list
    # 执行日志。
    # 这里用简单字符串模拟；后续可以替换为更结构化的 trace/span/event 日志。


# ============================================================================
# 2. Nodes：定义图里的每个执行步骤
# ============================================================================
# 每个节点本质上就是：
#   输入 state -> 修改 state -> 返回 state
#
# 在生产版里，这些节点可以分别代理到：
# - Hermes chat（文本规划 / 搜索 / 总结）
# - Claude Code adapter（代码生成 / 改文件 / 跑命令）
# - 内部审批系统（等待人工确认）
# - 交付系统（写报告 / 发消息 / 归档）


def research_node(state: DeloitteAgentState) -> DeloitteAgentState:
    """研究节点：模拟前置信息收集 / 调研阶段。"""

    # 每进入一个节点，先累加步数，便于后续追踪整个执行链路。
    state["step_count"] += 1

    # 写入执行日志，模拟 trace event。
    state["execution_log"].append(f"Step {state['step_count']}: research")

    # 追加一条 assistant 消息，表示该阶段完成。
    # 真实集成时，这里通常会放：模型输出、工具调用摘要、检索结论等。
    state["messages"].append(
        {
            "role": "assistant",
            "content": f"[research] 已研究项目 {state['project_id']}",
        }
    )

    return state



def analyze_node(state: DeloitteAgentState) -> DeloitteAgentState:
    """分析节点：模拟在研究基础上形成判断与结论。"""

    state["step_count"] += 1
    state["execution_log"].append(f"Step {state['step_count']}: analyze")
    state["messages"].append(
        {
            "role": "assistant",
            "content": "[analyze] 分析完成",
        }
    )

    # 这里刻意把 approvals_needed 设为 True，
    # 用来展示“分析后进入审批分支”的条件路由能力。
    state["approvals_needed"] = True

    return state



def approval_node(state: DeloitteAgentState) -> DeloitteAgentState:
    """审批节点：模拟人工确认；此处用 auto-approve 代替真实人工审批。"""

    state["step_count"] += 1
    state["execution_log"].append(f"Step {state['step_count']}: approval (auto)")
    state["messages"].append(
        {
            "role": "assistant",
            "content": "[approval] ✓ 已审批",
        }
    )

    # 审批完成后，把标志位切回 False，表示可以继续向后交付。
    state["approvals_needed"] = False

    return state



def deliver_node(state: DeloitteAgentState) -> DeloitteAgentState:
    """交付节点：生成最终交付物元数据。"""

    state["step_count"] += 1
    state["execution_log"].append(f"Step {state['step_count']}: deliver")
    state["messages"].append(
        {
            "role": "assistant",
            "content": "[deliver] 交付物已生成",
        }
    )

    # demo 里仅模拟产生一个报告型 artifact。
    # 后续可以替换为真实的文件输出路径、对象存储地址、消息回执等。
    state["artifacts"].append(
        {
            "type": "report",
            "name": "consulting_report.md",
        }
    )

    # result 字段在这里也可以顺手聚合一个最终摘要，便于上层系统读取。
    state["result"] = {
        "status": "completed",
        "summary": "LangGraph adapter 执行完成，已生成交付物元数据。",
        "artifact_count": len(state["artifacts"]),
    }

    return state


# ============================================================================
# 3. Router：定义条件分支逻辑
# ============================================================================
# LangGraph 的一个关键能力是：
# 节点执行完后，不一定总是走固定边；
# 可以根据 state 动态决定下一个节点。
#
# 本例中：
# analyze 完成后，如果需要审批 -> 走 approval
# 否则 -> 直接走 deliver

def need_approval(state: DeloitteAgentState) -> str:
    """根据状态判断 analyze 后该走哪个分支。"""

    return "approval" if state.get("approvals_needed") else "deliver"


# ============================================================================
# 4. Graph Builder：构建并编译 StateGraph
# ============================================================================
# 这里单独抽成函数，而不是直接在模块顶层拼图，
# 是为了后续更容易被外部系统 import 和复用。
#
# 例如：
# - Hermes chat 里按需 create app
# - 测试代码里单独 build graph
# - 不同环境传入不同 checkpointer

def build_langgraph_app():
    """构建并返回 LangGraph app。"""

    graph = StateGraph(DeloitteAgentState)

    # 4.1 注册节点
    graph.add_node("research", research_node)
    graph.add_node("analyze", analyze_node)
    graph.add_node("approval", approval_node)
    graph.add_node("deliver", deliver_node)

    # 4.2 定义执行边
    graph.add_edge(START, "research")
    graph.add_edge("research", "analyze")

    # 4.3 定义 analyze 之后的条件分支
    graph.add_conditional_edges(
        "analyze",
        need_approval,
        {
            "approval": "approval",
            "deliver": "deliver",
        },
    )

    # 4.4 审批完成后再进入交付
    graph.add_edge("approval", "deliver")

    # 4.5 最终交付结束后进入 END
    graph.add_edge("deliver", END)

    # 4.6 配置 checkpoint
    # 当前使用 MemorySaver，仅保存在内存中。
    # 优点：简单、适合 demo / 本地实验。
    # 缺点：进程退出后状态丢失，不适合生产恢复。
    # 如果后续需要真正的断点恢复，应考虑持久化后端。
    memory = MemorySaver()

    return graph.compile(checkpointer=memory)


# ============================================================================
# 5. Example State Factory：构造一个初始状态样例
# ============================================================================
# 这样做的目的：
# - 便于阅读者快速理解运行这个图需要哪些字段
# - 便于测试代码 / 上层调用方复用统一初始结构

def build_initial_state(
    task_id: str = "t_ebf0bdd6",
    project_id: str = "deloitte-ai-native-mvp",
) -> DeloitteAgentState:
    """构造 demo 用初始状态。"""

    return {
        "task_id": task_id,
        "project_id": project_id,
        "messages": [{"role": "user", "content": "研究德勤 AI Native 项目需求"}],
        "step_count": 0,
        "context": {"client": "德勤", "phase": "MVP"},
        "result": {},
        "artifacts": [],
        "approvals_needed": False,
        "execution_log": [],
    }


# ============================================================================
# 6. Demo Runner：保留一个可独立运行的最小示例入口
# ============================================================================
# 用户本次要求“不需要跑”，但保留 __main__ 入口仍然有价值：
# - 方便后续开发者自己验证
# - 方便与源 demo 对照
# - 方便未来加回归测试

def run_demo():
    """运行最小 demo，并打印关键输出。"""

    print("=" * 60)
    print("LangGraph Demo - 德勤执行器抽象层 StateGraph")
    print("=" * 60)

    print("\n[1] 搭建 StateGraph...")
    app = build_langgraph_app()
    print("✅ StateGraph 编译成功")
    print("   节点：research → analyze → [approval?] → deliver")
    print("   Checkpointer：MemorySaver (in-memory)")

    print("\n[2] 跑测试任务...")
    initial_state = build_initial_state()
    config = {"configurable": {"thread_id": "deloitte-test-001"}}
    result = app.invoke(initial_state, config=config)

    print("\n[3] 执行结果:")
    print(f"   task_id: {result['task_id']}")
    print(f"   step_count: {result['step_count']}")
    print(f"   execution_log: {result['execution_log']}")
    print(f"   artifacts: {result['artifacts']}")
    print(f"   approvals_needed: {result['approvals_needed']}")
    print(f"   result: {result['result']}")

    print("\n[4] 测试 checkpoint 恢复...")
    state_history = list(app.get_state_history(config=config))
    print(f"   checkpoint 数: {len(state_history)}")
    for i, snapshot in enumerate(state_history[:3]):
        print(
            f"   - checkpoint {i}: "
            f"step_count={snapshot.values.get('step_count')}, next={snapshot.next}"
        )

    print("\n" + "=" * 60)
    print("✅ LangGraph Demo 跑通 — 可作为德勤执行器 adapter 的后端")
    print("=" * 60)


# ============================================================================
# 7. 集成示例
# ============================================================================
# 下面给出一个“如何把 LangGraph adapter 集成到 Hermes chat 调用”的示范。
# 这是示意代码，重点在接口边界，而不是立即可运行。
#
# 设计意图：
# - Hermes chat 负责接收用户任务 / 组织上层对话
# - LangGraph adapter 负责把任务拆成显式节点流
# - 某些节点里再回调 Hermes 或 Claude Code adapter 执行具体能力
#
# 也就是说，Hermes chat 不一定直接等于图执行器；
# 它可以是图的“入口层”和“编排层”。

"""
集成示例：把 LangGraph adapter 接到 Hermes chat

示意结构：

    用户消息
        ↓
    Hermes chat / 上层 orchestrator
        ↓
    识别任务类型 = 需要结构化执行流
        ↓
    调用 build_langgraph_app()
        ↓
    app.invoke(initial_state, config={thread_id: ...})
        ↓
    读取 result / artifacts / execution_log
        ↓
    Hermes 再把结果回给用户或写入外部系统

示例伪代码：

    from executor.langgraph_adapter import build_langgraph_app, build_initial_state

    def handle_task_with_langgraph(task_id: str, user_prompt: str):
        app = build_langgraph_app()

        state = build_initial_state(task_id=task_id, project_id="deloitte-ai-native-mvp")
        state["messages"] = [{"role": "user", "content": user_prompt}]
        state["context"].update(
            {
                "entrypoint": "hermes-chat",
                "executor_type": "langgraph",
            }
        )

        config = {
            "configurable": {
                "thread_id": f"hermes-{task_id}",
            }
        }

        result = app.invoke(state, config=config)

        return {
            "task_id": result["task_id"],
            "status": result["result"].get("status"),
            "summary": result["result"].get("summary"),
            "artifacts": result["artifacts"],
            "execution_log": result["execution_log"],
        }

进一步演进方向：
1. 在 research_node / analyze_node 中真正调用 Hermes chat 模型能力。
2. 在 deliver_node 中把 artifact 写入 vault、数据库或消息系统。
3. 把 approval_node 替换成真实的人审 / 飞书 / 微信确认流。
4. 把 MemorySaver 改成持久化 checkpoint，支持中断恢复。
5. 在某些节点中桥接自研 adapter 去调用 Claude Code 完成代码型任务。
"""


if __name__ == "__main__":
    run_demo()
