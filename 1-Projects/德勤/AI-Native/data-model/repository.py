from __future__ import annotations

import sqlite3
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any, Iterable
from uuid import uuid4


STATUSES = ("todo", "in_progress", "pending_confirmation", "done")


@dataclass
class Organization:
    id: str
    name: str
    slug: str
    mission: str


@dataclass
class Project:
    id: str
    organization_id: str
    name: str
    slug: str
    goal: str
    status: str
    deliverable_requirements: str


@dataclass
class Member:
    id: str
    organization_id: str
    project_id: str | None
    display_name: str
    role: str
    email: str | None
    kind: str = "human"


@dataclass
class Agent:
    id: str
    project_id: str
    owner_member_id: str | None
    name: str
    provider: str
    executor_type: str
    status: str
    instruction_summary: str | None


@dataclass
class Skill:
    id: str
    project_id: str
    agent_id: str | None
    name: str
    version: str
    source: str
    summary: str | None


@dataclass
class Deliverable:
    id: str
    project_id: str
    task_id: str | None
    name: str
    type: str
    path: str | None
    status: str = "draft"
    acceptance_notes: str | None = None


@dataclass
class Task:
    id: str
    project_id: str
    assignee_member_id: str | None
    agent_id: str | None
    title: str
    description: str | None
    status: str = "todo"
    priority: int = 2
    deliverable_id: str | None = None


@dataclass
class Approval:
    id: str
    project_id: str
    task_id: str | None
    deliverable_id: str | None
    approver_member_id: str | None
    status: str = "pending"
    decision_note: str | None = None
    decided_at: str | None = None


class WorkspaceRepository:
    def __init__(self, db_path: str | Path, schema_path: str | Path):
        self.db_path = Path(db_path)
        self.schema_path = Path(schema_path)
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        self.conn = sqlite3.connect(self.db_path)
        self.conn.row_factory = sqlite3.Row
        self.conn.execute("PRAGMA foreign_keys = ON")
        self._init_schema()

    def close(self) -> None:
        self.conn.close()

    def _init_schema(self) -> None:
        self.conn.executescript(self.schema_path.read_text(encoding="utf-8"))
        self.conn.commit()

    def _insert(self, table: str, values: dict[str, Any]) -> dict[str, Any]:
        cols = ", ".join(values.keys())
        placeholders = ", ".join(f":{k}" for k in values.keys())
        self.conn.execute(f"INSERT INTO {table} ({cols}) VALUES ({placeholders})", values)
        self.conn.commit()
        return values

    def create_organization(self, name: str, slug: str, mission: str) -> Organization:
        record = Organization(id=self._id("org"), name=name, slug=slug, mission=mission)
        self._insert("organizations", asdict(record))
        return record

    def create_project(
        self,
        organization_id: str,
        name: str,
        slug: str,
        goal: str,
        deliverable_requirements: str,
        status: str = "active",
    ) -> Project:
        record = Project(
            id=self._id("proj"),
            organization_id=organization_id,
            name=name,
            slug=slug,
            goal=goal,
            status=status,
            deliverable_requirements=deliverable_requirements,
        )
        self._insert("projects", asdict(record))
        return record

    def create_member(
        self,
        organization_id: str,
        project_id: str | None,
        display_name: str,
        role: str,
        email: str | None = None,
        kind: str = "human",
    ) -> Member:
        record = Member(
            id=self._id("mem"),
            organization_id=organization_id,
            project_id=project_id,
            display_name=display_name,
            role=role,
            email=email,
            kind=kind,
        )
        self._insert("members", asdict(record))
        return record

    def create_agent(
        self,
        project_id: str,
        name: str,
        provider: str,
        executor_type: str,
        owner_member_id: str | None = None,
        status: str = "ready",
        instruction_summary: str | None = None,
    ) -> Agent:
        record = Agent(
            id=self._id("agt"),
            project_id=project_id,
            owner_member_id=owner_member_id,
            name=name,
            provider=provider,
            executor_type=executor_type,
            status=status,
            instruction_summary=instruction_summary,
        )
        self._insert("agents", asdict(record))
        return record

    def create_skill(
        self,
        project_id: str,
        name: str,
        source: str,
        summary: str,
        agent_id: str | None = None,
        version: str = "0.1.0",
    ) -> Skill:
        record = Skill(
            id=self._id("skl"),
            project_id=project_id,
            agent_id=agent_id,
            name=name,
            version=version,
            source=source,
            summary=summary,
        )
        self._insert("skills", asdict(record))
        return record

    def create_deliverable(
        self,
        project_id: str,
        name: str,
        type: str,
        path: str | None = None,
        task_id: str | None = None,
        status: str = "draft",
        acceptance_notes: str | None = None,
    ) -> Deliverable:
        record = Deliverable(
            id=self._id("deliv"),
            project_id=project_id,
            task_id=task_id,
            name=name,
            type=type,
            path=path,
            status=status,
            acceptance_notes=acceptance_notes,
        )
        self._insert("deliverables", asdict(record))
        return record

    def create_task(
        self,
        project_id: str,
        title: str,
        description: str,
        assignee_member_id: str | None = None,
        agent_id: str | None = None,
        status: str = "todo",
        priority: int = 2,
        deliverable_id: str | None = None,
    ) -> Task:
        if status not in STATUSES:
            raise ValueError(f"invalid task status: {status}")
        record = Task(
            id=self._id("task"),
            project_id=project_id,
            assignee_member_id=assignee_member_id,
            agent_id=agent_id,
            title=title,
            description=description,
            status=status,
            priority=priority,
            deliverable_id=deliverable_id,
        )
        self._insert("tasks", asdict(record))
        return record

    def create_approval(
        self,
        project_id: str,
        approver_member_id: str | None,
        task_id: str | None = None,
        deliverable_id: str | None = None,
        status: str = "pending",
        decision_note: str | None = None,
        decided_at: str | None = None,
    ) -> Approval:
        record = Approval(
            id=self._id("appr"),
            project_id=project_id,
            task_id=task_id,
            deliverable_id=deliverable_id,
            approver_member_id=approver_member_id,
            status=status,
            decision_note=decision_note,
            decided_at=decided_at,
        )
        self._insert("approvals", asdict(record))
        return record

    def transition_task(self, task_id: str, new_status: str) -> None:
        if new_status not in STATUSES:
            raise ValueError(f"invalid task status: {new_status}")
        self.conn.execute("UPDATE tasks SET status = ? WHERE id = ?", (new_status, task_id))
        self.conn.commit()

    def set_deliverable_status(self, deliverable_id: str, status: str, note: str | None = None) -> None:
        self.conn.execute(
            "UPDATE deliverables SET status = ?, acceptance_notes = COALESCE(?, acceptance_notes) WHERE id = ?",
            (status, note, deliverable_id),
        )
        self.conn.commit()

    def set_approval_status(self, approval_id: str, status: str, decision_note: str | None = None, decided_at: str | None = None) -> None:
        self.conn.execute(
            "UPDATE approvals SET status = ?, decision_note = ?, decided_at = ? WHERE id = ?",
            (status, decision_note, decided_at, approval_id),
        )
        self.conn.commit()

    def list_project_tasks(self, project_id: str) -> list[sqlite3.Row]:
        sql = """
        SELECT
            t.id,
            t.title,
            t.status,
            t.priority,
            m.display_name AS assignee,
            a.name AS agent_name,
            d.name AS deliverable_name
        FROM tasks t
        LEFT JOIN members m ON m.id = t.assignee_member_id
        LEFT JOIN agents a ON a.id = t.agent_id
        LEFT JOIN deliverables d ON d.id = t.deliverable_id
        WHERE t.project_id = ?
        ORDER BY t.priority ASC, t.created_at ASC
        """
        return list(self.conn.execute(sql, (project_id,)))

    def list_pending_confirmations(self, project_id: str) -> list[sqlite3.Row]:
        return list(
            self.conn.execute(
                "SELECT id, title, status FROM tasks WHERE project_id = ? AND status = 'pending_confirmation' ORDER BY updated_at DESC",
                (project_id,),
            )
        )

    def list_agent_skills(self, agent_id: str) -> list[sqlite3.Row]:
        return list(
            self.conn.execute(
                "SELECT name, version, source FROM skills WHERE agent_id = ? ORDER BY name",
                (agent_id,),
            )
        )

    def list_deliverable_approvals(self, project_id: str) -> list[sqlite3.Row]:
        sql = """
        SELECT
            d.name AS deliverable_name,
            d.status AS deliverable_status,
            a.status AS approval_status,
            m.display_name AS approver,
            a.decision_note
        FROM deliverables d
        LEFT JOIN approvals a ON a.deliverable_id = d.id
        LEFT JOIN members m ON m.id = a.approver_member_id
        WHERE d.project_id = ?
        ORDER BY d.created_at ASC
        """
        return list(self.conn.execute(sql, (project_id,)))

    def counts(self) -> dict[str, int]:
        tables = ["organizations", "projects", "members", "agents", "skills", "tasks", "deliverables", "approvals"]
        return {
            table: self.conn.execute(f"SELECT COUNT(*) FROM {table}").fetchone()[0]
            for table in tables
        }

    @staticmethod
    def _id(prefix: str) -> str:
        return f"{prefix}_{uuid4().hex[:10]}"


def rows_to_dicts(rows: Iterable[sqlite3.Row]) -> list[dict[str, Any]]:
    return [dict(row) for row in rows]
