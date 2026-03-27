#!/usr/bin/env python3
"""Build compact context bundles to reduce repeated prompt token usage."""

from __future__ import annotations

import argparse
from pathlib import Path

from codex_agent_common import (
    extract_summary_from_markdown,
    load_knowledge_index,
    load_state,
    path_from_plugin_relative,
    state_dir,
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Собрать компактные context bundles для .codex-agent")
    parser.add_argument("--workspace", default=".", help="Корень workspace.")
    return parser.parse_args()


def build_selected_pack_lines(state: dict, index: dict) -> list[str]:
    pack_map = {pack["id"]: pack for pack in index.get("packs", [])}
    selected_pack_lines: list[str] = []
    for pack_id in state.get("selected_packs", []):
        pack = pack_map.get(pack_id)
        if not pack:
            continue
        pack_path = path_from_plugin_relative(pack["path"])
        summary = extract_summary_from_markdown(pack_path, fallback=pack["title"])
        selected_pack_lines.append(f"- `{pack_id}`: {summary}")
    return selected_pack_lines


def build_role_contract_lines(state: dict) -> list[str]:
    contracts = state.get("role_contracts", {})
    lines: list[str] = []
    for role in state.get("active_roles", []):
        contract = contracts.get(role, {})
        mission = contract.get("mission")
        done = contract.get("done_criteria", [])
        handoff = contract.get("handoff_to", [])
        summary = mission or "контракт не описан"
        done_line = f" done: {done[0]}" if done else ""
        handoff_line = f" handoff: {', '.join(handoff)}" if handoff else ""
        lines.append(f"- `{role}`: {summary}.{done_line}{handoff_line}")
    return lines


def build_delegation_target_lines(state: dict) -> list[str]:
    lines: list[str] = []
    for target in state.get("delegation_targets", []):
        role = target.get("role", "unknown")
        ownership = target.get("ownership", "")
        spawn_when = target.get("spawn_when", "")
        lines.append(f"- `{role}`: зона = {ownership}; запускать, когда {spawn_when.lower()}")
    return lines


def build_ultra_context(state: dict) -> str:
    next_task = next((task for task in state.get("tasks", []) if task.get("status") == "in_progress"), None)
    blockers = "да" if state.get("blocked_on_user") else "нет"
    lines = [
        "# Ультра-контекст",
        "",
        "Сначала читай этот файл. Остальные файлы открывай только если без них нельзя решить текущий шаг.",
        "",
        f"- Цель: {state.get('goal') or '[не задана]'}",
        f"- Фаза: `{state.get('phase', 'unknown')}`",
        f"- Основной архетип: `{state.get('project_type', 'unknown')}`",
        f"- Вторичные архетипы: `{', '.join(state.get('secondary_archetypes', [])) or 'нет'}`",
        f"- Capabilities: `{', '.join(state.get('capabilities', [])) or 'нет'}`",
        f"- Режим оркестрации: `{state.get('orchestration_mode', 'solo')}`",
        f"- План заморожен: `{'да' if state.get('approval_snapshot', {}).get('locked') else 'нет'}`",
        f"- Выбранный вариант плана: `{state.get('selected_plan_variant', 'оптимально')}`",
        f"- Режим объяснений: `{state.get('beginner_explanation_mode', 'включен')}`",
        f"- Режим scope: `{state.get('scope_mode', 'mvp-с-отдельным-блоком-рекомендаций')}`",
        f"- Следующий шаг: `{next_task['id']}` -> {next_task['title']}" if next_task else "- Следующий шаг: `нет активного шага`",
        f"- Нужен ответ пользователя: `{blockers}`",
        f"- Сначала открой: `{', '.join(state.get('phase_context_targets', [])[:3])}`",
    ]
    return "\n".join(lines).rstrip() + "\n"


def build_context_bundle(state: dict, selected_pack_lines: list[str]) -> str:
    current_tasks = [
        f"- `{task['id']}` ({task['status']}): {task['title']}"
        for task in state.get("tasks", [])
        if task.get("status") != "done"
    ]
    role_contract_lines = build_role_contract_lines(state)
    delegation_target_lines = build_delegation_target_lines(state)

    bundle = "\n".join(
        [
            "# Контекстный bundle",
            "",
            "Используй этот файл вторым после `ultra-context.md`, если нужен расширенный, но всё ещё экономный контекст.",
            "",
            "## Текущий проект",
            "",
            f"- Цель: {state.get('goal') or '[не задана]'}",
            f"- Архетип: `{state.get('project_type', 'unknown')}`",
            f"- Вторичные архетипы: `{', '.join(state.get('secondary_archetypes', [])) or 'нет'}`",
            f"- Capabilities: `{', '.join(state.get('capabilities', [])) or 'нет'}`",
            f"- Фаза: `{state.get('phase', 'unknown')}`",
            f"- Режим токенов: `{state.get('token_mode', 'ultra')}`",
            f"- Режим качества: `{state.get('quality_mode', 'сбалансированно')}`",
            f"- Режим оркестрации: `{state.get('orchestration_mode', 'solo')}`",
            f"- План заморожен: `{'да' if state.get('approval_snapshot', {}).get('locked') else 'нет'}`",
            f"- Выбранный вариант плана: `{state.get('selected_plan_variant', 'оптимально')}`",
            f"- Режим объяснений: `{state.get('beginner_explanation_mode', 'включен')}`",
            f"- Режим scope: `{state.get('scope_mode', 'mvp-с-отдельным-блоком-рекомендаций')}`",
            f"- Политика рекомендаций: `{state.get('recommendation_policy', 'советы отдельно от MVP')}`",
            f"- Маршрут реализации: `{state.get('playbook', '')}`",
            "",
            "## Стек",
            "",
            *[f"- {key}: {value}" for key, value in state.get("selected_stack", {}).items()],
            "",
            "## Активные роли",
            "",
            *[f"- `{role}`" for role in state.get("active_roles", [])],
            "",
            "## Короткие контракты ролей",
            "",
            *(role_contract_lines or ["- контракты ролей не описаны"]),
            "",
            "## Делегирование",
            "",
            f"- Активный режим: `{state.get('orchestration_mode', 'solo')}`",
            *[
                f"- {item}"
                for item in state.get("delegation_policy", {}).get(state.get("orchestration_mode", "solo"), {}).get("guardrails", [])
            ],
            *(["", "### Возможные цели делегирования", ""] + delegation_target_lines if delegation_target_lines else []),
            "",
            "## Рекомендуемые skills",
            "",
            *[f"- `{skill}`" for skill in state.get("recommended_skills", [])],
            "",
            "## Выбранные knowledge packs",
            "",
            *(selected_pack_lines or ["- нет"]),
            "",
            "## Варианты плана",
            "",
            *[
                f"- `{variant.get('id')}`: {variant.get('summary')} Выбирать, когда {variant.get('when_to_choose', '').lower()}"
                for variant in state.get("plan_variants", [])
            ],
            "",
            "## Критерии качества",
            "",
            *[f"- `{gate}`" for gate in state.get("quality_gates", [])],
            "",
            "## Обязательная проверка",
            "",
            *[f"- `{item}`" for item in state.get("verification_required", [])],
            "",
            "## Сначала читай эти файлы",
            "",
            *[f"- `{path}`" for path in state.get("phase_context_targets", [])],
            "",
            "## Взаимные проверки ролей",
            "",
            *[f"- {item}" for item in state.get("cross_checks", [])],
            "",
            "## Правила handoff",
            "",
            *[f"- {item}" for item in state.get("handoff_rules", [])],
            "",
            "## Scope guardrails",
            "",
            *[f"- {item}" for item in state.get("scope_guardrails", [])],
            "",
            "## Текущая очередь работы",
            "",
            *(current_tasks or ["- нет активных задач"]),
            "",
            "## Правила экономии токенов",
            "",
            "- Сначала читай `ultra-context.md`, а не весь набор артефактов.",
            "- Открывай `context-bundle.md` только если ультра-контекста уже недостаточно.",
            "- Открывай другие файлы из `.codex-agent` только если они реально нужны текущему шагу.",
            "- Используй `state.json` для маршрутизации решений, а не перечитывай длинные документы.",
            "- Считай knowledge packs краткими инструкциями и открывай полный pack только для активной подсистемы.",
            "- Если план уже заморожен, не пересобирай стек и роли без явной причины.",
        ]
    ).rstrip() + "\n"
    return bundle


def main() -> None:
    args = parse_args()
    workspace = Path(args.workspace).expanduser().resolve()
    agent_dir = state_dir(workspace)
    state = load_state(workspace)
    index = load_knowledge_index()

    selected_pack_lines = build_selected_pack_lines(state, index)
    (agent_dir / "ultra-context.md").write_text(build_ultra_context(state), encoding="utf-8")
    (agent_dir / "context-bundle.md").write_text(build_context_bundle(state, selected_pack_lines), encoding="utf-8")
    print(agent_dir / "ultra-context.md")
    print(agent_dir / "context-bundle.md")


if __name__ == "__main__":
    main()
