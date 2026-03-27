#!/usr/bin/env python3
"""Cross-platform post-write guardrail for .codex-agent."""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path


def find_workspace(start: Path) -> Path:
    current = start.resolve()
    for candidate in [current, *current.parents]:
        if (candidate / ".codex-agent").exists():
            return candidate
    return start.resolve()


def main() -> None:
    script_dir = Path(__file__).resolve().parent
    workspace = find_workspace(Path.cwd())

    if not (workspace / ".codex-agent").exists():
        print("[codex-agent] Guardrail reminder: initialize .codex-agent before relying on plan or handoff artifacts.")
        return

    python_cmd = [sys.executable]
    subprocess.run(python_cmd + [str(script_dir / "build_context_bundle.py"), "--workspace", str(workspace)], check=True, capture_output=True, text=True)
    subprocess.run(python_cmd + [str(script_dir / "validate_codex_agent.py"), "--workspace", str(workspace), "--soft-fail"], check=True)
    print(
        "[codex-agent] Guardrail reminder: keep phase-card.md, ultra-context.md, state.json, implementation-plan.md, approval-snapshot.json, env-secrets-checklist.md, and final-handoff.md in sync."
    )


if __name__ == "__main__":
    main()
