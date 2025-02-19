import os
import json

IGNORED_FOLDERS = {".git", ".vscode", "node_modules", "__pycache__", "dist", "build", "venv"}

def find_package_json_files(directory):
    package_json_files = []
    for root, dirs, files in os.walk(directory):
        dirs[:] = [d for d in dirs if d not in IGNORED_FOLDERS]
        
        if "package.json" in files:
            package_json_files.append(os.path.join(root, "package.json"))

    return package_json_files

def extract_dependencies(package_json_path):
    with open(package_json_path, "r", encoding="utf-8") as file:
        try:
            data = json.load(file)
            dependencies = data.get("dependencies", {})
            dev_dependencies = data.get("devDependencies", {})
            return dependencies, dev_dependencies
        except json.JSONDecodeError:
            print(f"Error decoding JSON in {package_json_path}")
            return {}, {}

def scan_dependencies(directory: str) -> dict:
    package_json_files = find_package_json_files(directory)
    dependency_report = {}

    for package_json in package_json_files:
        relative_path = os.path.relpath(os.path.dirname(package_json), directory)
        dependencies, dev_dependencies = extract_dependencies(package_json)
        
        dependency_report[relative_path] = {
            "dependencies": dependencies,
            "devDependencies": dev_dependencies
        }

    return dependency_report
