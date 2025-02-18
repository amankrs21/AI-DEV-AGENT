from .mistral_helper import call_mistral_api

import json
import os

REPORT_FILES = [
    "final_project_summary.json",
    "backend_security.json",
    "frontend_security.json",
]

def load_reports():
    """Reads and merges the content of all report files into a structured prompt."""
    reports = {}
    for file in REPORT_FILES:
        file = f"reports/{file}"
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
    
    # Improved prompt structure
    prompt = """
        You are an AI assistant analyzing a software project.
        The following reports contain key insights about the project's structure, security, and dependencies.
        Summarize them in a detailed manner, focusing on important insights and recommendations.
        Along with the summary, provide a comprehensive analysis of the project's strengths, weaknesses, and potential risks.
        Also, suggest possible improvements and best practices for enhancing the project's overall quality and security.
        Please ensure that the generated insights are clear, concise, & actionable and in the README.md format.
        You can refer to the reports below for detailed information:
    """

    for filename, content in reports_data.items():
        prompt += f"### Report: {filename}\n"
        prompt += "```\n"  # Format content as code block for clarity
        prompt += json.dumps(content, indent=2)  # Keep full content
        prompt += "\n```\n\n"

    print("\nSending prompt to Mistral...")  

    response = call_mistral_api(prompt, stream=True)  # Enable streaming
    
    # Save the response as part of the final AI-generated report
    with open("./reports/model_analysis_report.md", "w", encoding="utf-8") as file:
        file.write(response)
    
    print("\nModel insights saved to 'model_analysis_report.md'")

