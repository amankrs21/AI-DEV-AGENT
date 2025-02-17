import os
import json

IGNORED_FOLDERS = {".git", ".vscode", "node_modules", "__pycache__", "dist", "build", "venv"}

def scan_directory(directory: str) -> dict:
    """
    Scans the directory structure and returns a dictionary representation.
    """
    project_structure = {}

    for root, dirs, files in os.walk(directory):
        dirs[:] = [d for d in dirs if d not in IGNORED_FOLDERS]

        relative_path = os.path.relpath(root, directory)
        if relative_path == ".":
            relative_path = ""

        project_structure[relative_path] = {
            "folders": sorted(dirs),
            "files": sorted(files)
        }

    return project_structure

def save_json_report(structure: dict, output_file: str):
    """
    Saves the scanned structure as a JSON file.
    """
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(structure, f, indent=4)
