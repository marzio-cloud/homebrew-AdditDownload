
#!/usr/bin/env python3
"""AdditDownloader CLI.

This tool keeps a tiny local registry of files, lets you register a file by
dropping it into the command, copies registered files into your current
directory, and prints a guided help screen.
"""

from __future__ import annotations

import argparse
import json
import shutil
from pathlib import Path


REGISTRY_FILE = Path("registry.json")


def load_registry() -> dict[str, dict[str, str]]:
    if REGISTRY_FILE.exists():
        try:
            with REGISTRY_FILE.open("r", encoding="utf-8") as file:
                data = json.load(file)
            if isinstance(data, dict):
                return data
        except json.JSONDecodeError:
            pass
    return {}


def save_registry(data: dict[str, dict[str, str]]) -> None:
    with REGISTRY_FILE.open("w", encoding="utf-8") as file:
        json.dump(data, file, indent=4, sort_keys=True)
        file.write("\n")


def register_file(source: str) -> None:
    source_path = Path(source).expanduser()
    if not source_path.exists():
        print(f"❌ Error: '{source}' was not found.")
        return
    if source_path.is_dir():
        print(f"❌ Error: '{source}' is a directory. Please drop a file.")
        return

    resolved = source_path.resolve()
    registry = load_registry()
    registry[source_path.name] = {"source": str(resolved)}
    save_registry(registry)
    print(f"✅ Registered '{source_path.name}' from {resolved}")


def _resolve_source(name: str) -> Path | None:
    registry = load_registry()
    entry = registry.get(name)
    if isinstance(entry, dict):
        source = entry.get("source")
        if source:
            candidate = Path(source)
            if candidate.exists():
                return candidate

    candidate = Path(name).expanduser()
    if candidate.exists() and candidate.is_file():
        return candidate

    return None


def install_file(name: str, destination: str | None = None, force: bool = False) -> None:
    source = _resolve_source(name)
    if source is None:
        print(f"❌ Error: '{name}' is not registered. Run 'additdownloader mkf <file>' first.")
        return

    target_dir = Path(destination).expanduser() if destination else Path.cwd()
    target_dir.mkdir(parents=True, exist_ok=True)
    target_path = target_dir / source.name

    if source.resolve() == target_path.resolve():
        print(f"📦 '{source.name}' is already in {target_dir}")
        return

    if target_path.exists() and not force:
        print(f"❌ Error: '{target_path}' already exists. Use --force to replace it.")
        return

    shutil.copy2(source, target_path)
    print(f"📦 Installed '{source.name}' to {target_path}")


def show_help() -> None:
    print(
        """AdditDownloader

What it does
- Register a local file with `mkf`
- Install a registered file with `install`
- Show this help with `help`

Examples
  additdownloader mkf ./MyFile.zip
  additdownloader install MyFile.zip
  additdownloader help

Notes
- Files are tracked in `registry.json` in the current working directory.
- `mk` and `download` remain as compatibility aliases.
"""
    )


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="additdownloader",
        description="Register local files and install them into your directory.",
    )
    subparsers = parser.add_subparsers(dest="command")

    parser_help = subparsers.add_parser("help", help="Show the guided help screen")
    parser_help.set_defaults(func=lambda args: show_help())

    parser_mkf = subparsers.add_parser("mkf", help="Register a local file")
    parser_mkf.add_argument("source", help="Path to the file to register")
    parser_mkf.set_defaults(func=lambda args: register_file(args.source))

    parser_mk = subparsers.add_parser(
        "mk",
        help=argparse.SUPPRESS,
        description="Compatibility alias for mkf.",
    )
    parser_mk.add_argument("source", help="Path to the file to register")
    parser_mk.set_defaults(func=lambda args: register_file(args.source))

    parser_install = subparsers.add_parser("install", help="Install a registered file")
    parser_install.add_argument("name", help="Registered file name to install")
    parser_install.add_argument(
        "--dest",
        default=None,
        help="Optional destination directory. Defaults to the current directory.",
    )
    parser_install.add_argument(
        "--force",
        action="store_true",
        help="Replace the file if it already exists.",
    )
    parser_install.set_defaults(
        func=lambda args: install_file(args.name, args.dest, args.force)
    )

    parser_download = subparsers.add_parser(
        "download",
        help=argparse.SUPPRESS,
        description="Compatibility alias for install.",
    )
    parser_download.add_argument("name", help="Registered file name to install")
    parser_download.add_argument(
        "--dest",
        default=None,
        help="Optional destination directory. Defaults to the current directory.",
    )
    parser_download.add_argument(
        "--force",
        action="store_true",
        help="Replace the file if it already exists.",
    )
    parser_download.set_defaults(
        func=lambda args: install_file(args.name, args.dest, args.force)
    )

    parser_dwnd = subparsers.add_parser(
        "dwnd",
        help=argparse.SUPPRESS,
        description="Compatibility alias for install.",
    )
    parser_dwnd.add_argument("name", help="Registered file name to install")
    parser_dwnd.add_argument(
        "--dest",
        default=None,
        help="Optional destination directory. Defaults to the current directory.",
    )
    parser_dwnd.add_argument(
        "--force",
        action="store_true",
        help="Replace the file if it already exists.",
    )
    parser_dwnd.set_defaults(
        func=lambda args: install_file(args.name, args.dest, args.force)
    )

    return parser


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()

    if not hasattr(args, "func"):
        show_help()
        return

    args.func(args)


if __name__ == "__main__":
    main()
