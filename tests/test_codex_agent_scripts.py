from __future__ import annotations

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


PLUGIN_ROOT = Path(__file__).resolve().parents[1]
INIT_SCRIPT = PLUGIN_ROOT / "scripts" / "init_codex_agent.py"
VALIDATE_SCRIPT = PLUGIN_ROOT / "scripts" / "validate_codex_agent.py"
TRANSITION_SCRIPT = PLUGIN_ROOT / "scripts" / "transition_codex_agent_phase.py"
INSTALL_SCRIPT = PLUGIN_ROOT / "scripts" / "install_local_plugin.py"
HOME_INSTALL_SCRIPT = PLUGIN_ROOT / "scripts" / "install_home_plugin.py"


class CodexAgentScriptTests(unittest.TestCase):
    def run_script(self, script: Path, *args: str) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            [sys.executable, str(script), *args],
            text=True,
            capture_output=True,
            check=False,
        )

    def test_init_creates_ultra_context_and_phase_aware_packs(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            workspace = Path(tmp)
            result = self.run_script(
                INIT_SCRIPT,
                "--workspace",
                str(workspace),
                "--idea",
                "Сделай Telegram-бота, который отвечает на вопросы поддержки",
            )
            self.assertEqual(result.returncode, 0, result.stderr)

            agent_dir = workspace / ".codex-agent"
            self.assertTrue(agent_dir.exists())
            state = json.loads((agent_dir / "state.json").read_text(encoding="utf-8"))
            self.assertEqual(state["project_type"], "telegram-ai-bot")
            self.assertEqual(state["selected_stack"]["bot_framework"], "Telegraf")
            self.assertEqual(state["token_mode"], "ultra")
            self.assertEqual(state["orchestration_mode"], "solo")
            self.assertEqual(state["selected_plan_variant"], "оптимально")
            self.assertEqual(state["beginner_explanation_mode"], "включен")
            self.assertEqual(state["role_system_version"], "morecil-role-system-v1")
            self.assertIn("project-discovery", state["role_contracts"])
            self.assertTrue(state["handoff_rules"])
            self.assertEqual(len(state["plan_variants"]), 3)
            self.assertIn("ultra-context.md", state["phase_context_targets"])
            self.assertNotIn("single-message-telegram-navigation", state["selected_packs"])
            self.assertTrue((agent_dir / "ultra-context.md").exists())
            self.assertTrue((agent_dir / "plan-variants.md").exists())
            self.assertTrue((agent_dir / "beginner-guide.md").exists())
            self.assertTrue((agent_dir / "approval-snapshot.json").exists())
            ultra_context = (agent_dir / "ultra-context.md").read_text(encoding="utf-8")
            self.assertIn("Сначала читай этот файл.", ultra_context)
            context_bundle = (agent_dir / "context-bundle.md").read_text(encoding="utf-8")
            self.assertIn("Короткие контракты ролей", context_bundle)
            self.assertIn("Правила handoff", context_bundle)

    def test_init_detects_secondary_archetypes_and_capabilities(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            workspace = Path(tmp)
            result = self.run_script(
                INIT_SCRIPT,
                "--workspace",
                str(workspace),
                "--idea",
                "Сделай Telegram-бота с админ-панелью, авторизацией и дашбордом для операторов",
            )
            self.assertEqual(result.returncode, 0, result.stderr)

            state = json.loads((workspace / ".codex-agent" / "state.json").read_text(encoding="utf-8"))
            self.assertEqual(state["project_type"], "telegram-ai-bot")
            self.assertIn("saas-mvp", state["secondary_archetypes"])
            self.assertIn("dashboard", state["capabilities"])
            self.assertIn("auth", state["capabilities"])
            self.assertEqual(state["orchestration_mode"], "delegated")
            self.assertTrue(any(item.get("role") == "frontend-builder" for item in state["delegation_targets"]))
            self.assertTrue(any(item.get("role") == "backend-builder" for item in state["delegation_targets"]))
            self.assertIn("frontend-builder", state["active_roles"])
            self.assertIn("./playbooks/saas-mvp.md", state["supporting_playbooks"])

    def test_override_is_preserved_after_merge(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            workspace = Path(tmp)
            init_result = self.run_script(INIT_SCRIPT, "--workspace", str(workspace), "--idea", "Сделай SaaS-дашборд")
            self.assertEqual(init_result.returncode, 0, init_result.stderr)

            state_path = workspace / ".codex-agent" / "state.json"
            state = json.loads(state_path.read_text(encoding="utf-8"))
            state["user_overrides"] = {
                "selected_stack": {
                    "framework": "Nuxt",
                    "ui_strategy": "custom-ui",
                    "database": "Supabase/Postgres-when-data-or-auth-is-real",
                }
            }
            state_path.write_text(json.dumps(state, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

            rerun = self.run_script(INIT_SCRIPT, "--workspace", str(workspace), "--idea", "Сделай SaaS-дашборд")
            self.assertEqual(rerun.returncode, 0, rerun.stderr)

            merged = json.loads(state_path.read_text(encoding="utf-8"))
            self.assertEqual(merged["selected_stack"]["framework"], "Nuxt")

    def test_transition_to_execution_locks_plan_and_enables_phase_specific_pack(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            workspace = Path(tmp)
            init_result = self.run_script(INIT_SCRIPT, "--workspace", str(workspace), "--idea", "Сделай Telegram-бота для FAQ")
            self.assertEqual(init_result.returncode, 0, init_result.stderr)

            agent_dir = workspace / ".codex-agent"
            replacements = {
                "discovery-questionnaire.md": "# Квиз discovery\n\nПользователь хочет Telegram-бота с inline-навигацией и простым FAQ.\n",
                "plan-variants.md": "# Варианты плана\n\n## Минимум\n\n- Что входит: один маршрут FAQ.\n\n## Оптимально\n\n- Что входит: один маршрут FAQ, callback-логика и webhook-ready конфигурация.\n\n## С запасом\n\n- Что входит: оптимальный вариант плюс одно улучшение.\n\n## Что рекомендовано по умолчанию\n\n- Выбранный вариант: Оптимально\n- Почему: это лучший баланс скорости и качества.\n",
                "beginner-guide.md": "# Объяснение простыми словами\n\nСейчас мы закончили план и готовы перейти к реализации. Всё лишнее вынесено из первой версии.\n",
                "project-brief.md": "# Краткий бриф проекта\n\nЭто Telegram-бот FAQ для клиентов. Он должен отвечать кнопками и не спамить чат.\n",
                "product-intelligence.md": "# Продуктовая аналитика\n\nАудитория — клиенты. Главная ценность — быстрые ответы без ожидания оператора.\n",
                "product-context.md": "# Контекст продукта\n\nОсновной сценарий — открыть меню, выбрать тему и получить ответ в том же сообщении.\n",
                "tech-context.md": "# Технический контекст\n\nБот строится на Node.js, Telegraf и Hono. Основной риск — хаотичная навигация и отсутствие webhook-ready конфигурации.\n",
                "implementation-plan.md": "# План реализации\n\nСобираем MVP Telegram-бота с меню, callback-обработкой, inline-навигацией и webhook-готовностью.\n",
                "active-context.md": "# Активный контекст\n\nПлан согласован. Следующий шаг — реализация обработчиков меню и callback-маршрутов.\n",
                "progress.md": "# Прогресс\n\nПлан и технический контекст готовы. Реализация ещё не началась.\n",
                "design-direction.md": "# Дизайн-направление\n\nДля бота важны компактность, отсутствие визуального мусора и понятные действия.\n",
            }
            for name, content in replacements.items():
                (agent_dir / name).write_text(content, encoding="utf-8")

            result = self.run_script(
                TRANSITION_SCRIPT,
                "--workspace",
                str(workspace),
                "--phase",
                "execution",
                "--approve-plan",
                "--force",
            )
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

            state = json.loads((agent_dir / "state.json").read_text(encoding="utf-8"))
            snapshot = json.loads((agent_dir / "approval-snapshot.json").read_text(encoding="utf-8"))
            self.assertEqual(state["phase"], "execution")
            self.assertEqual(state["approval_status"], "approved")
            self.assertTrue(state["approval_snapshot"]["locked"])
            self.assertTrue(snapshot["locked"])
            self.assertIn("single-message-telegram-navigation", state["selected_packs"])

    def test_validate_requires_locked_plan_for_execution(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            workspace = Path(tmp)
            init_result = self.run_script(INIT_SCRIPT, "--workspace", str(workspace), "--idea", "Сделай SaaS-дашборд")
            self.assertEqual(init_result.returncode, 0, init_result.stderr)

            state_path = workspace / ".codex-agent" / "state.json"
            state = json.loads(state_path.read_text(encoding="utf-8"))
            state["phase"] = "execution"
            state["approval_status"] = "pending"
            state_path.write_text(json.dumps(state, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

            result = self.run_script(
                VALIDATE_SCRIPT,
                "--workspace",
                str(workspace),
            )
            self.assertNotEqual(result.returncode, 0)
            self.assertIn("план должен быть заморожен", result.stdout)

    def test_validate_passes_once_required_docs_are_filled(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            workspace = Path(tmp)
            init_result = self.run_script(INIT_SCRIPT, "--workspace", str(workspace), "--idea", "Сделай лендинг-портфолио")
            self.assertEqual(init_result.returncode, 0, init_result.stderr)

            agent_dir = workspace / ".codex-agent"
            replacements = {
                "ultra-context.md": "# Ультра-контекст\n\nСначала читай этот файл. Проект находится на стадии handoff и готов к передаче.\n- Цель: Лендинг-портфолио\n- Фаза: handoff\n- Основной архетип: landing-page\n- План заморожен: да\n",
                "context-bundle.md": "# Контекстный bundle\n\nИспользуй этот файл вторым после `ultra-context.md`, если нужен расширенный, но всё ещё экономный контекст.\n",
                "discovery-questionnaire.md": "# Квиз discovery\n\nПользователь хочет простой сайт-портфолио. Квиз подтвердил, что логин, платежи и база данных не нужны.\n",
                "plan-variants.md": "# Варианты плана\n\n## Минимум\n\n- Что входит: один рабочий сценарий.\n\n## Оптимально\n\n- Что входит: основной сценарий, мобильная полировка и базовое SEO.\n\n## С запасом\n\n- Что входит: оптимальный вариант плюс одно полезное улучшение.\n\n## Что рекомендовано по умолчанию\n\n- Выбранный вариант: Оптимально\n- Почему: это лучший баланс скорости и качества.\n",
                "beginner-guide.md": "# Объяснение простыми словами\n\nСейчас проект на стадии handoff. Главное уже сделано, а оставшиеся ручные шаги минимальны.\n",
                "project-brief.md": "# Краткий бриф проекта\n\nЭто чистый лендинг-портфолио для независимого специалиста. Он показывает избранные работы, короткую биографию и один понятный способ связаться.\n",
                "product-intelligence.md": "# Продуктовая аналитика\n\nАудитория — потенциальные клиенты. Главный CTA — отправить заявку после просмотра кейсов и краткого описания опыта.\n",
                "product-context.md": "# Контекст продукта\n\nАудитория — потенциальные клиенты. Им нужны быстрые сигналы доверия, понятные примеры работ и одно явное действие для связи.\n",
                "tech-context.md": "# Технический контекст\n\nВыбран архетип лендинга на Astro. Основные критерии качества — мобильная аккуратность, базовое SEO и сильный CTA.\n",
                "active-context.md": "# Активный контекст\n\nВыбрано редакционное и минималистичное визуальное направление. Следующий шаг — дополировать адаптивные секции и финализировать CTA.\n",
                "progress.md": "# Прогресс\n\nОсновные секции уже собраны. Осталось выровнять мобильные отступы и финальные метаданные.\n",
                "implementation-plan.md": "# План реализации\n\nMVP выпускает лендинг-портфолио на Astro с кастомными секциями, формой контакта, чётким scope и готовыми критериями приёмки.\n",
                "verification-report.md": "# Отчёт по проверке\n\nДесктопная и мобильная версии проверены, главный CTA работает, SEO-метаданные на месте.\n",
                "scorecard.md": "# Оценочная карта\n\n- Чёткость задачи: 5\n- Архитектура: 5\n- UX/UI: 5\n- Надёжность: 4\n- Безопасность: 5\n- Проверки: 5\n- Готовность к handoff: 5\n",
                "env-secrets-checklist.md": "# Чеклист по переменным окружения и секретам\n\nПроект не требует обязательных секретов. При желании позже можно добавить ключи email-провайдера для формы контакта.\n",
                "final-handoff.md": "# Финальный handoff\n\nЛендинг готов к локальному запуску и деплою. Начни с `npm install` и `npm run dev`, затем задеплой на выбранный статический хостинг.\n",
                "approval-snapshot.json": json.dumps({"locked": True, "playbook": "./playbooks/landing-page.md"}, ensure_ascii=False, indent=2) + "\n",
            }
            for name, content in replacements.items():
                (agent_dir / name).write_text(content, encoding="utf-8")

            state = json.loads((agent_dir / "state.json").read_text(encoding="utf-8"))
            state["phase"] = "handoff"
            state["approval_status"] = "approved"
            state["selected_packs"] = ["memory-bank"]
            state["selected_plan_variant"] = "оптимально"
            state["plan_variants"] = [
                {"id": "минимум", "title": "Минимум", "summary": "Один рабочий сценарий", "when_to_choose": "Когда нужен быстрый запуск"},
                {"id": "оптимально", "title": "Оптимально", "summary": "Баланс скорости и качества", "when_to_choose": "Когда нужен лучший базовый результат"},
                {"id": "с-запасом", "title": "С запасом", "summary": "MVP плюс 1-2 улучшения", "when_to_choose": "Когда можно добавить немного качества"},
            ]
            state["beginner_explanation_mode"] = "включен"
            state["scope_mode"] = "mvp-с-отдельным-блоком-рекомендаций"
            state["recommendation_policy"] = "советуй-улучшения-отдельно-от-MVP-и-не-включай-их-в-первую-реализацию-без-подтверждения"
            state["scope_guardrails"] = [
                "Не добавляй функции, которые пользователь явно не просил, без отдельного блока рекомендаций."
            ]
            state["approval_snapshot"] = {
                "locked": True,
                "artifact": ".codex-agent/approval-snapshot.json",
                "locked_fields": ["playbook"],
            }
            (agent_dir / "state.json").write_text(json.dumps(state, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

            result = self.run_script(
                VALIDATE_SCRIPT,
                "--workspace",
                str(workspace),
                "--require-finalization",
            )
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

    def test_install_script_creates_marketplace_file(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            workspace = Path(tmp)
            result = self.run_script(INSTALL_SCRIPT, "--workspace", str(workspace))
            self.assertEqual(result.returncode, 0, result.stderr)

            marketplace_path = workspace / ".agents" / "plugins" / "marketplace.json"
            self.assertTrue(marketplace_path.exists())
            marketplace = json.loads(marketplace_path.read_text(encoding="utf-8"))
            self.assertEqual(marketplace["name"], "morecil-local")
            self.assertEqual(marketplace["plugins"][0]["name"], "codex-project-autopilot")
            self.assertEqual(marketplace["plugins"][0]["category"], "Productivity")
            self.assertEqual(
                marketplace["plugins"][0]["source"]["path"],
                str(PLUGIN_ROOT),
            )

    def test_install_script_updates_existing_marketplace_entry(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            workspace = Path(tmp)
            marketplace_path = workspace / ".agents" / "plugins" / "marketplace.json"
            marketplace_path.parent.mkdir(parents=True, exist_ok=True)
            marketplace_path.write_text(
                json.dumps(
                    {
                        "name": "custom-local",
                        "interface": {"displayName": "Custom Local Plugins"},
                        "plugins": [
                            {
                                "name": "codex-project-autopilot",
                                "source": {"source": "local", "path": "/old/path"},
                                "policy": {"installation": "AVAILABLE", "authentication": "ON_INSTALL"},
                                "category": "Productivity",
                            }
                        ],
                    },
                    ensure_ascii=False,
                    indent=2,
                )
                + "\n",
                encoding="utf-8",
            )

            result = self.run_script(INSTALL_SCRIPT, "--workspace", str(workspace))
            self.assertEqual(result.returncode, 0, result.stderr)

            marketplace = json.loads(marketplace_path.read_text(encoding="utf-8"))
            self.assertEqual(marketplace["name"], "custom-local")
            self.assertEqual(marketplace["interface"]["displayName"], "Custom Local Plugins")
            self.assertEqual(len(marketplace["plugins"]), 1)
            self.assertEqual(marketplace["plugins"][0]["source"]["path"], str(PLUGIN_ROOT))

    def test_home_install_script_copies_plugin_and_creates_user_marketplace(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            home_root = Path(tmp)
            result = self.run_script(HOME_INSTALL_SCRIPT, "--home-root", str(home_root))
            self.assertEqual(result.returncode, 0, result.stderr)

            installed_plugin = home_root / "plugins" / "codex-project-autopilot"
            self.assertTrue(installed_plugin.exists())
            self.assertTrue((installed_plugin / ".codex-plugin" / "plugin.json").exists())

            marketplace = json.loads(
                (home_root / ".agents" / "plugins" / "marketplace.json").read_text(encoding="utf-8")
            )
            self.assertEqual(marketplace["name"], "morecil-local")
            self.assertEqual(marketplace["plugins"][0]["source"]["path"], "./plugins/codex-project-autopilot")


if __name__ == "__main__":
    unittest.main()
