import os
import json

# List of folders to ignore
IGNORED_FOLDERS = {".git", ".vscode", "node_modules", "__pycache__", "dist", "build", "venv"}

def scan_directory(directory: str) -> dict:
    """
    Scans the directory structure and returns a dictionary representation.
    """
    project_structure = {}

    for root, dirs, files in os.walk(directory):
        dirs[:] = [d for d in dirs if d not in IGNORED_FOLDERS]  # Exclude ignored folders

        relative_path = os.path.relpath(root, directory)
        if relative_path == ".":
            relative_path = ""  # Root directory
        
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


"""--------- NOT NECESSARY FOR NOW --------------------
def build_tree(structure: dict, root: str = "", prefix=""):
    tree_str = "PROJECT STRUCTURE\n" if root == "" else ""

    # Get folders and files for the current root
    folders = structure.get(root, {}).get("folders", [])
    files = structure.get(root, {}).get("files", [])
    
    entries = folders + files
    total = len(entries)

    for i, entry in enumerate(entries):
        is_last = (i == total - 1)
        connector = "└── " if is_last else "├── "
        new_prefix = prefix + ("    " if is_last else "│   ")

        tree_str += f"{prefix}{connector}{entry}{'/' if entry in folders else ''}\n"

        if entry in folders:
            new_root = os.path.join(root, entry) if root else entry
            tree_str += build_tree(structure, new_root, new_prefix)

    return tree_str

def save_text_report(structure: dict, output_file: str):
    project_tree = build_tree(structure)
    
    with open(output_file, "w", encoding="utf-8") as f:
        f.write(project_tree)
"""

if __name__ == "__main__":
    project_path = input("Enter the project directory path: ")
    json_output = "reports/project_summary.json"
    text_output = "reports/project_report.txt"

    if not os.path.exists("reports"):
        os.makedirs("reports")

    structure = scan_directory(project_path)
    save_json_report(structure, json_output)

    print(f"Project structure saved to {json_output} and {text_output}")
