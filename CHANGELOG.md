# Changelog

## v1.0.0

Первый публичный релиз `Codex Project Autopilot`.

Что вошло:

- глобальная установка плагина и работа в любых проектах
- локальная память проекта через `.codex-agent/`
- фазы `discovery -> planning -> approval -> execution -> verification -> handoff`
- русскоязычный UX для новичков
- три варианта плана: `минимум`, `оптимально`, `с запасом`
- role-based orchestration с `solo` и `delegated` режимами
- `SOULS.md`, role contracts и handoff rules
- anti-template система для менее шаблонных результатов
- phase-aware knowledge packs и playbooks
- scope guardrails против раздувания MVP
- lean context flow через `phase-card.md`, `ultra-context.md` и фазовый `context-bundle.md`
- кроссплатформенные Python hooks для macOS, Linux и Windows
- validator, approval snapshot и базовые тесты
