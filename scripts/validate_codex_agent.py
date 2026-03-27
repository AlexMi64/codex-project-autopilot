#!/usr/bin/env python3
"""Validate .codex-agent consistency and handoff readiness."""

from __future__ import annotations

import argparse
from pathlib import Path

from codex_agent_common import (
    ARTIFACT_FILES,
    PHASES,
    REQUIRED_STATE_KEYS,
    approval_snapshot_path,
    has_meaningful_content,
    is_template_content,
    load_state,
    read_approval_snapshot,
    select_pack_ids,
    state_dir,
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Проверить артефакты и состояние .codex-agent.")
    parser.add_argument("--workspace", default=".", help="Корень workspace.")
    parser.add_argument("--allow-missing", action="store_true", help="Не считать ошибкой отсутствие .codex-agent.")
    parser.add_argument("--require-finalization", action="store_true", help="Жестко требовать заполненный handoff.")
    parser.add_argument("--soft-fail", action="store_true", help="Печатать ошибки, но завершаться с кодом 0.")
    return parser.parse_args()


def validate(workspace: Path, require_finalization: bool) -> list[str]:
    issues: list[str] = []
    agent_dir = state_dir(workspace)
    if not agent_dir.exists():
        issues.append(f"Отсутствует {agent_dir}")
        return issues

    state_file = agent_dir / "state.json"
    if not state_file.exists():
        issues.append(f"Отсутствует {state_file}")
        return issues

    try:
        state = load_state(workspace)
    except Exception as exc:  # noqa: BLE001
        issues.append(f"Некорректный JSON в {state_file}: {exc}")
        return issues

    for key in REQUIRED_STATE_KEYS:
        if key not in state:
            issues.append(f"В state.json нет обязательного ключа '{key}'")

    phase = state.get("phase")
    if phase not in PHASES:
        issues.append(f"В state.json неподдерживаемая фаза '{phase}'")

    if not isinstance(state.get("secondary_archetypes"), list):
        issues.append("В state.json должен быть список secondary_archetypes")
    if not isinstance(state.get("capabilities"), list):
        issues.append("В state.json должен быть список capabilities")
    if not isinstance(state.get("phase_history"), list) or not state.get("phase_history"):
        issues.append("В state.json должен быть непустой список phase_history")
    if not isinstance(state.get("plan_variants"), list) or len(state.get("plan_variants", [])) != 3:
        issues.append("В state.json должно быть ровно 3 варианта плана в plan_variants")
    if not isinstance(state.get("selected_plan_variant"), str) or not state.get("selected_plan_variant"):
        issues.append("В state.json должен быть непустой selected_plan_variant")
    if state.get("selected_plan_variant") not in {item.get("id") for item in state.get("plan_variants", []) if isinstance(item, dict)}:
        issues.append("selected_plan_variant должен совпадать с одним из id в plan_variants")
    if not isinstance(state.get("beginner_explanation_mode"), str) or not state.get("beginner_explanation_mode"):
        issues.append("В state.json должен быть непустой beginner_explanation_mode")
    if not isinstance(state.get("user_overrides"), dict):
        issues.append("В state.json должен быть объект user_overrides")

    if not isinstance(state.get("selected_stack"), dict) or not state.get("selected_stack"):
        issues.append("В state.json должен быть непустой объект selected_stack")
    if not isinstance(state.get("active_roles"), list) or not state.get("active_roles"):
        issues.append("В state.json должен быть непустой список active_roles")
    if not isinstance(state.get("recommended_skills"), list):
        issues.append("В state.json должен быть список recommended_skills")
    if not isinstance(state.get("selected_packs"), list) or not state.get("selected_packs"):
        issues.append("В state.json должен быть непустой список selected_packs")
    if not isinstance(state.get("quality_gates"), list) or not state.get("quality_gates"):
        issues.append("В state.json должен быть непустой список quality_gates")
    if not isinstance(state.get("verification_required"), list) or not state.get("verification_required"):
        issues.append("В state.json должен быть непустой список verification_required")
    if not isinstance(state.get("playbook"), str) or not state.get("playbook"):
        issues.append("В state.json должен быть непустой playbook")
    if not isinstance(state.get("supporting_playbooks"), list):
        issues.append("В state.json должен быть список supporting_playbooks")
    if not isinstance(state.get("scope_mode"), str) or not state.get("scope_mode"):
        issues.append("В state.json должен быть непустой scope_mode")
    if not isinstance(state.get("recommendation_policy"), str) or not state.get("recommendation_policy"):
        issues.append("В state.json должен быть непустой recommendation_policy")
    if not isinstance(state.get("scope_guardrails"), list) or not state.get("scope_guardrails"):
        issues.append("В state.json должен быть непустой список scope_guardrails")
    if not isinstance(state.get("orchestration_mode"), str) or state.get("orchestration_mode") not in {"solo", "delegated"}:
        issues.append("В state.json orchestration_mode должен быть 'solo' или 'delegated'")
    if not isinstance(state.get("delegation_policy"), dict) or not state.get("delegation_policy"):
        issues.append("В state.json должен быть непустой объект delegation_policy")
    if not isinstance(state.get("delegation_targets"), list):
        issues.append("В state.json должен быть список delegation_targets")
    if not isinstance(state.get("role_system_version"), str) or not state.get("role_system_version"):
        issues.append("В state.json должен быть непустой role_system_version")
    if not isinstance(state.get("role_contracts"), dict) or not state.get("role_contracts"):
        issues.append("В state.json должен быть непустой объект role_contracts")
    if not isinstance(state.get("handoff_rules"), list) or not state.get("handoff_rules"):
        issues.append("В state.json должен быть непустой список handoff_rules")
    if not isinstance(state.get("cross_checks"), list) or not state.get("cross_checks"):
        issues.append("В state.json должен быть непустой список cross_checks")
    if not isinstance(state.get("tasks"), list) or not state.get("tasks"):
        issues.append("В state.json должен быть непустой список tasks")

    approval_snapshot = state.get("approval_snapshot", {})
    if not isinstance(approval_snapshot, dict):
        issues.append("В state.json должен быть объект approval_snapshot")
    snapshot_file = approval_snapshot_path(workspace)
    snapshot_data = read_approval_snapshot(workspace)
    if approval_snapshot.get("locked") and not snapshot_file.exists():
        issues.append(f"План помечен как замороженный, но отсутствует {snapshot_file}")
    if approval_snapshot.get("locked") and not snapshot_data.get("locked"):
        issues.append("approval_snapshot.locked=true, но файл approval-snapshot.json не подтверждает заморозку плана")

    artifacts = state.get("artifacts", {})
    for artifact_name in ARTIFACT_FILES:
        artifact_path = agent_dir / artifact_name
        if artifact_name not in artifacts:
            issues.append(f"В state.json artifacts нет '{artifact_name}'")
        if not artifact_path.exists():
            issues.append(f"Отсутствует артефакт {artifact_path}")

    token_mode = state.get("token_mode", "ultra")
    if token_mode == "ultra":
        targets = state.get("phase_context_targets", [])
        if not targets or targets[0] != "ultra-context.md":
            issues.append("В режиме ultra первым phase_context_targets должен быть ultra-context.md")

    expected_packs = select_pack_ids(
        state.get("project_type", "general-web-product"),
        state.get("phase", "discovery"),
        state.get("secondary_archetypes", []),
        state.get("capabilities", []),
    )
    override_selected_packs = state.get("user_overrides", {}).get("selected_packs")
    if not override_selected_packs:
        unexpected_packs = sorted(set(state.get("selected_packs", [])) - set(expected_packs))
        if unexpected_packs:
            issues.append(f"selected_packs содержит элементы не по текущей фазе/архетипу: {', '.join(unexpected_packs)}")

    required_for_planning = [
        "ultra-context.md",
        "context-bundle.md",
        "discovery-questionnaire.md",
        "plan-variants.md",
        "beginner-guide.md",
        "project-brief.md",
        "product-intelligence.md",
        "product-context.md",
        "tech-context.md",
    ]
    required_before_approval = ["implementation-plan.md", "active-context.md", "progress.md"]
    required_before_handoff = ["verification-report.md", "scorecard.md", "env-secrets-checklist.md", "final-handoff.md"]

    if phase in {"planning", "approval", "execution", "verification", "handoff"}:
        for artifact_name in required_for_planning:
            artifact_path = agent_dir / artifact_name
            if artifact_name.endswith(".json"):
                continue
            if artifact_path.exists() and (
                is_template_content(artifact_path, artifact_name)
                or not has_meaningful_content(artifact_path.read_text(encoding="utf-8"))
            ):
                issues.append(f"{artifact_name} все еще шаблонный для фазы '{phase}'")

    if phase in {"approval", "execution", "verification", "handoff"}:
        for artifact_name in required_before_approval:
            artifact_path = agent_dir / artifact_name
            if artifact_path.exists() and (
                is_template_content(artifact_path, artifact_name)
                or not has_meaningful_content(artifact_path.read_text(encoding="utf-8"))
            ):
                issues.append(f"{artifact_name} все еще шаблонный для фазы '{phase}'")

    if phase in {"execution", "verification", "handoff"}:
        if state.get("approval_status") != "approved":
            issues.append("Для фаз execution/verification/handoff approval_status должен быть approved")
        if not approval_snapshot.get("locked"):
            issues.append("Для фаз execution/verification/handoff план должен быть заморожен через approval_snapshot")

    if require_finalization or phase == "handoff":
        for artifact_name in required_for_planning + required_before_approval + required_before_handoff:
            artifact_path = agent_dir / artifact_name
            if not artifact_path.exists():
                issues.append(f"Нет обязательного handoff-артефакта {artifact_path}")
                continue
            content = artifact_path.read_text(encoding="utf-8")
            if is_template_content(artifact_path, artifact_name) or not has_meaningful_content(content):
                issues.append(f"{artifact_name} должен быть заполнен до финализации")

    return issues


def main() -> None:
    args = parse_args()
    workspace = Path(args.workspace).expanduser().resolve()
    agent_dir = state_dir(workspace)
    if not agent_dir.exists() and args.allow_missing:
        print(f"[codex-agent] Пропускаю проверку: {agent_dir} не существует")
        return

    issues = validate(workspace, require_finalization=args.require_finalization)
    if issues:
        for issue in issues:
            print(f"[codex-agent] {issue}")
        if args.soft_fail:
            return
        raise SystemExit(1)

    print(f"[codex-agent] Проверка пройдена для {workspace}")


if __name__ == "__main__":
    main()
