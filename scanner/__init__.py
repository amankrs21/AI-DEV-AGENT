from .structure_scanner import scan_directory, save_json_report
from .dependency_scanner import scan_dependencies
from .security_scanner import scan_security

import os
import json

def scan_project():
    """
    Orchestrates the entire scanning process based on user input.
    """
    project_type = input("Is the project separated into frontend and backend? (yes/no): ").strip().lower()
    
    if project_type == "yes":
        frontend_path = input("Enter the frontend project directory path: ").strip()
        backend_path = input("Enter the backend project directory path: ").strip()
        project_dirs = {"frontend": frontend_path, "backend": backend_path}
    else:
        project_path = input("Enter the project directory path: ").strip()
        project_dirs = {"full_project": project_path}

    # Create a reports directory
    os.makedirs("reports", exist_ok=True)

    final_report = {}

    for key, path in project_dirs.items():
        print(f"Scanning {key} at {path}...")

        # Scan structure
        structure = scan_directory(path)
        structure_report_path = f"reports/{key}_structure.json"
        save_json_report(structure, structure_report_path)
        print(f"Structure report saved to {structure_report_path}")

        # Scan dependencies
        dependencies = scan_dependencies(path)
        dependency_report_path = f"reports/{key}_dependencies.json"
        with open(dependency_report_path, "w", encoding="utf-8") as f:
            json.dump(dependencies, f, indent=4)
        print(f"Dependency report saved to {dependency_report_path}")

        # Security Scan
        security_report_path = f"reports/{key}_security.json"
        scan_security(path, security_report_path)

        # Store results in final report
        final_report[key] = {
            "structure": structure,
            "dependencies": dependencies
        }

    # Save combined summary report
    summary_report_path = "reports/final_project_summary.json"
    with open(summary_report_path, "w", encoding="utf-8") as f:
        json.dump(final_report, f, indent=4)

    print(f"Final summary report saved to {summary_report_path}")
