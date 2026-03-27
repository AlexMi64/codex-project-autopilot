#!/usr/bin/env python3
"""Cross-platform post-write guardrail for .codex-agent."""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path


def find_workspace(start: Path) -> Path:
    current = start.resolve()
    for candidate in [current, *current.parents]:
        if (candidate / ".codex-agent").exists():
            return candidate
    return start.resolve()


def infer_seed_idea(workspace: Path) -> str:
    readme = workspace / "README.md"
    if readme.exists():
        lines = [line.strip() for line in readme.read_text(encoding="utf-8").splitlines() if line.strip()]
        for line in lines:
            if line.startswith("#"):
                title = line.lstrip("#").strip()
                if title and title.lower() not in {"readme", "smoke project"}:
                    return f"Проект: {title}"
                break

    package_json = workspace / "package.json"
    if package_json.exists():
        try:
            data = json.loads(package_json.read_text(encoding="utf-8"))
            name = data.get("name")
            description = data.get("description")
            if description:
                return str(description)
            if name:
                return f"Проект: {name}"
        except json.JSONDecodeError:
            pass

    return f"Проект в папке {workspace.name}"


def main() -> None:
    script_dir = Path(__file__).resolve().parent
    workspace = find_workspace(Path.cwd())

    if not (workspace / ".codex-agent").exists():
        seed_idea = infer_seed_idea(workspace)
        subprocess.run(
            [
                sys.executable,
                str(script_dir / "init_codex_agent.py"),
                "--workspace",
                str(workspace),
                "--idea",
                seed_idea,
            ],
            check=True,
            capture_output=True,
            text=True,
        )
        print(
            "[codex-agent] Recovery bootstrap: локальный .codex-agent был автоматически создан в текущем проекте. "
            "Нужно вернуться к discovery и плану, а не считать реализацию уже корректно запущенной."
        )
        return

    python_cmd = [sys.executable]
    subprocess.run(python_cmd + [str(script_dir / "build_context_bundle.py"), "--workspace", str(workspace)], check=True, capture_output=True, text=True)
    subprocess.run(python_cmd + [str(script_dir / "validate_codex_agent.py"), "--workspace", str(workspace), "--soft-fail"], check=True)
    print(
        "[codex-agent] Guardrail reminder: keep phase-card.md, ultra-context.md, state.json, implementation-plan.md, approval-snapshot.json, env-secrets-checklist.md, and final-handoff.md in sync."
    )


if __name__ == "__main__":
    main()
