import os
import json

IGNORED_FOLDERS = {".git", ".vscode", "node_modules", "__pycache__", "dist", "build", "venv"}
IGNORED_EXTENSIONS = {".log", ".json", ".lock", ".md", ".txt", ".png", ".jpg", ".jpeg", ".gif", ".svg", ".pdf", ".cjs"}

def scan_code_files(directory: str) -> dict:
    """
    Scans all code files in the given directory and extracts their content.
    """
    code_data = {}

    for root, dirs, files in os.walk(directory):
        dirs[:] = [d for d in dirs if d not in IGNORED_FOLDERS]
        
        for file in files:
            _, ext = os.path.splitext(file)
            if ext.lower() in IGNORED_EXTENSIONS:
                continue  # Ignore non-code files
            
            file_path = os.path.join(root, file)
            relative_path = os.path.relpath(file_path, directory)

            try:
                with open(file_path, "r", encoding="utf-8") as f:
                    content = f.read()
                code_data[relative_path] = content
            except Exception as e:
                print(f"Error reading {relative_path}: {e}")

    return code_data


def save_code_snapshot(directory: str):
    """
    Saves the scanned code into a JSON file inside the `data/` folder.
    """
    os.makedirs("data", exist_ok=True)
    code_snapshot = scan_code_files(directory)

    snapshot_path = f"data/code_snapshot.json"
    with open(snapshot_path, "w", encoding="utf-8") as f:
        json.dump(code_snapshot, f, indent=4)

    print(f"Code snapshot saved to {snapshot_path}")
