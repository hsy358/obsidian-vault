from __future__ import annotations

import json
from pathlib import Path

from registry import AgentRegistry, DEFAULT_DB_PATH


BASE_DIR = Path(__file__).resolve().parent
PROFILES_DIR = BASE_DIR / "profiles"
DB_PATH = DEFAULT_DB_PATH


PROFILES = {
    "hermes-chat": {
        "name": "hermes-chat",
        "role": "generalist-builder",
        "description": "负责通用任务执行、项目协作和最小实现交付。",
        "skills": ["hermes-agent", "kanban-worker"],
        "executor": {
            "type": "hermes-chat",
            "adapter": str(BASE_DIR.parent / "executor" / "adapters" / "hermes-chat-adapter.py"),
            "model": "custom/gpt-5.4",
            "workspace": str(BASE_DIR.parent),
            "metadata": {"channel": "cli"}
        },
        "owner": {
            "member_name": "咨询 PM",
            "member_role": "项目经理",
            "email": "pm@example.com"
        },
        "provider": "Hermes",
        "status": "ready",
        "instruction_summary": "负责通用项目推进、任务执行、状态反馈。",
        "session_source": "cli",
        "tags": ["mvp", "generalist"],
        "artifacts_dir": str(BASE_DIR.parent / "executor" / "runtime" / "artifacts" / "hermes-demo")
    },
    "claude-code": {
        "name": "claude-code",
        "role": "coding-agent",
        "description": "负责多文件编码与执行器接入。",
        "skills": ["codex", "requesting-code-review"],
        "executor": {
            "type": "claude-code",
            "adapter": str(BASE_DIR.parent / "executor" / "adapters" / "claude-code-adapter.py"),
            "workspace": str(BASE_DIR.parent),
            "metadata": {"fallback": "mock"}
        },
        "owner": {
            "member_name": "AI 工程师",
            "member_role": "实施工程师",
            "email": "eng@example.com"
        },
        "provider": "Claude Code",
        "status": "ready",
        "instruction_summary": "负责代码实现与验证。",
        "session_source": "cli",
        "tags": ["mvp", "code"],
        "artifacts_dir": str(BASE_DIR.parent / "executor" / "runtime" / "artifacts" / "claude-demo")
    },
    "langgraph": {
        "name": "langgraph",
        "role": "workflow-agent",
        "description": "负责图式工作流与状态编排。",
        "skills": ["autonomous-ai-agents", "systematic-debugging"],
        "executor": {
            "type": "langgraph",
            "adapter": str(BASE_DIR.parent / "executor" / "langgraph-adapter.py"),
            "workspace": str(BASE_DIR.parent),
            "metadata": {"graph_mode": "stateful"}
        },
        "owner": {
            "member_name": "流程架构师",
            "member_role": "方案架构师",
            "email": "arch@example.com"
        },
        "provider": "LangGraph",
        "status": "ready",
        "instruction_summary": "负责多步骤工作流、状态机与流程组合。",
        "session_source": "cli",
        "tags": ["mvp", "workflow"],
        "artifacts_dir": str(BASE_DIR.parent / "executor" / "runtime" / "artifacts" / "langgraph-demo")
    }
}


def write_profiles() -> list[str]:
    PROFILES_DIR.mkdir(parents=True, exist_ok=True)
    written: list[str] = []
    for name, payload in PROFILES.items():
        path = PROFILES_DIR / f"{name}.json"
        path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        written.append(str(path))
    return written


def main() -> None:
    written_profiles = write_profiles()
    registry = AgentRegistry(db_path=DB_PATH)
    try:
        organization, project = registry.ensure_workspace(
            organization_name="Deloitte AI Native Consulting",
            organization_slug="deloitte-ai-native",
            mission="交付一个支持 Agent 注册、角色、Skill、执行器与执行可见性的 AI Native MVP",
            project_name="Agent Management MVP",
            project_slug="agent-management-mvp",
            goal="支持 Agent profile 注册、Skill 绑定、执行器绑定和 sessions 可见",
            deliverable_requirements="至少三个 Agent 注册成功；可 list/show；能看到 executor 与 session source",
        )

        registrations = []
        for profile_path in written_profiles:
            registration = registry.register(profile_path=profile_path, project_id=project["id"])
            profile = registration.profile
            registrations.append(
                {
                    "name": profile["name"],
                    "agent_id": registration.agent_id,
                    "skills": profile["skills"],
                    "executor": registry.executor_summary(profile),
                    "sessions": registry.sessions(profile, limit=3),
                }
            )

        result = {
            "database": str(DB_PATH),
            "organization": organization,
            "project": project,
            "profiles_written": written_profiles,
            "agents": registry.list_agents(project["id"]),
            "registrations": registrations,
            "show_example": registry.show_agent(project["id"], "hermes-chat"),
        }
        print(json.dumps(result, ensure_ascii=False, indent=2))
    finally:
        registry.close()


if __name__ == "__main__":
    main()
