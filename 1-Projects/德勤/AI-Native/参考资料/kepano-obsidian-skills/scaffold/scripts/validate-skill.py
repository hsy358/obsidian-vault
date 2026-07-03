#!/usr/bin/env python3
"""validate-skill.py — 扫 hesiyan/agent-skills 仓库所有 skills/*/SKILL.md，校验 frontmatter 合规。

按 Agent Skills spec 要求每个 SKILL.md 必须有：
  - name (kebab-case)
  - description (含 "Use when ..." 触发条件)
  - H1 标题（# Skill Name）

用法：
  python3 validate-skill.py [--strict] [/path/to/skills]
"""

import argparse
import re
import sys
from pathlib import Path

import yaml


NAME_RE = re.compile(r"^[a-z][a-z0-9-]*$")  # kebab-case

def parse_frontmatter(path: Path) -> tuple[dict | None, str | None]:
    text = path.read_text(encoding="utf-8")
    if not text.startswith("---\n"):
        return None, "missing frontmatter delimiter (---)"
    try:
        end = text.index("\n---\n", 4)
    except ValueError:
        return None, "missing closing frontmatter delimiter"
    yaml_text = text[4:end]
    try:
        meta = yaml.safe_load(yaml_text) or {}
    except yaml.YAMLError as exc:
        return None, f"YAML parse error: {exc}"
    body = text[end + 5 :]
    return meta, body

def validate_one(skill_dir: Path, strict: bool = False) -> list[str]:
    errors: list[str] = []
    skill_md = skill_dir / "SKILL.md"
    if not skill_md.exists():
        return [f"  ❌ {skill_dir.name}: missing SKILL.md"]

    meta, body = parse_frontmatter(skill_md)
    if meta is None:
        return [f"  ❌ {skill_dir.name}: {body}"]

    name = meta.get("name")
    desc = meta.get("description")

    if not name:
        errors.append(f"  ❌ {skill_dir.name}: frontmatter missing 'name'")
    elif not isinstance(name, str):
        errors.append(f"  ❌ {skill_dir.name}: 'name' must be string")
    elif not NAME_RE.match(name):
        errors.append(f"  ❌ {skill_dir.name}: 'name' must be kebab-case ({name!r})")

    if not desc:
        errors.append(f"  ❌ {skill_dir.name}: frontmatter missing 'description'")
    elif not isinstance(desc, str):
        errors.append(f"  ❌ {skill_dir.name}: 'description' must be string")
    elif "Use when" not in desc and "use when" not in desc.lower():
        if strict:
            errors.append(f"  ⚠️  {skill_dir.name}: description missing 'Use when ...' (trigger condition)")

    # H1 check
    first_line = body.lstrip().split("\n", 1)[0].strip()
    if not first_line.startswith("# "):
        if strict:
            errors.append(f"  ⚠️  {skill_dir.name}: missing H1 title (should start with '# Skill Name')")

    return errors

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("skills_dir", nargs="?", default="skills")
    parser.add_argument("--strict", action="store_true", help="also enforce 'Use when' trigger and H1")
    args = parser.parse_args()

    skills_dir = Path(args.skills_dir)
    if not skills_dir.exists():
        print(f"❌ {skills_dir} not found")
        sys.exit(1)

    skill_dirs = sorted(p for p in skills_dir.iterdir() if p.is_dir())
    if not skill_dirs:
        print(f"⚠️  no skills in {skills_dir}")
        sys.exit(0)

    print(f"Validating {len(skill_dirs)} skill(s) in {skills_dir}\n")
    all_errors = []
    for sd in skill_dirs:
        errors = validate_one(sd, strict=args.strict)
        if not errors:
            print(f"  ✓ {sd.name}")
        all_errors.extend(errors)

    print("")
    if all_errors:
        print(f"❌ {len(all_errors)} issue(s) found")
        for e in all_errors:
            print(e)
        sys.exit(1)
    else:
        print(f"✅ All {len(skill_dirs)} skill(s) pass validation")

if __name__ == "__main__":
    main()
