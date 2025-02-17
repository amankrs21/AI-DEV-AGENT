from scanner import scan_project
from llm import generate_model_insights
import os

if __name__ == "__main__":
    # Create reports folder if it doesn't exist
    reports_folder = "./reports"
    if not os.path.exists(reports_folder):
        print("Creating reports folder...")
        os.makedirs(reports_folder)
    
    # scan_project()
    generate_model_insights()
