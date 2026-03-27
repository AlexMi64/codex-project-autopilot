#!/usr/bin/env python3
"""Move .codex-agent to the next phase with plan locking when needed."""

from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path

from codex_agent_common import (
    PHASES,
    can_transition_phase,
    freeze_approval_snapshot,
    load_state,
    merge_state_defaults,
    save_state,
    state_dir,
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Перевести .codex-agent в новую фазу и при необходимости заморозить план.")
    parser.add_argument("--workspace", default=".", help="Корень workspace.")
    parser.add_argument("--phase", required=True, choices=PHASES, help="Новая фаза проекта.")
    parser.add_argument("--approve-plan", action="store_true", help="Отметить план как утвержденный и заморозить его.")
    parser.add_argument("--force", action="store_true", help="Разрешить нетипичный переход между фазами.")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    workspace = Path(args.workspace).expanduser().resolve()
    if not state_dir(workspace).exists():
        raise SystemExit(f".codex-agent не найден в {workspace}")

    state = load_state(workspace)
    current_phase = state.get("phase", "discovery")
    if not can_transition_phase(current_phase, args.phase, force=args.force):
        raise SystemExit(f"Нельзя перейти из фазы '{current_phase}' в '{args.phase}' без --force")

    state["phase"] = args.phase
    if args.approve_plan:
        state["approval_status"] = "approved"

    state = merge_state_defaults(state, workspace, phase=args.phase)

    if args.approve_plan or (args.phase in {"execution", "verification", "handoff"} and state.get("approval_status") == "approved"):
        freeze_approval_snapshot(workspace, state)

    save_state(workspace, state)

    script_dir = Path(__file__).resolve().parent
    subprocess.run([sys.executable, str(script_dir / "build_context_bundle.py"), "--workspace", str(workspace)], check=True, capture_output=True, text=True)
    subprocess.run([sys.executable, str(script_dir / "validate_codex_agent.py"), "--workspace", str(workspace)], check=True, capture_output=True, text=True)

    print(f"phase={state['phase']}")
    print(f"approval_status={state['approval_status']}")
    print(f"plan_locked={'да' if state.get('approval_snapshot', {}).get('locked') else 'нет'}")


if __name__ == "__main__":
    main()
