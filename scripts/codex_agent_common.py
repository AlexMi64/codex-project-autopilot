#!/usr/bin/env python3
"""Shared helpers for the Autonomous Project Agent plugin."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any


PLUGIN_ROOT = Path(__file__).resolve().parents[1]
TEMPLATE_DIR = PLUGIN_ROOT / "templates"
REFERENCE_DIR = PLUGIN_ROOT / "references"
KNOWLEDGE_INDEX_PATH = REFERENCE_DIR / "knowledge-index.json"
ROLE_SYSTEM_VERSION = "morecil-role-system-v1"
SOULS_VERSION = "morecil-souls-v1"
STATE_DIRNAME = ".codex-agent"
ARTIFACT_FILES = [
    "phase-card.md",
    "ultra-context.md",
    "context-bundle.md",
    "discovery-questionnaire.md",
    "plan-variants.md",
    "beginner-guide.md",
    "project-brief.md",
    "design-system.json",
    "product-intelligence.md",
    "product-context.md",
    "tech-context.md",
    "active-context.md",
    "progress.md",
    "implementation-plan.md",
    "design-direction.md",
    "data-model.md",
    "execution-log.md",
    "verification-report.md",
    "scorecard.md",
    "env-secrets-checklist.md",
    "final-handoff.md",
    "approval-snapshot.json",
]
PLAN_LOCK_FIELDS = [
    "project_type",
    "project_archetype",
    "secondary_archetypes",
    "capabilities",
    "selected_stack",
    "active_roles",
    "recommended_skills",
    "selected_packs",
    "playbook",
    "supporting_playbooks",
    "quality_gates",
    "verification_required",
    "execution_strategy",
    "orchestration_mode",
    "delegation_policy",
    "delegation_targets",
    "delegation_packets",
    "quality_mode",
]
REQUIRED_STATE_KEYS = [
    "project_type",
    "project_archetype",
    "secondary_archetypes",
    "capabilities",
    "token_mode",
    "quality_mode",
    "content_language",
    "goal",
    "audience",
    "plan_variants",
    "selected_plan_variant",
    "beginner_explanation_mode",
    "phase",
    "phase_history",
    "answers",
    "assumptions",
    "selected_stack",
    "active_roles",
    "recommended_skills",
    "selected_packs",
    "playbook",
    "supporting_playbooks",
    "quality_gates",
    "verification_required",
    "approval_status",
    "approval_snapshot",
    "execution_strategy",
    "orchestration_mode",
    "delegation_policy",
    "delegation_targets",
    "delegation_packets",
    "scope_mode",
    "recommendation_policy",
    "scope_guardrails",
    "role_system_version",
    "souls_version",
    "design_profile",
    "style_inputs",
    "project_dna",
    "security_profile",
    "security_guardrails",
    "uniqueness_rules",
    "deliverable_templates",
    "role_contracts",
    "handoff_rules",
    "phase_context_targets",
    "doc_read_policy",
    "doc_open_triggers",
    "cross_checks",
    "user_overrides",
    "tasks",
    "blocked_on_user",
    "manual_inputs",
    "artifacts",
]
PHASES = ["discovery", "planning", "approval", "execution", "verification", "handoff"]
PHASE_INDEX = {phase: index for index, phase in enumerate(PHASES)}
PROJECT_TYPES = [
    "landing-page",
    "saas-mvp",
    "telegram-ai-bot",
    "automation-script",
    "api-integration-worker",
    "general-web-product",
]
PROJECT_TYPE_RULES: list[tuple[str, tuple[str, ...]]] = [
    ("telegram-ai-bot", ("telegram", "bot", "чат-бот", "бот", "assistant", "telegraf")),
    ("automation-script", ("cron", "script", "sync", "parser", "automation", "cli", "scrape", "worker", "скрипт", "автоматизац", "парсер")),
    ("api-integration-worker", ("webhook", "integration", "provider", "api", "callback", "endpoint", "интеграц", "вебхук")),
    ("saas-mvp", ("saas", "dashboard", "cabinet", "auth", "crm", "admin", "кабинет", "дашборд", "авторизац", "админ")),
    ("landing-page", ("landing", "promo", "marketing site", "website", "site", "лендинг", "сайт")),
]
CAPABILITY_RULES: list[tuple[str, tuple[str, ...]]] = [
    ("ai", ("ai", "gpt", "llm", "openai", "assistant", "ии")),
    ("auth", ("auth", "login", "sign in", "signup", "авторизац", "вход", "регистрац")),
    ("dashboard", ("dashboard", "cabinet", "admin", "panel", "дашборд", "кабинет", "панель", "админ")),
    ("database", ("database", "postgres", "supabase", "sql", "база", "таблиц")),
    ("payments", ("payment", "billing", "stripe", "подписк", "платеж", "оплат")),
    ("api", ("api", "endpoint", "webhook", "callback", "интеграц", "вебхук")),
    ("automation", ("automation", "cron", "sync", "worker", "автоматизац", "расписан")),
    ("telegram", ("telegram", "bot", "telegraf", "телеграм", "бот")),
    ("marketing", ("landing", "promo", "marketing", "лендинг", "маркетинг")),
    ("admin-panel", ("admin", "dashboard", "panel", "админ", "панель")),
]
CAPABILITY_SKILLS = {
    "ai": ["openai-docs"],
    "auth": ["security-best-practices"],
    "dashboard": ["frontend-skill", "react-best-practices"],
    "database": ["supabase-postgres-best-practices"],
    "payments": ["stripe-best-practices"],
    "api": ["security-best-practices"],
    "automation": ["playwright"],
    "marketing": ["frontend-skill", "web-design-guidelines"],
}
CAPABILITY_QUALITY_GATES = {
    "ai": ["prompt-and-fallback-paths-defined"],
    "auth": ["auth-boundaries", "least-privilege", "secrets-not-in-repo"],
    "dashboard": ["role-specific-empty-and-error-states"],
    "database": ["data-protection", "least-privilege", "sql-safe-paths"],
    "payments": ["payment-flow-sandboxed", "secret-hygiene"],
    "api": ["input-validation", "secret-hygiene"],
    "automation": ["dry-run-or-safe-preview", "dependency-hygiene"],
    "marketing": ["clear-cta"],
}
CAPABILITY_VERIFICATION = {
    "ai": ["fallback-response-check"],
    "auth": ["auth-flow-smoke-test", "access-boundary-check"],
    "dashboard": ["core-dashboard-route-check"],
    "database": ["data-flow-check", "sql-safety-review", "rls-or-access-review"],
    "payments": ["sandbox-payment-check", "secret-location-check"],
    "api": ["payload-validation-check", "secret-location-check"],
    "automation": ["failure-path-check", "dependency-vulnerability-check"],
    "marketing": ["cta-route-check"],
}
SCOPE_GUARDRAILS_BASE = [
    "Не добавляй функции, которые пользователь явно не просил, без отдельного блока рекомендаций.",
    "В первую версию включай только то, что нужно для одного рабочего сценария.",
    "Советы по улучшению отделяй от обязательного scope.",
    "Любое расширение scope после плана требует явного подтверждения пользователя.",
]
SECURITY_GUARDRAILS_BASE = [
    "Секреты хранятся только в env или панели провайдера, а не в коде и не в репозитории.",
    "Собирай и храни только те данные, без которых не работает главный сценарий.",
    "Не логируй токены, пароли, cookie, service_role ключи и другой чувствительный ввод.",
    "Перед handoff проверь зависимости и уязвимости, а не только happy path приложения.",
]
ROLE_CONTRACTS = {
    "project-discovery": {
        "mission": "Превращает смутную идею в понятный стартовый контекст без перегруза терминами.",
        "primary_outputs": [
            "discovery-questionnaire.md",
            "project-brief.md",
            "product-intelligence.md",
            "plan-variants.md",
            "beginner-guide.md",
        ],
        "done_criteria": [
            "Понятен один главный сценарий первой версии.",
            "Явно записано, что не входит в MVP.",
            "Пользователь может выбрать вариант плана без технических догадок.",
        ],
        "handoff_to": ["solution-architect"],
        "forbidden": [
            "Начинать реализацию или спорить с потребностью пользователя.",
            "Подменять вопрос новичка архитектурным допросом.",
        ],
    },
    "solution-architect": {
        "mission": "Собирает маленький, выполнимый и проверяемый маршрут вместо разросшейся схемы.",
        "primary_outputs": [
            "implementation-plan.md",
            "active-context.md",
            "progress.md",
            "plan-variants.md",
        ],
        "done_criteria": [
            "Первая версия ограничена 3-5 обязательными deliverables.",
            "Зоны frontend, backend, data и automation разделены явно.",
            "Есть acceptance criteria и список ручных входов от пользователя.",
        ],
        "handoff_to": ["design-director", "frontend-builder", "backend-builder", "database-designer", "automation-builder"],
        "forbidden": [
            "Раздувать MVP до мини-enterprise.",
            "Молча превращать рекомендации в обязательные задачи.",
        ],
    },
    "design-director": {
        "mission": "Даёт продукту характер и визуальную логику вместо дефолтного шаблона.",
        "primary_outputs": ["design-direction.md", "active-context.md"],
        "done_criteria": [
            "Выбрано одно направление с понятным обоснованием.",
            "Есть anti-generic правила и правила для mobile/readability.",
            "Дизайн поддерживает задачу продукта, а не отвлекает от неё.",
        ],
        "handoff_to": ["frontend-builder"],
        "forbidden": [
            "Оставлять дефолтный вид библиотек как финальный дизайн.",
            "Делать красивый, но нечитабельный интерфейс.",
        ],
    },
    "frontend-builder": {
        "mission": "Собирает интерфейс как инженер: ясно, устойчиво и без фальшивой витрины.",
        "primary_outputs": ["frontend-code", "execution-log.md"],
        "done_criteria": [
            "Покрыты критичные состояния интерфейса.",
            "Desktop и mobile не расходятся по качеству.",
            "UI не опирается на несуществующие API или скрытые допущения.",
        ],
        "handoff_to": ["qa-reviewer", "backend-builder"],
        "forbidden": [
            "Компенсировать архитектурные дыры красивой обёрткой.",
            "Придумывать серверную логику, которой нет.",
        ],
    },
    "backend-builder": {
        "mission": "Делает серверную логику наблюдаемой, валидируемой и пригодной к отладке.",
        "primary_outputs": ["backend-code", "execution-log.md"],
        "done_criteria": [
            "Входные данные валидируются.",
            "Ключевые события и ошибки логируются.",
            "Секреты не утекли в код, логи или клиентский слой.",
            "Failure-path и интеграционные риски хотя бы базово обработаны.",
        ],
        "handoff_to": ["frontend-builder", "qa-reviewer", "deploy-operator"],
        "forbidden": [
            "Хранить секреты в коде.",
            "Оставлять silent failure без сигнала в логах.",
        ],
    },
    "database-designer": {
        "mission": "Проектирует данные только там, где durable state действительно нужен.",
        "primary_outputs": ["data-model.md", "migration-plan"],
        "done_criteria": [
            "Обосновано, зачем вообще нужна база.",
            "Ownership, доступ и ограничения описаны.",
            "Least privilege и путь к RLS/ограничениям зафиксированы.",
            "Transient и durable state не смешаны.",
        ],
        "handoff_to": ["backend-builder", "qa-reviewer", "deploy-operator"],
        "forbidden": [
            "Добавлять таблицы без сценария использования.",
            "Игнорировать доступ и историю данных.",
        ],
    },
    "automation-builder": {
        "mission": "Собирает безопасные автоматизации, которые не превращаются в чёрный ящик.",
        "primary_outputs": ["automation-code", "execution-log.md"],
        "done_criteria": [
            "Есть dry-run или безопасный preview при side effects.",
            "Логи позволяют понять, что произошло.",
            "Повторный запуск не создаёт хаос без причины.",
        ],
        "handoff_to": ["qa-reviewer", "deploy-operator"],
        "forbidden": [
            "Скрывать side effects от пользователя.",
            "Строить автоматизацию без наблюдаемости.",
        ],
    },
    "qa-reviewer": {
        "mission": "Говорит правду о готовности и ловит слабые места перед handoff.",
        "primary_outputs": ["verification-report.md", "scorecard.md", "findings"],
        "done_criteria": [
            "Проверен happy path и хотя бы один failure path.",
            "Непроверенные зоны отмечены явно.",
            "Security-проверки не пропущены, если проект касается данных, auth, платежей или интеграций.",
            "Scorecard отражает реальное состояние, а не оптимизм.",
        ],
        "handoff_to": ["deploy-operator", "autonomous-project-orchestrator"],
        "forbidden": [
            "Писать пустое 'всё ок'.",
            "Игнорировать handoff, UX или безопасность.",
        ],
    },
    "deploy-operator": {
        "mission": "Превращает результат в понятный путь до реального запуска.",
        "primary_outputs": ["env-secrets-checklist.md", "final-handoff.md", "scorecard.md"],
        "done_criteria": [
            "Все обязательные ручные шаги перечислены.",
            "Секреты разделены на обязательные и опциональные.",
            "Пользователь может запустить проект без догадок.",
        ],
        "handoff_to": ["user"],
        "forbidden": [
            "Закрывать проект без env checklist.",
            "Скрывать остаточные риски и ручные действия.",
        ],
    },
}
HANDOFF_RULES = [
    "Каждый handoff обязан коротко перечислить: что готово, что не готово, какие решения заморожены, какие риски остались.",
    "Следующей роли нужно явно назвать 1-3 файла-источника истины, а не отправлять её 'читать всё'.",
    "Если роль не выполнила done criteria, оркестратор возвращает работу на доработку, а не двигается дальше.",
]
DELEGATION_POLICY = {
    "solo": {
        "summary": "Один агент ведёт проект последовательно по ролям без запуска под-агентов.",
        "when_to_use": [
            "Короткий или средний проект.",
            "Нет явной пользы от параллельной работы.",
            "Критичный путь требует плотной связки решений.",
        ],
        "guardrails": [
            "Не дроби работу ради видимости многозадачности.",
            "Держи контекст компактным и не пересылай всё каждой роли заново.",
        ],
    },
    "delegated": {
        "summary": "Оркестратор может запускать отдельные под-агенты для независимых ролей и интегрировать результат обратно.",
        "when_to_use": [
            "Есть хотя бы две независимые подсистемы.",
            "Фронтенд, бэкенд, data или verification можно вести параллельно.",
            "Следующий шаг не блокируется полностью одной ролью.",
        ],
        "guardrails": [
            "Не делегируй discovery и final handoff как фоновый шум — это ответственность оркестратора.",
            "Не делегируй блокирующую задачу, если без неё нельзя сделать следующий шаг локально.",
            "Каждому под-агенту нужен чёткий write scope и формат handoff.",
        ],
    },
}
DELIVERABLE_TEMPLATES = {
    "project-discovery": ["главный сценарий", "аудитория", "что входит в MVP", "что не входит в MVP", "неизвестные ответы"],
    "solution-architect": ["стек", "deliverables", "acceptance criteria", "known risks", "ручные входы"],
    "design-director": ["выбранное направление", "палитра", "типографика", "motion rules", "anti-generic rules"],
    "frontend-builder": ["реализованные маршруты", "покрытые состояния", "зависимости от backend"],
    "backend-builder": ["стабильные входы/выходы", "логируемые события", "failure-path"],
    "database-designer": ["сущности", "ownership", "доступ", "ограничения"],
    "automation-builder": ["dry-run", "логи", "side effects", "правила повторного запуска"],
    "qa-reviewer": ["findings", "что проверено", "что не проверено", "scorecard"],
    "deploy-operator": ["env checklist", "manual steps", "launch path", "residual risks"],
}
UNIQUENESS_RULES_BASE = [
    "Не существует одного универсального шаблона, который подходит всем проектам.",
    "Не выбирай решение только потому, что оно дефолтное для библиотеки или фреймворка.",
    "Не повторяй один и тот же визуальный стиль во всех проектах.",
    "Не заполняй пробелы типичным SaaS-набором без продуктового обоснования.",
    "Сначала фиксируй главный сценарий и характер продукта, потом выбирай визуал и архитектуру.",
]


def dedupe(items: list[str]) -> list[str]:
    seen: set[str] = set()
    ordered: list[str] = []
    for item in items:
        if not item or item in seen:
            continue
        seen.add(item)
        ordered.append(item)
    return ordered


def project_dna_for_project_type(project_type: str, capabilities: list[str] | None = None) -> dict[str, str]:
    capability_set = set(capabilities or [])
    matrix = {
        "landing-page": {
            "core_promise": "ясно показать ценность и подтолкнуть к одному действию",
            "interface_energy": "выразительная, но собранная",
            "trust_signal": "структура, типографика, честный CTA",
            "uniqueness_axis": "редакционная композиция вместо типового лендинга",
            "template_rejection": "не собирать сайт по дежурной схеме hero/features/testimonials/contact без причины",
        },
        "saas-mvp": {
            "core_promise": "дать пользователю один реально полезный рабочий сценарий",
            "interface_energy": "спокойная, инструментальная, но не безликая",
            "trust_signal": "понятные состояния, data clarity, ощущение контроля",
            "uniqueness_axis": "product-first UI вместо generic dashboard",
            "template_rejection": "не прятать суть продукта за типовым кабинетом из одинаковых карточек",
        },
        "telegram-ai-bot": {
            "core_promise": "давать быстрый полезный ответ без хаоса в чате",
            "interface_energy": "компактная и направляющая",
            "trust_signal": "понятное меню, отсутствие спама, предсказуемые действия",
            "uniqueness_axis": "single-message flow вместо россыпи сообщений",
            "template_rejection": "не имитировать богатый функционал десятками сообщений и лишними меню",
        },
        "automation-script": {
            "core_promise": "экономить рутину без превращения процесса в чёрный ящик",
            "interface_energy": "минимальная и служебная",
            "trust_signal": "dry-run, логи, предсказуемые side effects",
            "uniqueness_axis": "надёжность и объяснимость вместо магии",
            "template_rejection": "не маскировать логику скрипта красивыми словами без прозрачного поведения",
        },
        "api-integration-worker": {
            "core_promise": "стабильно связывать системы и переживать сбои",
            "interface_energy": "техническая и прозрачная",
            "trust_signal": "контракты, retry, идемпотентность",
            "uniqueness_axis": "операционная устойчивость вместо красивой обёртки",
            "template_rejection": "не превращать интеграцию в декоративный сервис без реальной устойчивости",
        },
        "general-web-product": {
            "core_promise": "довести пользователя до одной полезной цели без лишних подсистем",
            "interface_energy": "собранная и осмысленная",
            "trust_signal": "понятный маршрут, сильная структура, отсутствие лишнего",
            "uniqueness_axis": "характер и product fit вместо усреднённого web UI",
            "template_rejection": "не собирать продукт из готовых паттернов без привязки к реальной задаче пользователя",
        },
    }
    dna = matrix.get(project_type, matrix["general-web-product"]).copy()
    design_profile = design_profile_for_project_type(project_type, capabilities, [])
    dna["visual_intensity"] = str(design_profile.get("visual_intensity", "сдержанный"))
    dna["shape_language"] = str(design_profile.get("shape_language", "сдержанный"))
    if "ai" in capability_set:
        dna["ai_positioning"] = "AI не должен быть маской для шаблонности; он должен усиливать основной сценарий"
    if "payments" in capability_set:
        dna["payments_positioning"] = "Платёжный слой вторичен по отношению к главной ценности продукта"
    return dna


def uniqueness_rules_for_project_type(project_type: str, capabilities: list[str] | None = None) -> list[str]:
    capability_set = set(capabilities or [])
    rules = list(UNIQUENESS_RULES_BASE)
    if project_type == "landing-page":
        rules.extend(
            [
                "Не повторяй одинаковую структуру hero/features/testimonials/contact без причины.",
                "Избегай дежурной палитры и безликого hero-обещания.",
            ]
        )
    if project_type in {"saas-mvp", "general-web-product"}:
        rules.extend(
            [
                "Не превращай продукт в generic dashboard из одинаковых карточек.",
                "Визуальный слой должен подчёркивать модель продукта, а не скрывать её.",
            ]
        )
    if project_type == "telegram-ai-bot":
        rules.extend(
            [
                "Не делай UX бота шумным ради иллюзии функциональности.",
                "Уникальность бота должна идти из сценария и навигации, а не из количества сообщений.",
            ]
        )
    if "ai" in capability_set:
        rules.append("Не используй AI как стилистическую отговорку для шаблонного продукта.")
    if project_type in {"landing-page", "general-web-product"}:
        rules.append("Смелость допустима только там, где она усиливает продукт; не делай все проекты нарочито креативными по умолчанию.")
    return dedupe(rules)


def security_profile_for_project_type(project_type: str, capabilities: list[str] | None = None) -> dict[str, str]:
    capability_set = set(capabilities or [])
    needs_strict_data_rules = bool({"database", "auth", "payments"} & capability_set) or project_type in {"saas-mvp", "telegram-ai-bot", "api-integration-worker"}
    uses_integrations = bool({"api", "automation", "telegram"} & capability_set) or project_type in {"automation-script", "api-integration-worker", "telegram-ai-bot"}
    profile = {
        "security_level": "базовые-дефолты",
        "data_minimization": "не собирать лишние персональные данные и не тянуть базу без сценария",
        "secret_policy": "секреты только через env; service_role, PAT и сильные ключи не уходят в клиент",
        "query_policy": "никакой конкатенации SQL; только parameterized queries или ORM",
        "dependency_policy": "перед handoff проверить зависимости через OSV, npm audit или pip-audit по стеку",
        "logging_policy": "логи полезны для отладки, но без токенов, паролей и пользовательских секретов",
    }
    if needs_strict_data_rules:
        profile["security_level"] = "усиленный-для-данных-и-доступа"
        profile["access_policy"] = "least privilege, разделение client/server ключей, RLS или явная модель прав доступа"
    else:
        profile["access_policy"] = "не вводить сложную авторизацию без причины; если данных нет, не добавлять лишний access-layer"
    if uses_integrations:
        profile["integration_policy"] = "payload валидируется, webhook secrets документируются, retries не раскрывают чувствительные данные"
    return profile


def state_dir(workspace: Path) -> Path:
    return workspace / STATE_DIRNAME


def state_path(workspace: Path) -> Path:
    return state_dir(workspace) / "state.json"


def approval_snapshot_path(workspace: Path) -> Path:
    return state_dir(workspace) / "approval-snapshot.json"


def artifact_paths(_: Path) -> dict[str, str]:
    return {name: str(Path(STATE_DIRNAME) / name) for name in ARTIFACT_FILES}


def template_path(name: str) -> Path:
    return TEMPLATE_DIR / name


def read_template(name: str) -> str:
    return template_path(name).read_text(encoding="utf-8")


def detect_local_style_inputs(workspace: Path) -> list[dict[str, str]]:
    candidates: list[tuple[Path, str, str]] = [
        (workspace / "skill.md", "project-style-skill", "Локальный style skill в корне проекта"),
        (workspace / "SKILL.md", "project-style-skill", "Локальный style skill в корне проекта"),
        (workspace / "design-system.json", "design-system", "Локальная дизайн-система проекта"),
        (workspace / "brand-guide.md", "brand-guide", "Локальный бренд-гайд проекта"),
        (workspace / "brand-guidelines.md", "brand-guide", "Локальный бренд-гайд проекта"),
        (workspace / "moodboard.md", "moodboard", "Локальный moodboard проекта"),
        (workspace / "references" / "brand-guide.md", "brand-guide", "Бренд-гайд в папке references"),
        (workspace / "references" / "moodboard.md", "moodboard", "Moodboard в папке references"),
        (workspace / "skills" / "design" / "SKILL.md", "style-skill", "Локальный дизайн-скилл проекта"),
        (workspace / "skills" / "brand" / "SKILL.md", "style-skill", "Локальный бренд-скилл проекта"),
        (workspace / "skills" / "neobrutalism" / "SKILL.md", "style-skill", "Локальный style-skill neobrutalism"),
        (workspace / "skills" / "artistic" / "SKILL.md", "style-skill", "Локальный style-skill artistic"),
        (workspace / "skills" / "bold" / "style.md", "style-skill", "Локальный style-skill bold"),
        (workspace / "skills" / "bold" / "SKILL.md", "style-skill", "Локальный style-skill bold"),
    ]
    detected: list[dict[str, str]] = []
    seen: set[str] = set()
    for path, kind, label in candidates:
        if not path.exists():
            continue
        path_str = str(path)
        if path_str in seen:
            continue
        seen.add(path_str)
        detected.append({"type": kind, "path": path_str, "label": label})
    return detected


def design_profile_for_project_type(
    project_type: str,
    capabilities: list[str] | None = None,
    style_inputs: list[dict[str, str]] | None = None,
    content_language: str = "ru",
) -> dict[str, Any]:
    capability_set = set(capabilities or [])
    has_external_style = bool(style_inputs)
    profile: dict[str, Any] = {
        "visual_intensity": "выразительный",
        "composition_mode": "несимметричный, но контролируемый",
        "shape_language": "сдержанный",
        "allow_complex_shapes": False,
        "allow_bold_art_direction": False,
        "style_source_policy": "использовать внешние style-файлы как ориентир, а не как шаблон",
        "font_policy": "подбирать шрифты под язык контента, а не только по красоте",
    }

    if project_type == "landing-page":
        profile.update(
            {
                "visual_intensity": "выразительный",
                "composition_mode": "асимметричный продуктовый постер",
                "shape_language": "редакционный или органичный по ситуации",
                "allow_complex_shapes": True,
            }
        )
    elif project_type in {"saas-mvp", "general-web-product"}:
        profile.update(
            {
                "visual_intensity": "сдержанный",
                "composition_mode": "product-first с сильной иерархией",
                "shape_language": "структурный, без визуального шума",
            }
        )
    elif project_type == "telegram-ai-bot":
        profile.update(
            {
                "visual_intensity": "спокойный",
                "composition_mode": "компактный и утилитарный",
                "shape_language": "минимальный",
            }
        )
    elif project_type in {"automation-script", "api-integration-worker"}:
        profile.update(
            {
                "visual_intensity": "спокойный",
                "composition_mode": "служебный и объяснимый",
                "shape_language": "минимальный",
            }
        )

    if "marketing" in capability_set or project_type == "landing-page":
        profile["allow_bold_art_direction"] = True
    if has_external_style:
        profile["style_input_detected"] = True
        profile["allow_complex_shapes"] = profile["allow_complex_shapes"] or any(
            "neobrutalism" in item.get("path", "").lower() or "artistic" in item.get("path", "").lower() or "bold" in item.get("path", "").lower()
            for item in style_inputs or []
        )
    if content_language == "ru":
        profile["font_support"] = "обязательна кириллица для display и body шрифтов"
        profile["font_examples"] = "Manrope, Onest, Golos Text, IBM Plex Sans, Literata, Merriweather"
    else:
        profile["font_support"] = "латиница обязательна; декоративные гарнитуры допустимы только при нормальной читаемости"
    return profile


def load_knowledge_index() -> dict[str, Any]:
    return json.loads(KNOWLEDGE_INDEX_PATH.read_text(encoding="utf-8"))


def path_from_plugin_relative(path: str) -> Path:
    normalized = path[2:] if path.startswith("./") else path
    return PLUGIN_ROOT / normalized


def _project_match_scores(text: str) -> list[tuple[str, int]]:
    scores: list[tuple[str, int]] = []
    for project_type, tokens in PROJECT_TYPE_RULES:
        score = sum(1 for token in tokens if token in text)
        if score > 0:
            scores.append((project_type, score))
    return scores


def infer_content_language(*parts: str) -> str:
    text = " ".join(part for part in parts if part)
    if any("\u0400" <= char <= "\u04FF" for char in text):
        return "ru"
    return "en"


def infer_project_profile(
    idea: str,
    explicit: str | None = None,
    existing_secondary: list[str] | None = None,
    existing_capabilities: list[str] | None = None,
) -> dict[str, list[str] | str]:
    text = (idea or "").lower()
    matches = _project_match_scores(text)
    sorted_matches = sorted(matches, key=lambda item: (-item[1], PROJECT_TYPES.index(item[0])))

    if explicit:
        primary = explicit
    elif any(token in text for token in ("telegram", "телеграм", "telegraf")) and any(token in text for token in ("bot", "бот", "чат-бот")):
        primary = "telegram-ai-bot"
    elif sorted_matches:
        primary = sorted_matches[0][0]
    else:
        primary = "general-web-product"

    secondary = dedupe(
        (existing_secondary or [])
        + [project_type for project_type, _score in sorted_matches if project_type != primary]
    )[:3]

    detected_capabilities = [capability for capability, tokens in CAPABILITY_RULES if any(token in text for token in tokens)]
    if primary == "telegram-ai-bot":
        detected_capabilities.append("telegram")
    if primary == "landing-page":
        detected_capabilities.append("marketing")
    if primary == "automation-script":
        detected_capabilities.append("automation")
    if primary == "api-integration-worker":
        detected_capabilities.extend(["api", "automation"])
    if primary == "saas-mvp":
        detected_capabilities.extend(["dashboard", "auth"])
    if secondary and any(item in {"saas-mvp", "general-web-product", "landing-page"} for item in secondary):
        detected_capabilities.append("dashboard")

    capabilities = dedupe((existing_capabilities or []) + detected_capabilities)
    return {
        "primary": primary,
        "secondary_archetypes": secondary,
        "capabilities": capabilities,
    }


def infer_project_type(idea: str, explicit: str | None = None) -> str:
    return str(infer_project_profile(idea, explicit)["primary"])


def stack_for_project_type(project_type: str) -> dict[str, Any]:
    matrix: dict[str, dict[str, Any]] = {
        "landing-page": {
            "framework": "Astro",
            "ui_strategy": "custom-sections-first",
            "component_library": "minimal-forms-and-dialogs-only",
            "database": "none-unless-real-data-is-needed",
        },
        "saas-mvp": {
            "framework": "Next.js",
            "ui_strategy": "shadcn-ui-primitives-with-custom-visual-layer",
            "database": "Supabase/Postgres-when-data-or-auth-is-real",
            "auth": "required-when-user-accounts-exist",
        },
        "telegram-ai-bot": {
            "runtime": "Node.js",
            "bot_framework": "Telegraf",
            "http_layer": "Hono",
            "database": "Supabase/Postgres-when-user-state-or-history-is-real",
            "navigation_pattern": "single-message-inline-navigation",
        },
        "automation-script": {
            "runtime": "Python",
            "execution_mode": "cli-or-scheduled-task",
            "database": "none-unless-durable-state-is-real",
            "safety": "dry-run-first-when-side-effects-exist",
        },
        "api-integration-worker": {
            "runtime": "Node.js",
            "server_layer": "Hono-or-repo-native-equivalent",
            "database": "optional-when-durable-state-or-dedup-is-needed",
            "safety": "retry-backoff-and-idempotency-aware",
        },
        "general-web-product": {
            "framework": "Next.js",
            "ui_strategy": "custom-ui-with-focused-primitives",
            "database": "optional",
        },
    }
    return matrix.get(project_type, matrix["general-web-product"]).copy()


def stack_for_project_profile(project_type: str, capabilities: list[str]) -> dict[str, Any]:
    stack = stack_for_project_type(project_type)
    capability_set = set(capabilities)
    if "ai" in capability_set:
        stack.setdefault("ai_provider", "OpenAI-compatible")
    if "auth" in capability_set and "auth" not in stack:
        stack["auth"] = "required-for-protected-routes"
    if "database" in capability_set and stack.get("database") == "optional":
        stack["database"] = "recommended-because-capability-requires-state"
    if "dashboard" in capability_set and project_type in {"telegram-ai-bot", "automation-script", "api-integration-worker"}:
        stack["operator_ui"] = "web-dashboard-if-operator-workflow-is-real"
    if "payments" in capability_set:
        stack["payments"] = "Stripe-or-repo-native-provider"
    return stack


def roles_for_project_type(project_type: str) -> list[str]:
    base_roles = [
        "project-discovery",
        "solution-architect",
        "design-director",
        "qa-reviewer",
        "deploy-operator",
    ]
    matrix = {
        "landing-page": ["frontend-builder"],
        "saas-mvp": ["frontend-builder", "backend-builder", "database-designer"],
        "telegram-ai-bot": ["backend-builder", "database-designer"],
        "automation-script": ["automation-builder"],
        "api-integration-worker": ["backend-builder", "automation-builder", "database-designer"],
        "general-web-product": ["frontend-builder", "backend-builder"],
    }
    return base_roles + matrix.get(project_type, matrix["general-web-product"])


def roles_for_project_profile(project_type: str, secondary_archetypes: list[str], capabilities: list[str]) -> list[str]:
    roles = roles_for_project_type(project_type)
    if any(item in {"saas-mvp", "general-web-product", "landing-page"} for item in secondary_archetypes):
        roles.append("frontend-builder")
    if any(item in {"telegram-ai-bot", "api-integration-worker"} for item in secondary_archetypes):
        roles.append("backend-builder")
    if "database" in capabilities or "auth" in capabilities or "payments" in capabilities:
        roles.append("database-designer")
    if "dashboard" in capabilities:
        roles.append("frontend-builder")
    if "automation" in capabilities:
        roles.append("automation-builder")
    return dedupe(roles)


def select_pack_ids(project_type: str, phase: str, secondary_archetypes: list[str] | None = None, capabilities: list[str] | None = None) -> list[str]:
    index = load_knowledge_index()
    applicable_types = {project_type, *(secondary_archetypes or [])}
    selected: list[str] = []
    for pack in index.get("packs", []):
        pack_types = set(pack.get("project_types", []))
        pack_phases = set(pack.get("phases", []))
        if not applicable_types.intersection(pack_types):
            continue
        if pack_phases and phase not in pack_phases:
            continue
        required_capabilities = set(pack.get("capabilities", []))
        if required_capabilities and not required_capabilities.intersection(set(capabilities or [])):
            continue
        selected.append(pack["id"])
    return dedupe(selected)


def recommended_skills_for_project_type(project_type: str, secondary_archetypes: list[str] | None = None, capabilities: list[str] | None = None) -> list[str]:
    index = load_knowledge_index()
    skills = list(index.get("recommended_skills", {}).get(project_type, []))
    for archetype in secondary_archetypes or []:
        skills.extend(index.get("recommended_skills", {}).get(archetype, []))
    for capability in capabilities or []:
        skills.extend(CAPABILITY_SKILLS.get(capability, []))
    return dedupe(skills)


def quality_gates_for_project_type(project_type: str, secondary_archetypes: list[str] | None = None, capabilities: list[str] | None = None) -> list[str]:
    index = load_knowledge_index()
    gates = list(index.get("quality_gates", {}).get(project_type, []))
    for archetype in secondary_archetypes or []:
        gates.extend(index.get("quality_gates", {}).get(archetype, []))
    for capability in capabilities or []:
        gates.extend(CAPABILITY_QUALITY_GATES.get(capability, []))
    return dedupe(gates)


def verification_required_for_project_type(project_type: str, secondary_archetypes: list[str] | None = None, capabilities: list[str] | None = None) -> list[str]:
    verification_matrix = {
        "landing-page": ["desktop-ui-review", "mobile-ui-review", "cta-route-check", "seo-metadata-check"],
        "saas-mvp": ["auth-flow-smoke-test", "permissions-review", "data-flow-check", "env-audit", "dependency-vulnerability-check"],
        "telegram-ai-bot": ["manual-telegram-walkthrough", "callback-flow-check", "secret-audit", "webhook-readiness", "dependency-vulnerability-check"],
        "automation-script": ["dry-run-check", "logs-review", "failure-path-check", "env-audit", "dependency-vulnerability-check"],
        "api-integration-worker": ["payload-validation-check", "retry-policy-check", "idempotency-check", "provider-secret-audit", "dependency-vulnerability-check"],
        "general-web-product": ["core-flow-smoke-test", "mobile-ui-review", "env-audit"],
    }
    items = list(verification_matrix.get(project_type, verification_matrix["general-web-product"]))
    for archetype in secondary_archetypes or []:
        items.extend(verification_matrix.get(archetype, []))
    for capability in capabilities or []:
        items.extend(CAPABILITY_VERIFICATION.get(capability, []))
    return dedupe(items)


def playbook_for_project_type(project_type: str) -> str:
    index = load_knowledge_index()
    return index.get("playbooks", {}).get(project_type, "./playbooks/saas-mvp.md")


def supporting_playbooks_for_types(secondary_archetypes: list[str]) -> list[str]:
    index = load_knowledge_index()
    return dedupe(
        [index.get("playbooks", {}).get(archetype, "") for archetype in secondary_archetypes if index.get("playbooks", {}).get(archetype, "")]
    )


def execution_strategy_for_project_type(project_type: str, secondary_archetypes: list[str] | None = None, capabilities: list[str] | None = None) -> str:
    if secondary_archetypes:
        return "составной-проект-с-поэтапной-сборкой-и-замороженным-планом"
    if project_type in {"telegram-ai-bot", "automation-script", "api-integration-worker"}:
        return "последовательные-роли-с-guardrails-на-надежность"
    if "payments" in set(capabilities or []) or "auth" in set(capabilities or []):
        return "последовательные-роли-с-guardrails-на-доступ-и-данные"
    return "последовательные-роли-с-дизайн-и-smoke-gates"


def orchestration_mode_for_project_type(project_type: str, secondary_archetypes: list[str] | None = None, capabilities: list[str] | None = None) -> str:
    capability_set = set(capabilities or [])
    if secondary_archetypes:
        return "delegated"
    if len(capability_set.intersection({"dashboard", "database", "auth", "automation", "api"})) >= 2:
        return "delegated"
    if project_type in {"saas-mvp", "api-integration-worker"} and len(capability_set) >= 2:
        return "delegated"
    return "solo"


def delegation_targets_for_project_type(project_type: str, secondary_archetypes: list[str] | None = None, capabilities: list[str] | None = None) -> list[dict[str, str]]:
    targets: list[dict[str, str]] = []
    capability_set = set(capabilities or [])
    if project_type in {"landing-page", "general-web-product", "saas-mvp"} or "dashboard" in capability_set:
        targets.append(
            {
                "role": "frontend-builder",
                "ownership": "UI, states, responsive behavior, design implementation",
                "spawn_when": "Когда backend-контракты уже понятны и UI можно собирать независимо.",
            }
        )
    if project_type in {"saas-mvp", "telegram-ai-bot", "api-integration-worker"} or {"api", "telegram"} & capability_set:
        targets.append(
            {
                "role": "backend-builder",
                "ownership": "API, handlers, webhook logic, integrations, validation, logs",
                "spawn_when": "Когда продуктовый маршрут уже заморожен и нужен отдельный server-side поток работы.",
            }
        )
    if "database" in capability_set or "auth" in capability_set or "payments" in capability_set:
        targets.append(
            {
                "role": "database-designer",
                "ownership": "schema, ownership, access model, migrations, data constraints",
                "spawn_when": "Когда durable state действительно нужен и можно отдельно спроектировать data layer.",
            }
        )
    if project_type == "automation-script" or "automation" in capability_set:
        targets.append(
            {
                "role": "automation-builder",
                "ownership": "scripts, workers, dry-run, retries, safe side effects",
                "spawn_when": "Когда automation pipeline можно строить отдельно от UI.",
            }
        )
    targets.append(
        {
            "role": "qa-reviewer",
            "ownership": "findings, verification report, scorecard, release readiness",
            "spawn_when": "Когда реализация уже есть и review может идти параллельно с финальным полишем.",
        }
    )
    return dedupe_targets(targets)


def dedupe_targets(targets: list[dict[str, str]]) -> list[dict[str, str]]:
    seen: set[str] = set()
    ordered: list[dict[str, str]] = []
    for target in targets:
        role = target.get("role")
        if not role or role in seen:
            continue
        seen.add(role)
        ordered.append(target)
    return ordered


def scope_mode_for_project_type(project_type: str, quality_mode: str = "сбалансированно") -> str:
    if quality_mode == "быстро":
        return "жесткий-mvp"
    if project_type in {"telegram-ai-bot", "automation-script", "api-integration-worker"}:
        return "один-главный-сценарий-и-минимум-лишнего"
    return "mvp-с-отдельным-блоком-рекомендаций"


def recommendation_policy_for_project_type(project_type: str) -> str:
    if project_type in {"landing-page", "general-web-product"}:
        return "советуй-улучшения-отдельно-от-MVP-и-не-включай-их-в-первую-реализацию-без-подтверждения"
    return "предлагай-усиления-как-отложенные-идеи-и-не-реализуй-их-молча"


def scope_guardrails_for_project_type(project_type: str, capabilities: list[str] | None = None) -> list[str]:
    guardrails = list(SCOPE_GUARDRAILS_BASE)
    if project_type == "saas-mvp":
        guardrails.append("Не добавляй auth, billing, роли и админку одновременно, если главный сценарий можно проверить без этого.")
    if project_type == "telegram-ai-bot":
        guardrails.append("Не добавляй базу, AI, админку и панель операторов одновременно, если бот можно запустить без них.")
    if project_type == "landing-page":
        guardrails.append("Не превращай лендинг в мини-CMS или SaaS без отдельного решения пользователя.")
    if "payments" in set(capabilities or []):
        guardrails.append("Платежи не должны тянуть за собой лишнюю инфраструктуру, если можно начать с sandbox-сценария.")
    return dedupe(guardrails)


def security_guardrails_for_project_type(project_type: str, capabilities: list[str] | None = None) -> list[str]:
    capability_set = set(capabilities or [])
    guardrails = list(SECURITY_GUARDRAILS_BASE)
    if {"database", "api"} & capability_set or project_type in {"saas-mvp", "api-integration-worker", "telegram-ai-bot"}:
        guardrails.extend(
            [
                "SQL строится только через parameterized queries или ORM; строковая конкатенация считается провалом.",
                "Права доступа к данным описываются явно: кто что читает, пишет и удаляет.",
            ]
        )
    if {"database", "auth", "payments"} & capability_set:
        guardrails.extend(
            [
                "Service role, PAT и другие сильные ключи не попадают в браузер, бота или публичный фронтенд.",
                "Если есть пользовательские данные, для первой версии всё равно нужен путь к least privilege и RLS/ограничениям доступа.",
            ]
        )
    if project_type in {"automation-script", "api-integration-worker"} or "automation" in capability_set:
        guardrails.append("Перед handoff должна быть хотя бы одна проверка зависимостей и уязвимостей проекта.")
    return dedupe(guardrails)


def default_plan_variants(project_type: str, capabilities: list[str] | None = None) -> list[dict[str, Any]]:
    capability_set = set(capabilities or [])
    minimal_focus = "один главный рабочий сценарий"
    optimal_focus = "основной сценарий плюс базовая надежность и понятный UX"
    buffer_focus = "основной сценарий плюс 1-2 заранее полезных улучшения без расползания в большой продукт"

    if project_type == "telegram-ai-bot":
        minimal_focus = "одно меню, один маршрут пользователя и минимальный набор команд"
        optimal_focus = "одно меню, устойчивые callback-сценарии, базовые проверки и готовность к webhook"
        buffer_focus = "оптимальный вариант плюс 1 полезное улучшение, например AI-ответы или простое хранение состояния"
    elif project_type == "landing-page":
        minimal_focus = "один продающий сценарий с понятным CTA"
        optimal_focus = "продающий сценарий, мобильная полировка и базовое SEO"
        buffer_focus = "оптимальный вариант плюс 1-2 усиления, например анимации или улучшенная форма"
    elif project_type == "saas-mvp":
        minimal_focus = "один ключевой сценарий в кабинете без лишних подсистем"
        optimal_focus = "ключевой сценарий, базовые данные, права доступа и понятные состояния интерфейса"
        buffer_focus = "оптимальный вариант плюс 1 оправданное усиление, например простая аналитика или роли"
    elif project_type in {"automation-script", "api-integration-worker"}:
        minimal_focus = "один рабочий pipeline без лишней инфраструктуры"
        optimal_focus = "рабочий pipeline, логирование, dry-run или retry-поведение"
        buffer_focus = "оптимальный вариант плюс 1 заранее полезное улучшение, например уведомления или дедупликация"

    if "payments" in capability_set:
        buffer_focus += "; платежи только в sandbox-режиме"

    return [
        {
            "id": "минимум",
            "title": "Минимум",
            "summary": minimal_focus,
            "when_to_choose": "Когда важно как можно быстрее запустить первую рабочую версию.",
        },
        {
            "id": "оптимально",
            "title": "Оптимально",
            "summary": optimal_focus,
            "when_to_choose": "Когда нужен лучший баланс скорости, понятности и качества.",
        },
        {
            "id": "с-запасом",
            "title": "С запасом",
            "summary": buffer_focus,
            "when_to_choose": "Когда можно добавить 1-2 заранее полезных улучшения, но не уходить в переусложнение.",
        },
    ]


def cross_checks_for_project_type(project_type: str, secondary_archetypes: list[str] | None = None, capabilities: list[str] | None = None) -> list[str]:
    matrix = {
        "landing-page": [
            "solution-architect -> design-director: структура не расползается",
            "design-director -> frontend-builder: визуальное направление не стало generic",
            "qa-reviewer -> deploy-operator: mobile и CTA проверены до handoff",
        ],
        "saas-mvp": [
            "solution-architect -> database-designer: данные и права доступа согласованы",
            "backend-builder -> frontend-builder: UI не опирается на несуществующий API",
            "database-designer -> qa-reviewer: ownership и защита данных проверены",
        ],
        "telegram-ai-bot": [
            "solution-architect -> backend-builder: маршрут пользователя и callback-логика совпадают",
            "backend-builder -> qa-reviewer: single-message navigation не ломает ручной сценарий",
            "deploy-operator -> qa-reviewer: webhook и секреты готовы к публикации",
        ],
        "automation-script": [
            "solution-architect -> automation-builder: входы и выходы описаны явно",
            "automation-builder -> qa-reviewer: dry-run и логи действительно работают",
            "deploy-operator -> qa-reviewer: env и запуск по расписанию документированы",
        ],
        "api-integration-worker": [
            "solution-architect -> backend-builder: контракты внешнего API описаны",
            "backend-builder -> automation-builder: retry и idempotency не конфликтуют",
            "qa-reviewer -> deploy-operator: provider secrets и verification route задокументированы",
        ],
        "general-web-product": [
            "solution-architect -> frontend-builder: зона ответственности frontend и backend разделена",
            "backend-builder -> frontend-builder: UI не опирается на выдуманную серверную логику",
            "qa-reviewer -> deploy-operator: основные сценарии и env подтверждены",
        ],
    }
    checks = list(matrix.get(project_type, matrix["general-web-product"]))
    if "auth" in set(capabilities or []) or "database" in set(capabilities or []):
        checks.append("database-designer -> deploy-operator: правила доступа и env по данным согласованы")
    if secondary_archetypes:
        checks.append("autonomous-project-orchestrator -> все роли: вторичные архетипы не потеряны при реализации")
    return dedupe(checks)


def phase_context_targets(phase: str, token_mode: str = "ultra") -> list[str]:
    if token_mode == "ultra":
        matrix = {
            "discovery": [
                "phase-card.md",
                "ultra-context.md",
                "discovery-questionnaire.md",
                "state.json",
                "context-bundle.md",
            ],
            "planning": [
                "phase-card.md",
                "ultra-context.md",
                "project-brief.md",
                "state.json",
                "context-bundle.md",
                "product-intelligence.md",
            ],
            "approval": [
                "phase-card.md",
                "ultra-context.md",
                "implementation-plan.md",
                "state.json",
                "context-bundle.md",
                "design-direction.md",
            ],
            "execution": [
                "phase-card.md",
                "ultra-context.md",
                "implementation-plan.md",
                "state.json",
                "context-bundle.md",
                "active-context.md",
            ],
            "verification": [
                "phase-card.md",
                "ultra-context.md",
                "verification-report.md",
                "state.json",
                "context-bundle.md",
                "implementation-plan.md",
            ],
            "handoff": [
                "phase-card.md",
                "ultra-context.md",
                "final-handoff.md",
                "state.json",
                "context-bundle.md",
                "env-secrets-checklist.md",
            ],
        }
        return matrix.get(phase, matrix["discovery"])

    matrix = {
        "discovery": [
            "context-bundle.md",
            "discovery-questionnaire.md",
            "project-brief.md",
            "product-intelligence.md",
            "state.json",
        ],
        "planning": [
            "context-bundle.md",
            "project-brief.md",
            "product-intelligence.md",
            "product-context.md",
            "tech-context.md",
            "state.json",
        ],
        "approval": [
            "context-bundle.md",
            "implementation-plan.md",
            "design-direction.md",
            "state.json",
        ],
        "execution": [
            "context-bundle.md",
            "implementation-plan.md",
            "active-context.md",
            "progress.md",
            "state.json",
        ],
        "verification": [
            "context-bundle.md",
            "implementation-plan.md",
            "execution-log.md",
            "verification-report.md",
            "state.json",
        ],
        "handoff": [
            "context-bundle.md",
            "verification-report.md",
            "scorecard.md",
            "env-secrets-checklist.md",
            "state.json",
        ],
    }
    return matrix.get(phase, matrix["discovery"])


def doc_open_triggers_for_phase(phase: str, project_type: str, capabilities: list[str] | None = None) -> list[str]:
    capability_set = set(capabilities or [])
    matrix = {
        "discovery": [
            "только если ответ пользователя меняет scope первой версии",
            "только если без уточнения архетипа нельзя выбрать playbook",
            "только если короткой сводки уже недостаточно для следующего вопроса",
        ],
        "planning": [
            "только если нужно обосновать выбор стека или базы данных",
            "только если активный knowledge pack влияет на архитектурное решение",
            "только если без документа нельзя собрать реалистичный MVP-план",
        ],
        "approval": [
            "только если нужно проверить, что план и дизайн-направление не конфликтуют",
            "только если есть риск молча расширить scope",
            "только если пользователь просит подробное объяснение решения",
        ],
        "execution": [
            "только если активная роль реально упёрлась в контракт, API или data model",
            "только если без документа нельзя безопасно менять код",
            "только если текущий файл не даёт ответа на следующий инженерный шаг",
        ],
        "verification": [
            "только если нужно подтвердить конкретный quality gate",
            "только если без документа нельзя воспроизвести failure-path",
            "только если handoff рискует остаться без доказательства проверки",
        ],
        "handoff": [
            "только если нужно уточнить ручной шаг, секрет или порядок запуска",
            "только если без документа нельзя объяснить остаточный риск",
            "только если пользователь просит более подробный итог",
        ],
    }
    triggers = list(matrix.get(phase, matrix["discovery"]))
    if "ai" in capability_set and phase in {"planning", "execution"}:
        triggers.append("только если нужна документация конкретного AI-провайдера для активной интеграции")
    if {"auth", "database"} & capability_set and phase in {"planning", "execution", "verification"}:
        triggers.append("только если нужно проверить права доступа, схему данных или security boundary")
    if ({"api", "payments", "automation"} & capability_set or project_type in {"automation-script", "api-integration-worker"}) and phase in {"execution", "verification", "handoff"}:
        triggers.append("только если нужно понять, как проверять зависимости, секреты, webhook-подписи или уязвимости пакетов")
    if project_type == "telegram-ai-bot" and phase in {"execution", "verification"}:
        triggers.append("только если нужно уточнить callback/navigation-поведение Telegram-сценария")
    return dedupe(triggers)


def doc_read_policy_for_phase(phase: str) -> str:
    policies = {
        "discovery": "summary-first, quiz-first, docs-last",
        "planning": "summary-first, decision-driven docs",
        "approval": "locked-plan-first, no speculative reading",
        "execution": "task-first, code-first, docs-on-blocker",
        "verification": "evidence-first, docs-for-proof-only",
        "handoff": "final-state-first, docs-for-manual-steps-only",
    }
    return policies.get(phase, "summary-first, docs-on-demand")


def active_role_contracts(roles: list[str]) -> dict[str, Any]:
    return {role: ROLE_CONTRACTS[role] for role in roles if role in ROLE_CONTRACTS}


def active_deliverable_templates(roles: list[str]) -> dict[str, list[str]]:
    return {role: DELIVERABLE_TEMPLATES[role] for role in roles if role in DELIVERABLE_TEMPLATES}


def packet_inputs_for_role(role: str, phase_context_targets: list[str]) -> list[str]:
    shared = ["phase-card.md", "ultra-context.md", "state.json"]
    role_specific = {
        "frontend-builder": ["implementation-plan.md", "design-direction.md", "active-context.md"],
        "backend-builder": ["implementation-plan.md", "tech-context.md", "active-context.md"],
        "database-designer": ["implementation-plan.md", "product-context.md", "tech-context.md"],
        "automation-builder": ["implementation-plan.md", "tech-context.md", "active-context.md"],
        "qa-reviewer": ["implementation-plan.md", "execution-log.md", "verification-report.md", "env-secrets-checklist.md"],
    }
    return dedupe(shared + role_specific.get(role, []) + phase_context_targets[:2])


def write_scope_for_role(role: str) -> list[str]:
    mapping = {
        "frontend-builder": ["ui files", "components", "pages", "styles", "execution-log.md"],
        "backend-builder": ["server handlers", "api routes", "integration logic", "execution-log.md"],
        "database-designer": ["data-model.md", "migrations", "schema docs", "execution-log.md"],
        "automation-builder": ["scripts", "workers", "schedulers", "execution-log.md"],
        "qa-reviewer": ["verification-report.md", "scorecard.md"],
    }
    return mapping.get(role, ["execution-log.md"])


def delegation_packets_for_roles(
    roles: list[str],
    phase_context_targets: list[str],
    role_contracts: dict[str, Any],
    deliverable_templates: dict[str, list[str]],
) -> list[dict[str, Any]]:
    packets: list[dict[str, Any]] = []
    for role in roles:
        if role not in {"frontend-builder", "backend-builder", "database-designer", "automation-builder", "qa-reviewer"}:
            continue
        contract = role_contracts.get(role, {})
        packets.append(
            {
                "role": role,
                "mission": contract.get("mission", ""),
                "read_first": packet_inputs_for_role(role, phase_context_targets),
                "write_scope": write_scope_for_role(role),
                "must_return": {
                    "deliverables": deliverable_templates.get(role, []),
                    "handoff_format": [
                        "что готово",
                        "что не готово",
                        "какие решения заморожены",
                        "какие риски остались",
                        "что читать следующей роли",
                    ],
                },
                "stop_if": contract.get("forbidden", []),
            }
        )
    return packets


def _task_status_for_phase(task_id: str, phase: str) -> str:
    if task_id == phase:
        return "in_progress"
    if PHASE_INDEX.get(task_id, -1) < PHASE_INDEX.get(phase, 0):
        return "done"
    return "pending"


def merge_tasks(existing_tasks: list[dict[str, str]] | None, defaults: list[dict[str, str]]) -> list[dict[str, str]]:
    existing_by_id = {task.get("id"): task for task in existing_tasks or [] if task.get("id")}
    merged: list[dict[str, str]] = []
    for task in defaults:
        existing = existing_by_id.get(task["id"], {})
        status = task["status"]
        if existing.get("status") == "done" and status == "pending":
            status = "done"
        merged.append(
            {
                "id": task["id"],
                "title": task["title"],
                "owner": existing.get("owner", task["owner"]),
                "status": status,
            }
        )
    return merged


def default_tasks(project_type: str, phase: str) -> list[dict[str, str]]:
    execution_owner = {
        "telegram-ai-bot": "backend-builder",
        "automation-script": "automation-builder",
        "api-integration-worker": "automation-builder",
    }.get(project_type, "frontend-builder")
    tasks = [
        {
            "id": "discovery",
            "title": "Провести понятный discovery-квиз и зафиксировать scope первой версии",
            "owner": "project-discovery",
            "status": _task_status_for_phase("discovery", phase),
        },
        {
            "id": "planning",
            "title": "Собрать план реализации, выбрать knowledge packs и зафиксировать маршрут",
            "owner": "solution-architect",
            "status": _task_status_for_phase("planning", phase),
        },
        {
            "id": "approval",
            "title": "Получить одно явное подтверждение плана до начала продуктовых правок",
            "owner": "autonomous-project-orchestrator",
            "status": _task_status_for_phase("approval", phase),
        },
        {
            "id": "execution",
            "title": f"Реализовать MVP типа {project_type} по выбранному маршруту",
            "owner": execution_owner,
            "status": _task_status_for_phase("execution", phase),
        },
        {
            "id": "verification",
            "title": "Провести QA-проверку и пройти критерии качества",
            "owner": "qa-reviewer",
            "status": _task_status_for_phase("verification", phase),
        },
        {
            "id": "handoff",
            "title": "Подготовить отчёт по проверке, чеклист секретов и финальный handoff",
            "owner": "deploy-operator",
            "status": _task_status_for_phase("handoff", phase),
        },
    ]
    return tasks


def default_approval_snapshot(workspace: Path) -> dict[str, Any]:
    return {
        "locked": False,
        "artifact": str(Path(STATE_DIRNAME) / "approval-snapshot.json"),
        "locked_fields": list(PLAN_LOCK_FIELDS),
    }


def default_state(
    workspace: Path,
    project_type: str,
    secondary_archetypes: list[str],
    capabilities: list[str],
    goal: str,
    audience: str,
    phase: str,
) -> dict[str, Any]:
    token_mode = "ultra"
    content_language = infer_content_language(goal, audience)
    style_inputs = detect_local_style_inputs(workspace)
    selected_packs = select_pack_ids(project_type, phase, secondary_archetypes, capabilities)
    active_roles = roles_for_project_profile(project_type, secondary_archetypes, capabilities)
    role_contracts = active_role_contracts(active_roles)
    deliverable_templates = active_deliverable_templates(active_roles)
    phase_targets = phase_context_targets(phase, token_mode)
    state: dict[str, Any] = {
        "project_type": project_type,
        "project_archetype": project_type,
        "secondary_archetypes": secondary_archetypes,
        "capabilities": capabilities,
        "token_mode": token_mode,
        "quality_mode": "сбалансированно",
        "content_language": content_language,
        "goal": goal,
        "audience": audience,
        "plan_variants": default_plan_variants(project_type, capabilities),
        "selected_plan_variant": "оптимально",
        "beginner_explanation_mode": "включен",
        "phase": phase,
        "phase_history": [phase],
        "answers": {},
        "assumptions": [],
        "selected_stack": stack_for_project_profile(project_type, capabilities),
        "active_roles": active_roles,
        "recommended_skills": recommended_skills_for_project_type(project_type, secondary_archetypes, capabilities),
        "selected_packs": selected_packs,
        "playbook": playbook_for_project_type(project_type),
        "supporting_playbooks": supporting_playbooks_for_types(secondary_archetypes),
        "quality_gates": quality_gates_for_project_type(project_type, secondary_archetypes, capabilities),
        "verification_required": verification_required_for_project_type(project_type, secondary_archetypes, capabilities),
        "approval_status": "pending" if phase in {"discovery", "planning", "approval"} else "approved",
        "approval_snapshot": default_approval_snapshot(Path(".")),
        "execution_strategy": execution_strategy_for_project_type(project_type, secondary_archetypes, capabilities),
        "orchestration_mode": orchestration_mode_for_project_type(project_type, secondary_archetypes, capabilities),
        "delegation_policy": DELEGATION_POLICY,
        "delegation_targets": delegation_targets_for_project_type(project_type, secondary_archetypes, capabilities),
        "scope_mode": scope_mode_for_project_type(project_type),
        "recommendation_policy": recommendation_policy_for_project_type(project_type),
        "scope_guardrails": scope_guardrails_for_project_type(project_type, capabilities),
        "role_system_version": ROLE_SYSTEM_VERSION,
        "souls_version": SOULS_VERSION,
        "design_profile": design_profile_for_project_type(project_type, capabilities, style_inputs, content_language),
        "style_inputs": style_inputs,
        "project_dna": project_dna_for_project_type(project_type, capabilities),
        "security_profile": security_profile_for_project_type(project_type, capabilities),
        "security_guardrails": security_guardrails_for_project_type(project_type, capabilities),
        "uniqueness_rules": uniqueness_rules_for_project_type(project_type, capabilities),
        "deliverable_templates": deliverable_templates,
        "role_contracts": role_contracts,
        "handoff_rules": list(HANDOFF_RULES),
        "phase_context_targets": phase_targets,
        "doc_read_policy": doc_read_policy_for_phase(phase),
        "doc_open_triggers": doc_open_triggers_for_phase(phase, project_type, capabilities),
        "cross_checks": cross_checks_for_project_type(project_type, secondary_archetypes, capabilities),
        "delegation_packets": delegation_packets_for_roles(active_roles, phase_targets, role_contracts, deliverable_templates),
        "user_overrides": {},
        "tasks": default_tasks(project_type, phase),
        "blocked_on_user": False,
        "manual_inputs": [],
        "artifacts": artifact_paths(workspace),
    }
    return state


def load_state(workspace: Path) -> dict[str, Any]:
    return json.loads(state_path(workspace).read_text(encoding="utf-8"))


def save_state(workspace: Path, state: dict[str, Any]) -> None:
    path = state_path(workspace)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(state, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def read_approval_snapshot(workspace: Path) -> dict[str, Any]:
    path = approval_snapshot_path(workspace)
    if not path.exists():
        return {}
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return {}


def freeze_approval_snapshot(workspace: Path, state: dict[str, Any]) -> dict[str, Any]:
    snapshot = {
        "locked": True,
        "project_type": state.get("project_type"),
        "project_archetype": state.get("project_archetype"),
        "secondary_archetypes": state.get("secondary_archetypes", []),
        "capabilities": state.get("capabilities", []),
        "selected_stack": state.get("selected_stack", {}),
        "active_roles": state.get("active_roles", []),
        "recommended_skills": state.get("recommended_skills", []),
        "selected_packs": state.get("selected_packs", []),
        "playbook": state.get("playbook", ""),
        "supporting_playbooks": state.get("supporting_playbooks", []),
        "quality_gates": state.get("quality_gates", []),
        "verification_required": state.get("verification_required", []),
        "execution_strategy": state.get("execution_strategy", ""),
        "quality_mode": state.get("quality_mode", "сбалансированно"),
        "goal": state.get("goal", ""),
        "locked_fields": list(PLAN_LOCK_FIELDS),
    }
    path = approval_snapshot_path(workspace)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(snapshot, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    state["approval_snapshot"] = {
        "locked": True,
        "artifact": str(Path(STATE_DIRNAME) / "approval-snapshot.json"),
        "locked_fields": list(PLAN_LOCK_FIELDS),
    }
    state["approval_status"] = "approved"
    return snapshot


def merge_state_defaults(
    state: dict[str, Any],
    workspace: Path,
    *,
    goal: str = "",
    audience: str = "",
    project_type: str = "",
    phase: str = "",
) -> dict[str, Any]:
    profile = infer_project_profile(
        goal or state.get("goal", ""),
        project_type or state.get("project_type") or None,
        state.get("secondary_archetypes", []),
        state.get("capabilities", []),
    )
    resolved_project_type = str(profile["primary"])
    resolved_secondary = list(profile["secondary_archetypes"])
    resolved_capabilities = list(profile["capabilities"])
    resolved_phase = phase or state.get("phase", "discovery")
    resolved_goal = goal or state.get("goal", "")
    resolved_audience = audience or state.get("audience", "")
    resolved_content_language = infer_content_language(resolved_goal, resolved_audience)

    merged = {
        **default_state(
            workspace,
            resolved_project_type,
            resolved_secondary,
            resolved_capabilities,
            resolved_goal,
            resolved_audience,
            resolved_phase,
        ),
        **state,
    }

    if goal:
        merged["goal"] = goal
    if audience:
        merged["audience"] = audience
    if phase:
        merged["phase"] = phase
    if project_type:
        merged["project_type"] = project_type

    profile = infer_project_profile(
        merged.get("goal", ""),
        merged.get("project_type"),
        merged.get("secondary_archetypes", []),
        merged.get("capabilities", []),
    )
    merged["project_type"] = str(profile["primary"])
    merged["project_archetype"] = merged["project_type"]
    merged["secondary_archetypes"] = list(profile["secondary_archetypes"])
    merged["capabilities"] = list(profile["capabilities"])

    user_overrides = merged.get("user_overrides", {})
    if not isinstance(user_overrides, dict):
        user_overrides = {}
    merged["user_overrides"] = user_overrides

    snapshot_meta = merged.get("approval_snapshot", {})
    if not isinstance(snapshot_meta, dict):
        snapshot_meta = {}
    snapshot_data = read_approval_snapshot(workspace)
    snapshot_locked = bool(snapshot_meta.get("locked")) or bool(snapshot_data.get("locked"))

    resolved_plan_fields: dict[str, Any] = {
        "selected_stack": stack_for_project_profile(merged["project_type"], merged["capabilities"]),
        "active_roles": roles_for_project_profile(merged["project_type"], merged["secondary_archetypes"], merged["capabilities"]),
        "recommended_skills": recommended_skills_for_project_type(merged["project_type"], merged["secondary_archetypes"], merged["capabilities"]),
        "selected_packs": select_pack_ids(merged["project_type"], merged["phase"], merged["secondary_archetypes"], merged["capabilities"]),
        "playbook": playbook_for_project_type(merged["project_type"]),
        "supporting_playbooks": supporting_playbooks_for_types(merged["secondary_archetypes"]),
        "quality_gates": quality_gates_for_project_type(merged["project_type"], merged["secondary_archetypes"], merged["capabilities"]),
        "verification_required": verification_required_for_project_type(merged["project_type"], merged["secondary_archetypes"], merged["capabilities"]),
        "execution_strategy": execution_strategy_for_project_type(merged["project_type"], merged["secondary_archetypes"], merged["capabilities"]),
        "orchestration_mode": orchestration_mode_for_project_type(merged["project_type"], merged["secondary_archetypes"], merged["capabilities"]),
        "quality_mode": merged.get("quality_mode", "сбалансированно"),
        "content_language": merged.get("content_language", resolved_content_language),
        "scope_mode": scope_mode_for_project_type(merged["project_type"], merged.get("quality_mode", "сбалансированно")),
        "recommendation_policy": recommendation_policy_for_project_type(merged["project_type"]),
        "scope_guardrails": scope_guardrails_for_project_type(merged["project_type"], merged["capabilities"]),
        "plan_variants": default_plan_variants(merged["project_type"], merged["capabilities"]),
        "selected_plan_variant": merged.get("selected_plan_variant", "оптимально"),
        "beginner_explanation_mode": merged.get("beginner_explanation_mode", "включен"),
    }

    for field, default_value in resolved_plan_fields.items():
        if field in user_overrides:
            merged[field] = user_overrides[field]
            continue
        if snapshot_locked and field in snapshot_data:
            merged[field] = snapshot_data[field]
            continue
        merged[field] = default_value

    merged["token_mode"] = user_overrides.get("token_mode", merged.get("token_mode", "ultra"))
    merged["phase_context_targets"] = phase_context_targets(merged["phase"], merged["token_mode"])
    merged["doc_read_policy"] = user_overrides.get("doc_read_policy", doc_read_policy_for_phase(merged["phase"]))
    merged["doc_open_triggers"] = user_overrides.get(
        "doc_open_triggers",
        doc_open_triggers_for_phase(merged["phase"], merged["project_type"], merged["capabilities"]),
    )
    merged["role_system_version"] = user_overrides.get("role_system_version", ROLE_SYSTEM_VERSION)
    merged["souls_version"] = user_overrides.get("souls_version", SOULS_VERSION)
    detected_style_inputs = detect_local_style_inputs(workspace)
    merged["style_inputs"] = user_overrides.get("style_inputs", detected_style_inputs)
    merged["design_profile"] = user_overrides.get(
        "design_profile",
        design_profile_for_project_type(
            merged["project_type"],
            merged["capabilities"],
            merged["style_inputs"],
            merged.get("content_language", resolved_content_language),
        ),
    )
    merged["project_dna"] = user_overrides.get("project_dna", project_dna_for_project_type(merged["project_type"], merged["capabilities"]))
    merged["security_profile"] = user_overrides.get("security_profile", security_profile_for_project_type(merged["project_type"], merged["capabilities"]))
    merged["security_guardrails"] = user_overrides.get("security_guardrails", security_guardrails_for_project_type(merged["project_type"], merged["capabilities"]))
    merged["uniqueness_rules"] = user_overrides.get("uniqueness_rules", uniqueness_rules_for_project_type(merged["project_type"], merged["capabilities"]))
    merged["deliverable_templates"] = user_overrides.get("deliverable_templates", active_deliverable_templates(merged["active_roles"]))
    merged["role_contracts"] = user_overrides.get("role_contracts", active_role_contracts(merged["active_roles"]))
    merged["handoff_rules"] = user_overrides.get("handoff_rules", list(HANDOFF_RULES))
    merged["delegation_policy"] = user_overrides.get("delegation_policy", DELEGATION_POLICY)
    merged["delegation_targets"] = user_overrides.get(
        "delegation_targets",
        delegation_targets_for_project_type(merged["project_type"], merged["secondary_archetypes"], merged["capabilities"]),
    )
    merged["delegation_packets"] = user_overrides.get(
        "delegation_packets",
        delegation_packets_for_roles(
            merged["active_roles"],
            merged["phase_context_targets"],
            merged["role_contracts"],
            merged["deliverable_templates"],
        ),
    )
    merged["cross_checks"] = user_overrides.get(
        "cross_checks",
        cross_checks_for_project_type(merged["project_type"], merged["secondary_archetypes"], merged["capabilities"]),
    )
    merged["approval_status"] = (
        "approved"
        if snapshot_locked
        else "pending"
        if merged["phase"] in {"discovery", "planning", "approval"} and merged.get("approval_status") != "revision_requested"
        else merged.get("approval_status", "approved")
    )
    merged["approval_snapshot"] = {
        "locked": snapshot_locked,
        "artifact": str(Path(STATE_DIRNAME) / "approval-snapshot.json"),
        "locked_fields": list(PLAN_LOCK_FIELDS),
    }
    merged["tasks"] = merge_tasks(state.get("tasks", []), default_tasks(merged["project_type"], merged["phase"]))

    phase_history = [item for item in state.get("phase_history", []) if isinstance(item, str)]
    if not phase_history:
        phase_history = [merged["phase"]]
    elif phase_history[-1] != merged["phase"]:
        phase_history.append(merged["phase"])
    merged["phase_history"] = phase_history

    existing_artifacts = state.get("artifacts", {})
    if isinstance(existing_artifacts, dict):
        merged["artifacts"] = {
            **artifact_paths(workspace),
            **existing_artifacts,
        }
    else:
        merged["artifacts"] = artifact_paths(workspace)
    return merged


def can_transition_phase(current_phase: str, next_phase: str, *, force: bool = False) -> bool:
    if force or current_phase == next_phase:
        return True
    allowed = {
        "discovery": {"planning"},
        "planning": {"approval", "discovery"},
        "approval": {"planning", "execution"},
        "execution": {"verification", "approval"},
        "verification": {"execution", "handoff"},
        "handoff": {"verification"},
    }
    return next_phase in allowed.get(current_phase, set())


def has_meaningful_content(text: str) -> bool:
    lines = [line.strip() for line in text.splitlines() if line.strip()]
    meaningful = [
        line
        for line in lines
        if not line.startswith("#")
        and not line.startswith("| ---")
        and not line.startswith("<!--")
        and not line.startswith("[")
        and line not in {"{}", "[]"}
    ]
    return len(" ".join(meaningful)) >= 40


def is_template_content(path: Path, template_name: str) -> bool:
    if not path.exists():
        return False
    return path.read_text(encoding="utf-8").strip() == read_template(template_name).strip()


def extract_summary_from_markdown(path: Path, *, fallback: str) -> str:
    if not path.exists():
        return fallback
    lines = [line.strip() for line in path.read_text(encoding="utf-8").splitlines()]
    for line in lines:
        if not line or line.startswith("#") or line.startswith("- ") or line.startswith("## "):
            continue
        return line
    return fallback
