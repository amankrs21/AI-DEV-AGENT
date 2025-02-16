from .structure_scanner import scan_directory, save_json_report, save_text_report

def scan_project(directory: str, output_file: str):
    """
    Orchestrates the scanning process and saves the report.
    """
    structure = scan_directory(directory)
    save_json_report(structure, f'{output_file}.json')
    save_text_report(structure, f'{output_file}.txt')
    print(f"Project structure saved to {output_file}")
