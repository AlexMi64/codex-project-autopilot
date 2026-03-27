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

Последнее обновление внутри `v1.0.0`:

- discovery усилен до двух волн с более сильным brief
- добавлены правила уникальности проекта и антишаблонные ограничения
- усилен `design-director`: композиция, proof-слой, визуальный якорь, уровень смелости, язык форм
- усилен `frontend-builder`: обязательная проверка `1440 / 768 / 375`, запрет на слабый mobile и деградацию до generic UI
- усилен `qa-reviewer`: отдельная проверка адаптива, читаемости и реальных viewport size
- добавлена поддержка локальных style-inputs:
  - `skill.md`
  - `SKILL.md`
  - `design-system.json`
  - `brand-guide.md`
  - `moodboard.md`
- добавлен шаблон `design-system.json`
- добавлена проверка типографики под язык контента, включая поддержку кириллицы для русского интерфейса
