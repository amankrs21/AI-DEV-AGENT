import os
import subprocess
import json

IGNORED_FOLDERS = {".git", ".vscode", "node_modules", "__pycache__", "dist", "build", "venv"}

def run_npm_audit(package_json_path):
    """Runs 'npm audit --json' and captures the output."""
    package_dir = os.path.dirname(package_json_path)

    try:
        result = subprocess.run(
            ["npm", "audit", "--json"],
            cwd=package_dir,
            capture_output=True,
            text=True
        )

        audit_data = json.loads(result.stdout)

        return {
            "vulnerabilities": audit_data.get("vulnerabilities", {}),
            "metadata": audit_data.get("metadata", {}).get("vulnerabilities", {}),
            "dependencies": audit_data.get("metadata", {}).get("dependencies", {})
        }
    except subprocess.CalledProcessError as e:
        print(f"Failed to run npm audit in {package_dir}: {e}")
        return None
    except json.JSONDecodeError:
        print(f"Error decoding JSON output in {package_dir}")
        return None

def scan_security(directory, output_file):
    """Scans security vulnerabilities in all package.json files."""
    security_report = {}

    for root, dirs, files in os.walk(directory):
        dirs[:] = [d for d in dirs if d not in IGNORED_FOLDERS]

        if "package.json" in files:
            package_path = os.path.join(root, "package.json")
            relative_path = os.path.relpath(root, directory)

            audit_results = run_npm_audit(package_path)

            if audit_results:
                security_report[relative_path] = audit_results

    os.makedirs(os.path.dirname(output_file), exist_ok=True)

    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(security_report, f, indent=4)

    print(f"Security audit report saved to {output_file}")
