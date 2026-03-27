Продолжить текущий проект из `.codex-agent/state.json`.

Используй skill `autonomous-project-orchestrator`.

Поведение:

- прочитай `.codex-agent/state.json`
- определи текущую фазу
- восстанови playbook, packs, quality gates и следующий checkpoint
- продолжай с ближайшей незавершенной задачи
- спрашивай пользователя только если проект реально уперся в секрет, доступ или критичный выбор
