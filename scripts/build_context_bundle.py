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


def build_deliverable_template_lines(state: dict) -> list[str]:
    lines: list[str] = []
    templates = state.get("deliverable_templates", {})
    for role in state.get("active_roles", []):
        parts = templates.get(role, [])
        if not parts:
            continue
        lines.append(f"- `{role}`: {', '.join(parts[:4])}")
    return lines


def build_delegation_packet_lines(state: dict) -> list[str]:
    lines: list[str] = []
    for packet in state.get("delegation_packets", []):
        role = packet.get("role", "unknown")
        read_first = ", ".join(packet.get("read_first", [])[:4])
        write_scope = ", ".join(packet.get("write_scope", [])[:4])
        deliverables = ", ".join(packet.get("must_return", {}).get("deliverables", [])[:4])
        lines.append(f"- `{role}`: читать {read_first}; менять {write_scope}; вернуть {deliverables}")
    return lines


def limited_lines(items: list[str], limit: int) -> list[str]:
    if len(items) <= limit:
        return items
    hidden = len(items) - limit
    return items[:limit] + [f"- ... ещё {hidden} пункт(ов), открывай подробные файлы только если они реально нужны."]


def phase_heading(state: dict) -> list[str]:
    return [
        "## Текущая фаза",
        "",
        f"- Фаза: `{state.get('phase', 'unknown')}`",
        f"- Режим токенов: `{state.get('token_mode', 'ultra')}`",
        f"- Режим оркестрации: `{state.get('orchestration_mode', 'solo')}`",
        f"- Политика чтения docs: `{state.get('doc_read_policy', 'summary-first, docs-on-demand')}`",
        f"- Сначала открой: `{', '.join(state.get('phase_context_targets', [])[:4])}`",
    ]


def next_task_line(state: dict) -> str:
    next_task = next((task for task in state.get("tasks", []) if task.get("status") == "in_progress"), None)
    if not next_task:
        return "- Текущий шаг: `нет активного шага`"
    return f"- Текущий шаг: `{next_task['id']}` -> {next_task['title']}"


def build_phase_card(state: dict) -> str:
    lines = [
        "# Фазовая карточка",
        "",
        "Прочитай этот файл первым. Если его хватает для следующего решения, остальные файлы не открывай.",
        "",
        f"- Цель: {state.get('goal') or '[не задана]'}",
        f"- Архетип: `{state.get('project_type', 'unknown')}`",
        next_task_line(state),
        f"- Выбранный план: `{state.get('selected_plan_variant', 'оптимально')}`",
        f"- План заморожен: `{'да' if state.get('approval_snapshot', {}).get('locked') else 'нет'}`",
        f"- Нужен ответ пользователя: `{'да' if state.get('blocked_on_user') else 'нет'}`",
        f"- Открывай полные docs только если: {state.get('doc_open_triggers', ['без них нельзя сделать текущий шаг'])[0]}",
        f"- Потом, если нужно: `{', '.join(state.get('phase_context_targets', [])[:4])}`",
    ]
    return "\n".join(lines).rstrip() + "\n"


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
        f"- Soul system: `{state.get('souls_version', 'unknown')}`",
        f"- План заморожен: `{'да' if state.get('approval_snapshot', {}).get('locked') else 'нет'}`",
        f"- Выбранный вариант плана: `{state.get('selected_plan_variant', 'оптимально')}`",
        f"- Режим объяснений: `{state.get('beginner_explanation_mode', 'включен')}`",
        f"- Режим scope: `{state.get('scope_mode', 'mvp-с-отдельным-блоком-рекомендаций')}`",
        f"- Политика docs: `{state.get('doc_read_policy', 'summary-first, docs-on-demand')}`",
        f"- Следующий шаг: `{next_task['id']}` -> {next_task['title']}" if next_task else "- Следующий шаг: `нет активного шага`",
        f"- Нужен ответ пользователя: `{blockers}`",
        f"- Сначала открой: `{', '.join(state.get('phase_context_targets', [])[:4])}`",
    ]
    return "\n".join(lines).rstrip() + "\n"


def build_context_bundle(state: dict, selected_pack_lines: list[str]) -> str:
    phase = state.get("phase", "discovery")
    current_tasks = [
        f"- `{task['id']}` ({task['status']}): {task['title']}"
        for task in state.get("tasks", [])
        if task.get("status") != "done"
    ]
    role_contract_lines = build_role_contract_lines(state)
    delegation_target_lines = build_delegation_target_lines(state)
    delegation_packet_lines = build_delegation_packet_lines(state)
    sections: list[str] = [
        "# Контекстный bundle",
        "",
        "Открывай этот файл только если `phase-card.md` и `ultra-context.md` уже не дают ответа на текущий шаг.",
        "",
        "## Проект",
        "",
        f"- Цель: {state.get('goal') or '[не задана]'}",
        f"- Язык контента: `{state.get('content_language', 'unknown')}`",
        f"- Архетип: `{state.get('project_type', 'unknown')}`",
        f"- Capabilities: `{', '.join(state.get('capabilities', [])) or 'нет'}`",
        f"- Маршрут реализации: `{state.get('playbook', '')}`",
        "",
        *phase_heading(state),
        "",
    ]

    if phase in {"discovery", "planning", "approval"}:
        style_input_lines = limited_lines(
            [
                f"- {item.get('type')}: {item.get('label')} ({item.get('path')})"
                for item in state.get("style_inputs", [])
            ],
            3,
        ) or ["- нет внешних style-inputs"]
        sections.extend(
            [
                "## Product DNA",
                "",
                *limited_lines([f"- {key}: {value}" for key, value in state.get("project_dna", {}).items()], 3),
                "",
                "## Профиль дизайна",
                "",
                *limited_lines([f"- {key}: {value}" for key, value in state.get("design_profile", {}).items()], 4),
                "",
                "## Источники стиля",
                "",
                *style_input_lines,
                "",
                "## Правила уникальности",
                "",
                *limited_lines([f"- {item}" for item in state.get("uniqueness_rules", [])], 4),
                "",
                "## Варианты плана",
                "",
                *[
                    f"- `{variant.get('id')}`: {variant.get('summary')}"
                    for variant in state.get("plan_variants", [])
                ],
                "",
            ]
        )

    if phase in {"planning", "approval", "execution"}:
        sections.extend(
            [
                "## Стек",
                "",
                *limited_lines([f"- {key}: {value}" for key, value in state.get("selected_stack", {}).items()], 5),
                "",
                "## Активные роли",
                "",
                *limited_lines([f"- `{role}`" for role in state.get("active_roles", [])], 6),
                "",
            ]
        )

    if phase in {"planning", "execution"}:
        sections.extend(
            [
                "## Короткие контракты ролей",
                "",
                *(limited_lines(role_contract_lines, 4) or ["- контракты ролей не описаны"]),
                "",
            ]
        )

    if phase == "execution" and state.get("orchestration_mode") == "delegated":
        sections.extend(
            [
                "## Делегирование",
                "",
                *limited_lines(
                    [
                        f"- {item}"
                        for item in state.get("delegation_policy", {}).get("delegated", {}).get("guardrails", [])
                    ],
                    3,
                ),
                "",
                "### Возможные цели",
                "",
                *limited_lines(delegation_target_lines, 4),
                "",
                "### Delegation packets",
                "",
                *limited_lines(delegation_packet_lines, 3),
                "",
            ]
        )

    if phase in {"discovery", "planning", "execution"}:
        sections.extend(
            [
                "## Активные knowledge packs",
                "",
                *(selected_pack_lines or ["- нет"]),
                "",
            ]
        )

    if phase in {"planning", "approval", "execution", "verification"}:
        sections.extend(
            [
                "## Критерии качества",
                "",
                *limited_lines([f"- `{gate}`" for gate in state.get("quality_gates", [])], 6),
                "",
            ]
        )

    if phase in {"verification", "handoff"}:
        sections.extend(
            [
                "## Обязательная проверка",
                "",
                *limited_lines([f"- `{item}`" for item in state.get("verification_required", [])], 6),
                "",
            ]
        )

    if phase == "verification":
        sections.extend(
            [
                "## Взаимные проверки",
                "",
                *limited_lines([f"- {item}" for item in state.get("cross_checks", [])], 4),
                "",
            ]
        )

    if phase == "handoff":
        sections.extend(
            [
                "## Правила handoff",
                "",
                *limited_lines([f"- {item}" for item in state.get("handoff_rules", [])], 4),
                "",
            ]
        )

    sections.extend(
        [
            "## Scope guardrails",
            "",
            *limited_lines([f"- {item}" for item in state.get("scope_guardrails", [])], 4),
            "",
            "## Открывай полные docs только если",
            "",
            *limited_lines([f"- {item}" for item in state.get("doc_open_triggers", [])], 4),
            "",
            "## Текущая очередь",
            "",
            *(limited_lines(current_tasks, 4) if current_tasks else ["- нет активных задач"]),
            "",
            "## Правила экономии токенов",
            "",
            "- Сначала читай `phase-card.md`, потом `ultra-context.md`.",
            "- Открывай `context-bundle.md` только если коротких файлов уже недостаточно.",
            "- Открывай полные docs только по текущим триггерам фазы.",
            "- Используй `state.json` для маршрутизации решений, а не для полного перечитывания проекта.",
            "- Если план уже заморожен, не пересобирай стек, роли и packs без явной причины.",
        ]
    )

    return "\n".join(sections).rstrip() + "\n"


def main() -> None:
    args = parse_args()
    workspace = Path(args.workspace).expanduser().resolve()
    agent_dir = state_dir(workspace)
    state = load_state(workspace)
    index = load_knowledge_index()

    selected_pack_lines = build_selected_pack_lines(state, index)
    (agent_dir / "phase-card.md").write_text(build_phase_card(state), encoding="utf-8")
    (agent_dir / "ultra-context.md").write_text(build_ultra_context(state), encoding="utf-8")
    (agent_dir / "context-bundle.md").write_text(build_context_bundle(state, selected_pack_lines), encoding="utf-8")
    print(agent_dir / "phase-card.md")
    print(agent_dir / "ultra-context.md")
    print(agent_dir / "context-bundle.md")


if __name__ == "__main__":
    main()
