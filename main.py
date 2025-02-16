from scanner import scan_project, scan_dependencies, scan_security

def main():
    print("Project Analysis Tool")
    project_type = input("Is the project separated into frontend and backend? (yes/no): ").strip().lower()
    
    if project_type == "yes":
        frontend_path = input("Enter the frontend directory path: ").strip()
        backend_path = input("Enter the backend directory path: ").strip()
        project_paths = {"frontend": frontend_path, "backend": backend_path}
    else:
        project_path = input("Enter the project directory path: ").strip()
        project_paths = {"full_project": project_path}
    
    framework = input("Enter the primary framework (React, Angular, Vue, Django, Express, etc.): ").strip()
    
    for key, path in project_paths.items():
        print(f"Scanning {key} at {path}...")
        scan_project(path, f"reports/{key}_project_summary")
        scan_dependencies(path, f"reports/{key}_dependency_report.json")
        scan_security(path, f"reports/{key}_security_audit.json")
    
    print("All reports generated successfully!")

if __name__ == "__main__":
    main()
