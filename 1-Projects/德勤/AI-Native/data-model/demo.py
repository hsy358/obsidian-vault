from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path

from repository import WorkspaceRepository, rows_to_dicts


BASE_DIR = Path(__file__).resolve().parent
DB_PATH = BASE_DIR / "workspace-demo.db"
SCHEMA_PATH = BASE_DIR / "schema.sql"


def main() -> None:
    if DB_PATH.exists():
        DB_PATH.unlink()

    repo = WorkspaceRepository(DB_PATH, SCHEMA_PATH)
    validation_conn = None
    try:
        org = repo.create_organization(
            name="Deloitte AI Native Consulting",
            slug="deloitte-ai-native",
            mission="交付一个可管理组织、项目、成员与 Agent 的 AI Native Workspace MVP",
        )
        project = repo.create_project(
            organization_id=org.id,
            name="Workspace MVP Sprint 1",
            slug="workspace-mvp-s1",
            goal="支撑项目空间创建、成员维护、任务流转、交付物确认",
            deliverable_requirements="需要录入目标、成员、Agent 与交付要求；支持待执行→执行中→待确认→已完成",
        )

        sponsor = repo.create_member(org.id, project.id, "何大人", "项目发起人", "he@example.com")
        pm = repo.create_member(org.id, project.id, "咨询 PM", "项目经理", "pm@example.com")
        engineer = repo.create_member(org.id, project.id, "AI 工程师", "实施工程师", "eng@example.com")

        planner = repo.create_agent(
            project_id=project.id,
            owner_member_id=pm.id,
            name="workspace-planner",
            provider="Hermes",
            executor_type="kanban-worker",
            instruction_summary="负责拆解需求、维护任务状态和协作上下文",
        )
        builder = repo.create_agent(
            project_id=project.id,
            owner_member_id=engineer.id,
            name="workspace-builder",
            provider="Claude Code",
            executor_type="coding-agent",
            instruction_summary="负责数据模型、Repository 和 demo 落地",
        )

        repo.create_skill(project.id, "project-breakdown", "hermes-skill", "项目拆卡与状态流转", planner.id)
        repo.create_skill(project.id, "sqlite-repository", "custom", "轻量 sqlite3 + dataclass 持久层", builder.id)

        deliverable = repo.create_deliverable(
            project_id=project.id,
            name="Sprint 1 数据模型包",
            type="data-model",
            path=str(BASE_DIR),
            status="draft",
        )

        task_1 = repo.create_task(
            project_id=project.id,
            title="创建项目 Workspace",
            description="创建组织、项目空间并录入目标与交付要求",
            assignee_member_id=pm.id,
            agent_id=planner.id,
            status="todo",
            priority=0,
        )
        task_2 = repo.create_task(
            project_id=project.id,
            title="录入成员与 Agent",
            description="维护 3 个成员与 2 个 Agent 档案",
            assignee_member_id=engineer.id,
            agent_id=builder.id,
            status="todo",
            priority=1,
        )
        task_3 = repo.create_task(
            project_id=project.id,
            title="提交数据模型交付物",
            description="产出 schema.sql / schema.md / repository.py / demo.py 并进入确认",
            assignee_member_id=engineer.id,
            agent_id=builder.id,
            status="todo",
            priority=2,
            deliverable_id=deliverable.id,
        )

        repo.transition_task(task_1.id, "in_progress")
        repo.transition_task(task_1.id, "done")
        repo.transition_task(task_2.id, "in_progress")
        repo.transition_task(task_2.id, "done")
        repo.transition_task(task_3.id, "in_progress")
        repo.set_deliverable_status(deliverable.id, "submitted", "已提交数据模型初版，等待项目发起人确认")
        repo.transition_task(task_3.id, "pending_confirmation")

        approval = repo.create_approval(
            project_id=project.id,
            task_id=task_3.id,
            deliverable_id=deliverable.id,
            approver_member_id=sponsor.id,
            status="pending",
        )

        before = {
            "counts": repo.counts(),
            "tasks": rows_to_dicts(repo.list_project_tasks(project.id)),
            "pending_confirmation": rows_to_dicts(repo.list_pending_confirmations(project.id)),
            "agent_skills": rows_to_dicts(repo.list_agent_skills(builder.id)),
            "deliverable_approvals": rows_to_dicts(repo.list_deliverable_approvals(project.id)),
        }

        repo.set_approval_status(
            approval.id,
            status="approved",
            decision_note="结构满足 Sprint 1 MVP，允许进入已完成",
            decided_at=datetime.now(timezone.utc).isoformat(),
        )
        repo.set_deliverable_status(deliverable.id, "approved", "项目发起人已确认")
        repo.transition_task(task_3.id, "done")

        after = {
            "counts": repo.counts(),
            "tasks": rows_to_dicts(repo.list_project_tasks(project.id)),
            "pending_confirmation": rows_to_dicts(repo.list_pending_confirmations(project.id)),
            "deliverable_approvals": rows_to_dicts(repo.list_deliverable_approvals(project.id)),
        }

        validation_conn = repo.conn.__class__(DB_PATH)
        validation_conn.execute("PRAGMA foreign_keys = ON")
        validation = {
            "foreign_keys": validation_conn.execute("PRAGMA foreign_keys").fetchone()[0],
            "tables": [
                row[0]
                for row in validation_conn.execute(
                    "SELECT name FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%' ORDER BY name"
                )
            ],
            "triggers": [
                row[0]
                for row in validation_conn.execute(
                    "SELECT name FROM sqlite_master WHERE type='trigger' ORDER BY name"
                )
            ],
        }

        result = {
            "database": str(DB_PATH),
            "organization": org.name,
            "project": project.name,
            "before_approval": before,
            "after_approval": after,
            "validation": validation,
        }
        print(json.dumps(result, ensure_ascii=False, indent=2))
    finally:
        repo.close()
        if validation_conn is not None:
            validation_conn.close()


if __name__ == "__main__":
    main()
