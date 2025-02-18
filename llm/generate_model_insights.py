import json
import os
from .mistral_helper import call_mistral_api

REPORT_FILES = [
    "final_project_summary.json",
    "backend_security.json",
    "frontend_security.json",
]

def load_reports():
    """Reads and merges the content of all report files into a structured prompt."""
    reports = {}
    for file in REPORT_FILES:
        if os.path.exists(file):
            with open(file, "r", encoding="utf-8") as f:
                try:
                    reports[file] = json.load(f)  # Load JSON data
                except json.JSONDecodeError:
                    print(f"Warning: Could not decode JSON from {file}")
    
    return reports

def generate_model_insights():
    """
    Uses Mistral 7B to generate insights based on project analysis and reports.
    """
    reports_data = load_reports()
    
    # Structure the prompt dynamically based on available reports
    prompt = "Analyze the given project reports and summarize key insights:\n\n"
    
    for filename, content in reports_data.items():
        prompt += f"### {filename}:\n"
        prompt += json.dumps(content, indent=2)[:4000]  # Truncate if too long
        prompt += "\n\n"

    print("\nSending prompt to Mistral...")    
    response = call_mistral_api(prompt)
    
    # Save the response as part of the final AI-generated report
    with open("model_analysis_report.md", "w", encoding="utf-8") as file:
        file.write(response)
    
    print("\nModel insights saved to 'model_analysis_report.md'")
