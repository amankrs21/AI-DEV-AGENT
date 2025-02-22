import json
from .context_manager import send_code_in_chunks, request_file_selection

def select_files_for_feature(feature_request):
    """
    Selects relevant files for updating based on user feature request.
    """
    snapshot_path = "data/code_snapshot.json"

    try:
        with open(snapshot_path, "r", encoding="utf-8") as f:
            code_snapshot = json.load(f)
    except FileNotFoundError:
        print("Error: code_snapshot.json not found. Run the scanner first.")
        return None

    # Send the code snapshot in chunks
    send_code_in_chunks(code_snapshot)

    # Ask AI to identify relevant files
    files_to_update = request_file_selection(feature_request)

    if not files_to_update:
        print("No relevant files identified.")
        return None

    print("\nSuggested files to update:\n", "\n".join(files_to_update))

    confirmation = input("\nDo you want to proceed with these files? (yes/no): ").strip().lower()

    if confirmation in {"yes", "y"}:
        return files_to_update
    else:
        print("Please specify the correct files manually.")
        return None
