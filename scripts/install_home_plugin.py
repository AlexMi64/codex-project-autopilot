#!/usr/bin/env python3
"""Install Codex Project Autopilot as a home-local plugin for all projects."""

from __future__ import annotations

import argparse
import json
import shutil
from pathlib import Path


PLUGIN_NAME = "codex-project-autopilot"
DEFAULT_MARKETPLACE_NAME = "morecil-local"
DEFAULT_MARKETPLACE_DISPLAY_NAME = "Morecil Local Plugins"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Установить Codex Project Autopilot как общий локальный плагин для всех проектов."
    )
    parser.add_argument(
        "--home-root",
        default="~",
        help="Корень домашней установки. По умолчанию используется домашняя папка пользователя.",
    )
    parser.add_argument(
        "--source-plugin",
        default="",
        help="Путь до исходной папки плагина. По умолчанию используется текущий репозиторий плагина.",
    )
    parser.add_argument(
        "--marketplace-name",
        default=DEFAULT_MARKETPLACE_NAME,
        help="Внутренний id пользовательского marketplace.",
    )
    parser.add_argument(
        "--marketplace-display-name",
        default=DEFAULT_MARKETPLACE_DISPLAY_NAME,
        help="Отображаемое имя пользовательского marketplace.",
    )
    return parser.parse_args()


def plugin_root(source_plugin: str) -> Path:
    if source_plugin:
        return Path(source_plugin).expanduser().resolve()
    return Path(__file__).resolve().parents[1]


def install_root(home_root: Path) -> Path:
    return home_root / "plugins" / PLUGIN_NAME


def marketplace_path(home_root: Path) -> Path:
    return home_root / ".agents" / "plugins" / "marketplace.json"


def load_marketplace(path: Path, marketplace_name: str, display_name: str) -> dict:
    if path.exists():
        return json.loads(path.read_text(encoding="utf-8"))
    return {
        "name": marketplace_name,
        "interface": {"displayName": display_name},
        "plugins": [],
    }


def copy_plugin_tree(source: Path, destination: Path) -> None:
    if destination.exists():
        shutil.rmtree(destination)
    shutil.copytree(
        source,
        destination,
        ignore=shutil.ignore_patterns(".git", "__pycache__", ".codex-agent", ".DS_Store", "*.pyc", "*.pyo"),
    )


def plugin_entry() -> dict:
    return {
        "name": PLUGIN_NAME,
        "source": {
            "source": "local",
            "path": f"./plugins/{PLUGIN_NAME}",
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
    home_root = Path(args.home_root).expanduser().resolve()
    source = plugin_root(args.source_plugin)
    destination = install_root(home_root)
    destination.parent.mkdir(parents=True, exist_ok=True)
    copy_plugin_tree(source, destination)

    path = marketplace_path(home_root)
    path.parent.mkdir(parents=True, exist_ok=True)
    marketplace = load_marketplace(path, args.marketplace_name, args.marketplace_display_name)
    marketplace.setdefault("name", args.marketplace_name)
    marketplace.setdefault("interface", {})
    marketplace["interface"].setdefault("displayName", args.marketplace_display_name)
    marketplace = upsert_plugin(marketplace, plugin_entry())
    path.write_text(json.dumps(marketplace, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    print(f"Плагин скопирован в: {destination}")
    print(f"Marketplace обновлён: {path}")
    print("Теперь открой любой проект в Codex, зайди в Skills & Apps и установи плагин из пользовательского marketplace.")


if __name__ == "__main__":
    main()
