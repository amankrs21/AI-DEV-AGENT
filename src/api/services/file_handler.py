import os
import json
from flask import request

from src.core.ai_agent import send_code_in_chunks, remove_file_from_memory


# File path to save uploaded files
SNAPSHOT_FILE = "data/snapshots/code_snapshots.json"
os.makedirs(os.path.dirname(SNAPSHOT_FILE), exist_ok=True)

ACCEPTED_EXTENSIONS = ('.js', '.jsx', '.py', '.html', '.css')


# Function to save uploaded files
def save_files():
    if "files" not in request.files:
        return {"error": "No files found!"}, 400

    uploaded_files = request.files.getlist("files")
    if not uploaded_files or all(file.filename == "" for file in uploaded_files):
        return {"error": "No valid files found!"}, 400

    files_data = {}
    if os.path.exists(SNAPSHOT_FILE):
        try:
            with open(SNAPSHOT_FILE, 'r') as f:
                files_data = json.load(f)
        except json.JSONDecodeError:
            files_data = {}
        except IOError as e:
            return {"error": f"Something went wrong: {str(e)}"}, 500

    new_files = []
    for file in uploaded_files:
        if file.filename == "":
            continue
        if not file.filename.endswith(ACCEPTED_EXTENSIONS):
            return {"error": f"Sorry, {file.filename} isn’t a valid file type! Only {', '.join(ACCEPTED_EXTENSIONS)} are allowed."}, 400
        try:
            file_content = file.read().decode('utf-8')
            new_files.append(file.filename)
            files_data[file.filename] = file_content
        except UnicodeDecodeError:
            return {"error": f"Couldn’t decode {file.filename}!"}, 400

    try:
        with open(SNAPSHOT_FILE, 'w') as f:
            json.dump(files_data, f, indent=4)
    except IOError as e:
        return {"error": f"Failed to save the snapshots! {str(e)}"}, 500

    # Send code to AI with a chuckle
    send_code_in_chunks(files_data)

    return {"message": "Files uploaded successfully!🎉"}, 200


# Get uploaded file names
def get_files():
    if not os.path.exists(SNAPSHOT_FILE):
        return [], 200

    try:
        with open(SNAPSHOT_FILE, 'r') as f:
            files_data = json.load(f)
    except json.JSONDecodeError:
        return {"error": "JSON file’s corrupted!, Please re-upload the files."}, 500
    except IOError as e:
        return {"error": f"Can’t access the snapshot file! {str(e)}"}, 500

    file_list = list(files_data.keys())
    if not file_list:
        return [], 200

    return file_list, 200


# Remove a file from uploaded files
def remove_file(file_name):
    if not os.path.exists(SNAPSHOT_FILE):
        return {"error": f"{file_name} not found"}, 404

    try:
        with open(SNAPSHOT_FILE, 'r') as f:
            files_data = json.load(f)
    except json.JSONDecodeError:
        return {"error": "JSON file’s corrupted!, Please re-upload the files."}, 500
    except IOError as e:
        return {"error": f"Can’t access the snapshot file! {str(e)}"}, 500

    if file_name not in files_data:
        return {"error": f"{file_name} not found"}, 404

    del files_data[file_name]

    try:
        with open(SNAPSHOT_FILE, 'w') as f:
            json.dump(files_data, f, indent=4)
    except IOError as e:
        return {"error": f"Failed to save the snapshots! {str(e)}"}, 500

    remove_file_from_memory(file_name)

    return {}, 204
