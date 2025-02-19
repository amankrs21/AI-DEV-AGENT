from .structure_scanner import scan_directory
from .dependency_scanner import scan_dependencies
from .security_scanner import scan_security
from .code_scanner import save_code_snapshot

import os
import json

def project_initial_report():
    """
    Orchestrates the entire scanning process based on user input.
    """
    project_path = input("Enter the project directory path: ").strip()

    os.makedirs("reports", exist_ok=True)

    print(f"Scanning project at {project_path}...")

    structure = scan_directory(project_path)
    dependencies = scan_dependencies(project_path)
    security = scan_security(project_path)
    save_code_snapshot(project_path)  # Unified code scanning

    final_report = {
        "structure": structure,
        "dependencies": dependencies,
        "security": security
    }

    summary_report_path = "reports/project_summary.json"
    with open(summary_report_path, "w", encoding="utf-8") as f:
        json.dump(final_report, f, indent=4)

    print(f"Project Summary Report Saved to {summary_report_path}")
