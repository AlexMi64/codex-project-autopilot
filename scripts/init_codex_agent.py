#!/usr/bin/env python3
"""Bootstrap .codex-agent workspace artifacts."""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path

from codex_agent_common import (
    ARTIFACT_FILES,
    PHASES,
    PROJECT_TYPES,
    infer_project_type,
    merge_state_defaults,
    read_template,
    save_state,
    state_dir,
    state_path,
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Инициализировать артефакты .codex-agent для workspace.")
    parser.add_argument("--workspace", default=".", help="Корень workspace.")
    parser.add_argument("--idea", default="", help="Идея проекта для стартовой цели.")
    parser.add_argument("--audience", default="", help="Короткая подсказка по аудитории.")
    parser.add_argument(
        "--project-type",
        choices=PROJECT_TYPES,
        default="",
        help="Явно задать тип проекта.",
    )
    parser.add_argument("--phase", choices=PHASES, default="discovery", help="Текущая или стартовая фаза проекта.")
    parser.add_argument(
        "--quality-mode",
        choices=["быстро", "сбалансированно", "строго"],
        default="сбалансированно",
        help="Режим качества для нового проекта.",
    )
    parser.add_argument("--force", action="store_true", help="Перезаписать шаблонные артефакты.")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    workspace = Path(args.workspace).expanduser().resolve()
    workspace_state_path = state_path(workspace)
    workspace_state_path.parent.mkdir(parents=True, exist_ok=True)

    existing_state = {}
    if workspace_state_path.exists() and not args.force:
        existing_state = json.loads(workspace_state_path.read_text(encoding="utf-8"))

    project_type = infer_project_type(args.idea, args.project_type or None)
    state = merge_state_defaults(
        existing_state,
        workspace,
        goal=args.idea,
        audience=args.audience,
        project_type=project_type if args.project_type or args.idea or not existing_state else "",
        phase=args.phase,
    )
    state["quality_mode"] = args.quality_mode if not existing_state or args.force else state.get("quality_mode", args.quality_mode)

    artifact_root = state_dir(workspace)
    artifact_root.mkdir(parents=True, exist_ok=True)
    for artifact_name in ARTIFACT_FILES:
        artifact_path = artifact_root / artifact_name
        if args.force or not artifact_path.exists():
            artifact_path.write_text(read_template(artifact_name), encoding="utf-8")

    save_state(workspace, state)
    subprocess.run(
        [
            sys.executable,
            str(Path(__file__).resolve().parent / "build_context_bundle.py"),
            "--workspace",
            str(workspace),
        ],
        check=True,
        capture_output=True,
        text=True,
    )

    print(f"Инициализировано: {artifact_root}")
    print(f"project_type={state['project_type']}")
    print(f"secondary={','.join(state.get('secondary_archetypes', [])) or 'нет'}")
    print(f"capabilities={','.join(state.get('capabilities', [])) or 'нет'}")
    print(f"phase={state['phase']}")
    print(f"token_mode={state['token_mode']}")
    print(f"quality_mode={state['quality_mode']}")
    print(f"playbook={state['playbook']}")
    print(f"supporting_playbooks={','.join(state.get('supporting_playbooks', [])) or 'нет'}")
    print(f"packs={','.join(state['selected_packs'])}")
    print(f"roles={','.join(state['active_roles'])}")


if __name__ == "__main__":
    main()
