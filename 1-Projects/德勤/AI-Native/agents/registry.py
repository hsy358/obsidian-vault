from __future__ import annotations

import importlib.util
import json
import sqlite3
import subprocess
import sys
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any


BASE_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = BASE_DIR.parent
DATA_MODEL_DIR = PROJECT_ROOT / "data-model"
EXECUTOR_DIR = PROJECT_ROOT / "executor"
SCHEMA_PATH = BASE_DIR / "profile-schema.json"
DEFAULT_DB_PATH = BASE_DIR / "registry.db"


spec = importlib.util.spec_from_file_location("workspace_repository", DATA_MODEL_DIR / "repository.py")
if spec is None or spec.loader is None:
    raise RuntimeError("failed to load data-model/repository.py")
repo_module = importlib.util.module_from_spec(spec)
sys.modules[spec.name] = repo_module
spec.loader.exec_module(repo_module)
WorkspaceRepository = repo_module.WorkspaceRepository
rows_to_dicts = repo_module.rows_to_dicts


EXECUTOR_ADAPTERS = {
    "hermes-chat": EXECUTOR_DIR / "adapters" / "hermes-chat-adapter.py",
    "claude-code": EXECUTOR_DIR / "adapters" / "claude-code-adapter.py",
    "langgraph": EXECUTOR_DIR / "langgraph-adapter.py",
}


@dataclass
class RegisteredAgent:
    profile_path: str
    profile: dict[str, Any]
    agent_id: str
    owner_member_id: str | None
    skill_ids: list[str]


class AgentRegistryError(RuntimeError):
    pass


class AgentRegistry:
    def __init__(
        self,
        db_path: str | Path = DEFAULT_DB_PATH,
        schema_path: str | Path = DATA_MODEL_DIR / "schema.sql",
        profile_schema_path: str | Path = SCHEMA_PATH,
    ) -> None:
        self.db_path = Path(db_path)
        self.profile_schema_path = Path(profile_schema_path)
        self.repo = WorkspaceRepository(db_path=self.db_path, schema_path=schema_path)
        self._validate_support_files()

    def close(self) -> None:
        self.repo.close()

    def ensure_workspace(self, organization_name: str, organization_slug: str, mission: str, project_name: str, project_slug: str, goal: str, deliverable_requirements: str) -> tuple[dict[str, Any], dict[str, Any]]:
        org = self.repo.conn.execute(
            "SELECT id, name, slug, mission FROM organizations WHERE slug = ?",
            (organization_slug,),
        ).fetchone()
        if org is None:
            org_obj = self.repo.create_organization(organization_name, organization_slug, mission)
            org = self.repo.conn.execute(
                "SELECT id, name, slug, mission FROM organizations WHERE id = ?",
                (org_obj.id,),
            ).fetchone()

        project = self.repo.conn.execute(
            "SELECT id, organization_id, name, slug, goal, status, deliverable_requirements FROM projects WHERE organization_id = ? AND slug = ?",
            (org["id"], project_slug),
        ).fetchone()
        if project is None:
            project_obj = self.repo.create_project(
                organization_id=org["id"],
                name=project_name,
                slug=project_slug,
                goal=goal,
                deliverable_requirements=deliverable_requirements,
            )
            project = self.repo.conn.execute(
                "SELECT id, organization_id, name, slug, goal, status, deliverable_requirements FROM projects WHERE id = ?",
                (project_obj.id,),
            ).fetchone()

        return dict(org), dict(project)

    def register(self, profile_path: str | Path, project_id: str) -> RegisteredAgent:
        profile_file = Path(profile_path)
        profile = json.loads(profile_file.read_text(encoding="utf-8"))
        self.validate_profile(profile)

        owner = profile["owner"]
        owner_row = self._get_or_create_member(
            organization_id=self._project(project_id)["organization_id"],
            project_id=project_id,
            display_name=owner["member_name"],
            role=owner["member_role"],
            email=owner.get("email"),
        )

        existing_agent = self.repo.conn.execute(
            "SELECT id FROM agents WHERE project_id = ? AND name = ?",
            (project_id, profile["name"]),
        ).fetchone()
        if existing_agent is None:
            agent = self.repo.create_agent(
                project_id=project_id,
                owner_member_id=owner_row["id"],
                name=profile["name"],
                provider=profile["provider"],
                executor_type=profile["executor"]["type"],
                status=profile["status"],
                instruction_summary=profile.get("instruction_summary") or profile.get("description"),
            )
            agent_id = agent.id
        else:
            agent_id = existing_agent["id"]
            self.repo.conn.execute(
                """
                UPDATE agents
                SET owner_member_id = ?,
                    provider = ?,
                    executor_type = ?,
                    status = ?,
                    instruction_summary = ?
                WHERE id = ?
                """,
                (
                    owner_row["id"],
                    profile["provider"],
                    profile["executor"]["type"],
                    profile["status"],
                    profile.get("instruction_summary") or profile.get("description"),
                    agent_id,
                ),
            )
            self.repo.conn.commit()

        skill_ids = self._sync_skills(project_id=project_id, agent_id=agent_id, skills=profile["skills"])
        return RegisteredAgent(
            profile_path=str(profile_file),
            profile=profile,
            agent_id=agent_id,
            owner_member_id=owner_row["id"],
            skill_ids=skill_ids,
        )

    def list_agents(self, project_id: str) -> list[dict[str, Any]]:
        rows = self.repo.conn.execute(
            """
            SELECT
                a.id,
                a.name,
                a.provider,
                a.executor_type,
                a.status,
                a.instruction_summary,
                m.display_name AS owner_name,
                m.role AS owner_role,
                GROUP_CONCAT(s.name, ', ') AS skills
            FROM agents a
            LEFT JOIN members m ON m.id = a.owner_member_id
            LEFT JOIN skills s ON s.agent_id = a.id
            WHERE a.project_id = ?
            GROUP BY a.id, a.name, a.provider, a.executor_type, a.status, a.instruction_summary, m.display_name, m.role
            ORDER BY a.name ASC
            """,
            (project_id,),
        ).fetchall()
        return [dict(row) for row in rows]

    def show_agent(self, project_id: str, agent_name: str) -> dict[str, Any]:
        row = self.repo.conn.execute(
            """
            SELECT
                a.id,
                a.name,
                a.provider,
                a.executor_type,
                a.status,
                a.instruction_summary,
                m.display_name AS owner_name,
                m.role AS owner_role,
                m.email AS owner_email
            FROM agents a
            LEFT JOIN members m ON m.id = a.owner_member_id
            WHERE a.project_id = ? AND a.name = ?
            """,
            (project_id, agent_name),
        ).fetchone()
        if row is None:
            raise AgentRegistryError(f"unknown agent: {agent_name}")

        skills = rows_to_dicts(self.repo.list_agent_skills(row["id"]))
        return {**dict(row), "skills": skills}

    def sessions(self, profile_or_agent: dict[str, Any], limit: int = 5) -> dict[str, Any]:
        """查询执行器的最近 session 列表。如果底层 CLI 不在 PATH，会返回降级信息而不是崩溃。"""
        source = profile_or_agent.get("session_source")
        if not source:
            return {"source": None, "items": [], "note": "session_source not configured"}

        import shutil

        hermes_cli = shutil.which("hermes")
        if hermes_cli is None:
            return {
                "source": source,
                "items": [],
                "note": "hermes CLI not on PATH; skipped real query",
                "degraded": True,
            }

        command = ["hermes", "sessions", "list", "--source", source, "--limit", str(limit)]
        completed = subprocess.run(command, capture_output=True, text=True, check=False)
        return {
            "source": source,
            "command": command,
            "exit_code": completed.returncode,
            "stdout": completed.stdout.strip(),
            "stderr": completed.stderr.strip(),
        }

    def executor_summary(self, profile_or_agent: dict[str, Any]) -> dict[str, Any]:
        executor = profile_or_agent["executor"]
        adapter_path = executor.get("adapter") or str(EXECUTOR_ADAPTERS[executor["type"]])
        return {
            "type": executor["type"],
            "adapter": adapter_path,
            "workspace": executor.get("workspace"),
            "model": executor.get("model"),
            "metadata": executor.get("metadata", {}),
        }

    def validate_profile(self, profile: dict[str, Any]) -> None:
        required = {"name", "role", "skills", "executor", "owner", "provider", "session_source", "status"}
        missing = sorted(required - set(profile.keys()))
        if missing:
            raise AgentRegistryError(f"missing required fields: {', '.join(missing)}")
        if not isinstance(profile["skills"], list):
            raise AgentRegistryError("skills must be a list")
        if profile["executor"]["type"] not in EXECUTOR_ADAPTERS:
            raise AgentRegistryError(f"unsupported executor: {profile['executor']['type']}")
        if not self.profile_schema_path.exists():
            raise AgentRegistryError(f"profile schema missing: {self.profile_schema_path}")

    def _sync_skills(self, project_id: str, agent_id: str, skills: list[str]) -> list[str]:
        existing = self.repo.conn.execute(
            "SELECT id, name FROM skills WHERE project_id = ? AND agent_id = ?",
            (project_id, agent_id),
        ).fetchall()
        existing_by_name = {row["name"]: row["id"] for row in existing}
        skill_ids: list[str] = []
        for skill_name in skills:
            if skill_name in existing_by_name:
                skill_ids.append(existing_by_name[skill_name])
                continue
            skill = self.repo.create_skill(
                project_id=project_id,
                agent_id=agent_id,
                name=skill_name,
                source="hermes-skill",
                summary=f"bound to agent {agent_id}",
            )
            skill_ids.append(skill.id)
        return skill_ids

    def _project(self, project_id: str) -> dict[str, Any]:
        row = self.repo.conn.execute(
            "SELECT id, organization_id, name, slug FROM projects WHERE id = ?",
            (project_id,),
        ).fetchone()
        if row is None:
            raise AgentRegistryError(f"unknown project_id: {project_id}")
        return dict(row)

    def _get_or_create_member(self, organization_id: str, project_id: str, display_name: str, role: str, email: str | None) -> sqlite3.Row:
        row = self.repo.conn.execute(
            "SELECT id, display_name, role, email FROM members WHERE organization_id = ? AND project_id = ? AND display_name = ?",
            (organization_id, project_id, display_name),
        ).fetchone()
        if row is not None:
            return row
        member = self.repo.create_member(
            organization_id=organization_id,
            project_id=project_id,
            display_name=display_name,
            role=role,
            email=email,
        )
        row = self.repo.conn.execute(
            "SELECT id, display_name, role, email FROM members WHERE id = ?",
            (member.id,),
        ).fetchone()
        return row

    def _validate_support_files(self) -> None:
        if not self.profile_schema_path.exists():
            raise AgentRegistryError(f"profile schema missing: {self.profile_schema_path}")
        for executor_type, adapter_path in EXECUTOR_ADAPTERS.items():
            if not adapter_path.exists():
                raise AgentRegistryError(f"adapter missing for {executor_type}: {adapter_path}")


def main() -> None:
    import argparse

    parser = argparse.ArgumentParser(description="Agent registry for Deloitte AI-Native MVP")
    parser.add_argument("command", choices=["register", "list", "show"])
    parser.add_argument("--db", default=str(DEFAULT_DB_PATH))
    parser.add_argument("--project-id")
    parser.add_argument("--profile")
    parser.add_argument("--name")
    args = parser.parse_args()

    registry = AgentRegistry(db_path=args.db)
    try:
        if args.command == "register":
            if not args.project_id or not args.profile:
                raise SystemExit("register requires --project-id and --profile")
            result = registry.register(args.profile, args.project_id)
            print(json.dumps(asdict(result), ensure_ascii=False, indent=2))
        elif args.command == "list":
            if not args.project_id:
                raise SystemExit("list requires --project-id")
            print(json.dumps(registry.list_agents(args.project_id), ensure_ascii=False, indent=2))
        elif args.command == "show":
            if not args.project_id or not args.name:
                raise SystemExit("show requires --project-id and --name")
            print(json.dumps(registry.show_agent(args.project_id, args.name), ensure_ascii=False, indent=2))
    finally:
        registry.close()


if __name__ == "__main__":
    main()
