import os

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
