from .mistral_helper import call_mistral_api

import json
import os


REPORT_FILE = "./reports/project_summary.json"
LLM_REPORT_FILE = "./reports/LLM_analysis.md"


# Load the reports data from the JSON file
def load_reports():
    reports = {}
    
    if os.path.exists(REPORT_FILE):
        try:
            with open(REPORT_FILE, "r", encoding="utf-8") as file:
                reports = json.load(file)
        except json.JSONDecodeError:
            print(f"Warning: Could not decode JSON from {REPORT_FILE}")
    else:
        print(f"Warning: {REPORT_FILE} not found!")

    return reports


# Format the extracted report data into a structured Markdown report
def format_markdown_report(reports_data):
    markdown_report = ""

    for filename, content in reports_data.items():
        if "frontend" in filename.lower():
            section = "Frontend"
        elif "backend" in filename.lower():
            section = "Backend"
        else:
            section = "General Project Summary"

        markdown_report += f"### {section}\n"

        # Extract and format metadata, dependencies and vulnerabilities
        metadata = content.get("security", {}).get(".", {}).get("metadata", {})
        dependencies = content.get("security", {}).get(".", {}).get("dependencies", {})
        vulnerabilities = content.get("security", {}).get(".", {}).get("vulnerabilities", [])

        # Formatting the security issues (metadata)
        if metadata:
            markdown_report += "- **Security Issues [METADATA]:**\n"
            markdown_report += f"  - Critical: {metadata.get('critical', 0)}\n"
            markdown_report += f"  - High: {metadata.get('high', 0)}\n"
            markdown_report += f"  - Moderate: {metadata.get('moderate', 0)}\n"
            markdown_report += f"  - Low: {metadata.get('low', 0)}\n"
            markdown_report += f"  - Info: {metadata.get('info', 0)}\n"
            markdown_report += f"  - Total: {metadata.get('total', 0)}\n\n"
        
        # Formatting the dependencies summary
        if dependencies:
            markdown_report += "- **Dependency Summary [DEPENDENCIES]:**\n"
            markdown_report += f"  - **Total Dependencies:** {dependencies.get('total', 'N/A')}\n"
            markdown_report += f"  - Production: {dependencies.get('prod', 'N/A')}\n"
            markdown_report += f"  - Development: {dependencies.get('dev', 'N/A')}\n"
            markdown_report += f"  - Optional: {dependencies.get('optional', 'N/A')}\n"
            markdown_report += f"  - Peer: {dependencies.get('peer', 'N/A')}\n"
            markdown_report += f"  - PeerOptional: {dependencies.get('peerOptional', 'N/A')}\n\n"

        # Formatting the vulnerabilities
        if vulnerabilities:
            markdown_report += "- **Security Vulnerabilities [VUNDERABILITIES]:**\n"
            for vuln in vulnerabilities.values():
                markdown_report += f"  - {vuln.get('name', 'N/A')}\n"
                markdown_report += f"    - Severity: {vuln.get('severity', 'N/A')}\n"
                markdown_report += f"    - Description: {vuln.get('description', 'N/A')}\n"
                markdown_report += f"    - Reference: {vuln.get('reference', 'N/A')}\n\n"
        
    return markdown_report


# Generate the model insights using Mistral
def generate_model_insights():
    reports_data = load_reports()
    
    json_data_for_mistral = json.dumps(reports_data)

    # Ask Mistral to generate a detailed report about project structure and files
    prompt = f"""
    Please analyze the following project data and generate a detailed report in Markdown format. 
    The report should include:
    - A summary of the file structure for both the frontend and backend.
    - A list of security vulnerabilities, including severity levels.
    - A list of dependencies with production, development, and optional dependencies.
    - Any recommendations for improving security, performance, or dependencies.
    - Generate the report in attractive and well design Markdown format.

    The data is as follows:

    {json_data_for_mistral}
    """
    
    print("\nSending prompt to Mistral for analysis...")
    
    # Call Mistral API to generate the report
    mistral_response = call_mistral_api(prompt)
    
    # other markdown report
    markdown_report = format_markdown_report(reports_data)
    
    return mistral_response, markdown_report


# Generate & save the full report
def llm_analysis_report():
    mistral_response, markdown_report = generate_model_insights()
    
    full_report = "# Project Detailed Report by Mistral\n\n"
    full_report += f"## Mistral Analysis\n\n{mistral_response}\n\n\n\n"
    full_report += f"## Security Analysis Summary\n\n{markdown_report}"
    
    # Save the full report to a file
    with open(LLM_REPORT_FILE, "w", encoding="utf-8") as file:
        file.write(full_report)
    
    print(f"Full report generated and saved to {LLM_REPORT_FILE}")
