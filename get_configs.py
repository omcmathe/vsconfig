#!/usr/bin/env python3
"""
Utility script to copy VS Code (or VSCodium) user configuration files
(settings.json, keybindings.json, and snippets folder) to the project root.
Works on Windows, macOS, and Linux.
"""

import sys
import json
from pathlib import Path
from typing import Any
from argparse import ArgumentParser


SCRIPT_OS: str = sys.platform


def get_vscode_dir() -> Path:
	"""
	Search for a valid VS Code or VSCodium configuration directory.
	Checks user/global paths across platforms.
	Raises FileNotFoundError if no directory is found.
	"""
	home: Path = Path.home()
	candidates: List[Path] = []

	if SCRIPT_OS.startswith("win"):
		# Windows User and Global/System settings directories
		candidates = [
			home / "AppData" / "Roaming" / "Code" / "User",
			home / "AppData" / "Roaming" / "VSCodium" / "User",
		]
	elif SCRIPT_OS == "darwin":
		# macOS directories
		candidates = [
			home / "Library" / "Application Support" / "Code" / "User",
			home / "Library" / "Application Support" / "VSCodium" / "User",
		]
	else:
		# Linux and other Unix-like systems (Standard, Flatpak, Snap)
		candidates = [
			home / ".config" / "Code" / "User",
			home / ".config" / "VSCodium" / "User",
			# Flatpak
			home / ".var" / "app" / "com.visualstudio.code" / "config" / "Code" / "User",
			home / ".var" / "app" / "com.vscodium.codium" / "config" / "VSCodium" / "User",
			# Snap
			home / "snap" / "code" / "common" / ".config" / "Code" / "User",
			home / "snap" / "codium" / "common" / ".config" / "VSCodium" / "User",
		]

	for path in candidates:
		if path.exists() and path.is_dir():
			print(f"Found configuration directory: {path}")
			return path

	raise FileNotFoundError(
		"Could not find a valid VS Code or VSCodium user configuration directory "
		"on this system. Checked locations:\n" + "\n".join(f" - {p}" for p in candidates)
	)


VSC_PATH = get_vscode_dir()


def get_vscode_extensions() -> list[str]:
	from subprocess import run as run_command

	base_commands = ["code", "codium"]

	for command in base_commands:
		try:
			output = run_command([command, "--list-extensions"], capture_output=True, text=True, check=True).stdout.strip()
			return output.split('\n')
		except Exception:
			continue
	
	return []


def format_vsc_extensions(extensions: list[str]) -> dict[str, Any]:
	format: dict[str, list[str]] = {"recommendations": []}

	format["recommendations"].extend(extensions)

	return format


def copy_config_to_project(dir: Path | None = None) -> None:
	if dir and dir.suffix != "":
		raise TypeError("`dir` can't contain extension.")

	dir.mkdir(exist_ok=True)

	project_root: Path = Path(__file__).parent.resolve()
	save_at: Path = project_root / dir if dir else project_root

	vsc_dir: Path = VSC_PATH

	# Existing files to copy
	path_to_copy: List[str] = ["settings.json", "keybindings.json", "tasks.json", "snippets"]
	
	for end_path in path_to_copy:
		src: Path = vsc_dir / end_path
		dst: Path = save_at / end_path
		
		if src.exists():
			try:
				dst._delete()
			finally:
				src.copy(dst)
		else:
			print(f"Optional `{end_path}` not found in configuration directory (skipping).")

	# Extensions file to create
	extensions_file_content = format_vsc_extensions(get_vscode_extensions())
	extensions_file = save_at / "extensions.json"

	extensions_file.write_text(json.dumps(extensions_file_content, indent=2))

	print(f"Complete.")

# 

PARSER = ArgumentParser(
		prog='VSC Config Getter',
		description='Does one thing: obtain VSC configs and copy them into the script root.'
	)
PARSER.add_argument('-d', '--directory', help="Optional directory to copy into.")


def main() -> None:
	args = PARSER.parse_args()
	
	try:
		copy_config_to_project(Path(args.directory))
	except Exception as e:
		print(f"Error: {e}")
		sys.exit(1)

if __name__ == "__main__":
	main()