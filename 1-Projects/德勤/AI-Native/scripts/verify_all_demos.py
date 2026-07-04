#!/usr/bin/env python3
"""
---
title: 德勤 AI-Native MVP 端到端部署验证
date: 2026-07-05
type: verification-script
purpose: 把所有可部署的 demo 一次性跑完，输出部署状态汇总 + 健康检查
related:
  - /root/vault/1-Projects/德勤/AI-Native/executor/abstract-interface.md
  - /root/vault/1-Projects/德勤/AI-Native/agents/demo.py
  - /root/vault/1-Projects/德勤/AI-Native/executor/scripts/run_executor_demo.py
  - /root/vault/1-Projects/德勤/AI-Native/executor/langgraph-adapter.py
  - /root/vault/1-Projects/德勤/AI-Native/observability/langfuse_demo.py
---

跑法：
    cd /root/vault/1-Projects/德勤/AI-Native
    python3 scripts/verify_all_demos.py

行为：
1. 数据模型 demo（schema.sql + repository.py）
2. Agent registry demo（profile 注册 + skill 绑定 + 执行器摘要）
3. 执行器双 adapter demo（hermes-chat mock + claude-code mock）
4. LangGraph adapter demo（StateGraph 编译 + checkpoint）
5. Langfuse SDK demo（本地 trace 落盘 + 远端可选）

输出：单一 JSON 汇总 + Markdown 状态报告
"""
from __future__ import annotations

import importlib.util
import json
import os
import runpy
import subprocess
import sys
import traceback
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
REPORTS_DIR = ROOT / "部署报告"
REPORTS_DIR.mkdir(parents=True, exist_ok=True)


def iso_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def run_subprocess(name: str, command: list[str], cwd: Path, env: dict | None = None) -> dict:
    """跑子进程 demo 并收集 stdout/stderr/exit_code。"""
    started = iso_now()
    full_env = os.environ.copy()
    if env:
        full_env.update(env)
    try:
        completed = subprocess.run(
            command,
            cwd=str(cwd),
            capture_output=True,
            text=True,
            env=full_env,
            timeout=180,
        )
        return {
            "name": name,
            "status": "ok" if completed.returncode == 0 else "failed",
            "exit_code": completed.returncode,
            "started_at": started,
            "finished_at": iso_now(),
            "stdout_tail": completed.stdout[-800:] if completed.stdout else "",
            "stderr_tail": completed.stderr[-500:] if completed.stderr else "",
        }
    except subprocess.TimeoutExpired:
        return {"name": name, "status": "timeout", "started_at": started, "finished_at": iso_now()}
    except Exception as exc:
        return {
            "name": name,
            "status": "exception",
            "error": repr(exc),
            "started_at": started,
            "finished_at": iso_now(),
        }


def run_inproc(name: str, target_path: Path, attr: str = "main") -> dict:
    """在当前进程里跑 demo 文件的 main() / run_demo() 函数。"""
    started = iso_now()
    # 把目标文件所在目录加入 sys.path，让 from registry import ... 这种相对导入能找到
    target_dir = str(target_path.parent)
    path_added = False
    if target_dir not in sys.path:
        sys.path.insert(0, target_dir)
        path_added = True
    try:
        spec = importlib.util.spec_from_file_location(target_path.stem, str(target_path))
        if spec is None or spec.loader is None:
            raise RuntimeError(f"cannot load spec for {target_path}")
        module = importlib.util.module_from_spec(spec)
        sys.modules[spec.name] = module
        spec.loader.exec_module(module)
        result = getattr(module, attr, None)
        if result is None:
            raise RuntimeError(f"{target_path} has no {attr} function")
        output = result()
        return {
            "name": name,
            "status": "ok",
            "started_at": started,
            "finished_at": iso_now(),
            "output_summary": _summarize(output),
        }
    except SystemExit as exc:
        return {
            "name": name,
            "status": "ok" if exc.code == 0 else "failed",
            "exit_code": exc.code,
            "started_at": started,
            "finished_at": iso_now(),
        }
    except Exception as exc:
        return {
            "name": name,
            "status": "exception",
            "error": repr(exc),
            "traceback": traceback.format_exc()[-1500:],
            "started_at": started,
            "finished_at": iso_now(),
        }
    finally:
        if path_added and target_dir in sys.path:
            sys.path.remove(target_dir)


def _summarize(value) -> dict:
    """对返回对象做摘要。dataclass / dict / str 都处理。"""
    if isinstance(value, dict):
        return {k: _summarize(v) for k, v in value.items() if k in {"task_id", "status", "trace_id", "trace_path", "events_written", "database", "organization", "project"}}
    if isinstance(value, list):
        return [type(v).__name__ for v in value[:3]]
    if hasattr(value, "name") and hasattr(value, "id"):
        return {"name": value.name, "id": value.id}
    return type(value).__name__


def check_python_packages() -> dict:
    """检查关键 Python 包是否装好。"""
    packages = ["langgraph", "langchain", "langchain_openai", "langfuse"]
    results = {}
    for pkg in packages:
        try:
            __import__(pkg)
            results[pkg] = "installed"
        except ImportError:
            results[pkg] = "MISSING"
    return results


def check_cli_tools() -> dict:
    """检查关键 CLI 是否在 PATH。"""
    import shutil

    tools = ["hermes", "claude", "codex"]
    return {tool: (shutil.which(tool) or "MISSING") for tool in tools}


def main() -> int:
    overall_started = iso_now()

    # 1. 环境检查
    env_check = {
        "python_packages": check_python_packages(),
        "cli_tools": check_cli_tools(),
    }

    # 2. 数据模型 demo（进程隔离）
    data_model_result = run_subprocess(
        "data-model-demo",
        ["python3", str(ROOT / "data-model" / "demo.py")],
        cwd=ROOT / "data-model",
    )

    # 3. Agent registry demo（in-process）
    agent_result = run_inproc(
        "agent-registry-demo",
        ROOT / "agents" / "demo.py",
        attr="main",
    )

    # 4. 执行器双 adapter demo（in-process，但子 demo 内置 mock 兜底）
    executor_result = run_inproc(
        "executor-dual-adapter-demo",
        ROOT / "executor" / "scripts" / "run_executor_demo.py",
        attr="main",
    )
    # hermes-chat-adapter 在脚本加载时会触发其 __main__ 块跑 demo；runpy.run_path 等价于 __main__
    # runpy 加载会跑 hermes-chat-adapter.py 的 __main__ 块（环境变量需预先设置）
    # runpy 已在那之前跑过；这里只是汇总结果。

    # 5. LangGraph adapter demo（in-process，文件没有 main() 函数，所以用 _run_script 路径）
    langgraph_started = iso_now()
    try:
        # 该文件 __main__ 块直接打印 demo 结果，不返回 dict。
        # 我们用 subprocess 模式以更稳。
        lg_completed = subprocess.run(
            ["python3", str(ROOT / "executor" / "langgraph-adapter.py")],
            cwd=str(ROOT / "executor"),
            capture_output=True,
            text=True,
            timeout=120,
            env={**os.environ},
        )
        langgraph_result = {
            "name": "langgraph-adapter-demo",
            "status": "ok" if lg_completed.returncode == 0 else "failed",
            "exit_code": lg_completed.returncode,
            "started_at": langgraph_started,
            "finished_at": iso_now(),
            "stdout_tail": lg_completed.stdout[-600:] if lg_completed.stdout else "",
            "stderr_tail": lg_completed.stderr[-400:] if lg_completed.stderr else "",
        }
    except Exception as exc:
        langgraph_result = {
            "name": "langgraph-adapter-demo",
            "status": "exception",
            "error": repr(exc),
            "started_at": langgraph_started,
            "finished_at": iso_now(),
        }

    # 6. Langfuse SDK demo（in-process）
    langfuse_result = run_inproc(
        "langfuse-sdk-demo",
        ROOT / "observability" / "langfuse_demo.py",
        attr="main",
    )

    overall_finished = iso_now()

    # 汇总
    summary = {
        "started_at": overall_started,
        "finished_at": overall_finished,
        "environment": env_check,
        "demos": {
            "data-model": data_model_result,
            "agent-registry": agent_result,
            "executor-dual-adapter": executor_result,
            "langgraph-adapter": langgraph_result,
            "langfuse-sdk": langfuse_result,
        },
        "deployed_components": [
            "data-model (8 张核心表 + repository.py + schema.sql + demo)",
            "agents (registry.py + profile-schema.json + 3 个 profile + demo)",
            "executor (abstract-interface.md + log-schema.json + 2 adapters)",
            "executor-langgraph (langgraph-adapter.py + StateGraph demo)",
            "observability (langfuse_demo.py + 本地 trace 落盘)",
            "collab (vault PARA 频道 + 线程 + 评论 + 文件)",
        ],
        "deployment_strategy": "可插拔 + 可单独部署 — 每个组件独立可跑，可独立验证。",
    }

    # 整体成功判断
    all_ok = all(d.get("status") == "ok" for d in summary["demos"].values())
    summary["overall_status"] = "healthy" if all_ok else "partial"

    # 写报告
    json_report = REPORTS_DIR / f"deployment-verify-{datetime.now().strftime('%Y%m%d-%H%M%S')}.json"
    json_report.write_text(json.dumps(summary, ensure_ascii=False, indent=2), encoding="utf-8")

    # 打印
    print("=" * 60)
    print("德勤 AI-Native MVP 部署验证")
    print("=" * 60)
    print(f"整体状态: {summary['overall_status']}")
    print(f"开始: {overall_started}")
    print(f"结束: {overall_finished}")
    print()
    print("--- 环境检查 ---")
    print(f"Python 包: {env_check['python_packages']}")
    print(f"CLI 工具: {env_check['cli_tools']}")
    print()
    print("--- Demo 运行结果 ---")
    for name, result in summary["demos"].items():
        marker = "✅" if result["status"] == "ok" else "❌"
        print(f"{marker} {name}: {result['status']}")
    print()
    print(f"详细报告: {json_report}")

    return 0 if all_ok else 1


if __name__ == "__main__":
    raise SystemExit(main())