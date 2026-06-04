from pathlib import Path
import json


CWD = Path.cwd()
CWD_NAME = CWD.name


WORKSPACE_FILE_TEMPLATE = {
    "folders": [
        {"path": "..", "name": CWD_NAME},
        {"path": "scratchpads", "name": "Scratchpads"},
    ],
    "settings": {
        "files.exclude": {
            "**/.vscode": True,
        }
    },
}

WORKSPACE_FILE_EXT = ".code-workspace"

SETTINGS_TEMPLATE = {
    "files.exclude": {
        "**/.git": True,
        "**/.svn": True,
        "**/.hg": True,
        "**/.DS_Store": True,
        "**/Thumbs.db": True,
    }
}


def main() -> None:
    new_vsc_folder = CWD / ".vscode"
    scratchpads_folder = new_vsc_folder / "scratchpads"
    settings_file = new_vsc_folder / "settings.json"
    workspace_file = new_vsc_folder / f"{CWD_NAME}{WORKSPACE_FILE_EXT}"
    
    try:
        new_vsc_folder.mkdir(exist_ok=True)
        scratchpads_folder.mkdir(exist_ok=True)
        settings_file.write_text(json.dumps(SETTINGS_TEMPLATE, indent=2))
        workspace_file.write_text(json.dumps(WORKSPACE_FILE_TEMPLATE, indent=2))
    except Exception:
        print(f"Failed to create project `{CWD_NAME}`")


if __name__ == "__main__":
    main()