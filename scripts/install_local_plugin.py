#!/usr/bin/env python3
"""Register Codex Project Autopilot in a workspace marketplace.json."""

from __future__ import annotations

import argparse
import json
from pathlib import Path


DEFAULT_MARKETPLACE_NAME = "morecil-local"
DEFAULT_MARKETPLACE_DISPLAY_NAME = "Morecil Local Plugins"
PLUGIN_NAME = "codex-project-autopilot"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Добавить Codex Project Autopilot в .agents/plugins/marketplace.json выбранного workspace."
    )
    parser.add_argument(
        "--workspace",
        default=".",
        help="Путь до проекта, в котором нужно зарегистрировать плагин.",
    )
    parser.add_argument(
        "--plugin-path",
        default="",
        help="Необязательный путь до папки плагина. По умолчанию используется текущий репозиторий плагина.",
    )
    parser.add_argument(
        "--marketplace-name",
        default=DEFAULT_MARKETPLACE_NAME,
        help="Внутренний id локального marketplace.",
    )
    parser.add_argument(
        "--marketplace-display-name",
        default=DEFAULT_MARKETPLACE_DISPLAY_NAME,
        help="Отображаемое имя локального marketplace в Codex.",
    )
    return parser.parse_args()


def plugin_root_from_args(plugin_path: str) -> Path:
    if plugin_path:
        return Path(plugin_path).expanduser().resolve()
    return Path(__file__).resolve().parents[1]


def marketplace_path(workspace: Path) -> Path:
    return workspace / ".agents" / "plugins" / "marketplace.json"


def load_marketplace(path: Path, marketplace_name: str, display_name: str) -> dict:
    if path.exists():
        return json.loads(path.read_text(encoding="utf-8"))
    return {
        "name": marketplace_name,
        "interface": {"displayName": display_name},
        "plugins": [],
    }


def plugin_entry(plugin_path: Path) -> dict:
    return {
        "name": PLUGIN_NAME,
        "source": {
            "source": "local",
            "path": str(plugin_path),
        },
        "policy": {
            "installation": "AVAILABLE",
            "authentication": "ON_INSTALL",
        },
        "category": "Productivity",
    }


def upsert_plugin(marketplace: dict, entry: dict) -> dict:
    plugins = list(marketplace.get("plugins", []))
    updated = False
    for index, existing in enumerate(plugins):
        if existing.get("name") == entry["name"]:
            plugins[index] = entry
            updated = True
            break
    if not updated:
        plugins.append(entry)
    marketplace["plugins"] = plugins
    return marketplace


def main() -> None:
    args = parse_args()
    workspace = Path(args.workspace).expanduser().resolve()
    plugin_root = plugin_root_from_args(args.plugin_path)
    path = marketplace_path(workspace)
    path.parent.mkdir(parents=True, exist_ok=True)

    marketplace = load_marketplace(path, args.marketplace_name, args.marketplace_display_name)
    marketplace.setdefault("name", args.marketplace_name)
    marketplace.setdefault("interface", {})
    marketplace["interface"].setdefault("displayName", args.marketplace_display_name)
    marketplace = upsert_plugin(marketplace, plugin_entry(plugin_root))

    path.write_text(json.dumps(marketplace, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    print(f"Marketplace обновлён: {path}")
    print(f"Плагин зарегистрирован: {PLUGIN_NAME}")
    print(f"Путь до плагина: {plugin_root}")


if __name__ == "__main__":
    main()
