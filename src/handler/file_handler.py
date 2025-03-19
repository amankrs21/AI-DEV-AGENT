import os
import json
from flask import request


# Function to save uploaded files
def save_files():
    if "files" not in request.files:
        return {"error": "No files uploaded"}, 400

    uploaded_files = request.files.getlist("files")
    
    # Create 'data' directory if it doesn't exist
    folder_name = request.remote_addr
    report_folder = os.path.join(os.getcwd(), "data", folder_name)
    if not os.path.exists(report_folder):
        os.makedirs(report_folder)

    # Path to uploaded files JSON
    report_file = os.path.join(report_folder, "uploaded_files.json")

    # Load existing data from JSON (if any)
    if os.path.exists(report_file):
        with open(report_file, 'r') as f:
            try:
                files_data = json.load(f)
            except json.JSONDecodeError:
                files_data = {}
    else:
        files_data = {}

    # Add or update file content in the JSON object
    for file in uploaded_files:
        if file.filename == "":
            continue
        file_content = file.read().decode('utf-8')
        files_data[file.filename] = file_content

    # Save updated data as JSON
    with open(report_file, 'w') as f:
        json.dump(files_data, f, indent=4)

    return {"message": "Files uploaded successfully"}, 200


# get uploaded files names
def get_files():
    folder_name = request.remote_addr
    report_folder = os.path.join(os.getcwd(), "data", folder_name)
    report_file = os.path.join(report_folder, "uploaded_files.json")

    # Load existing data from JSON (if any)
    if os.path.exists(report_file):
        with open(report_file, 'r') as f:
            try:
                files_data = json.load(f)
            except json.JSONDecodeError:
                files_data = {}
    else:
        return {"error": "No files uploaded"}, 400
        
    return list(files_data.keys())


# remove a file from uploaded files
def remove_file(file_name):
    folder_name = request.remote_addr
    report_folder = os.path.join(os.getcwd(), "data", folder_name)
    report_file = os.path.join(report_folder, "uploaded_files.json")

    # Load existing data from JSON (if any)
    if os.path.exists(report_file):
        with open(report_file, 'r') as f:
            try:
                files_data = json.load(f)
            except json.JSONDecodeError:
                files_data = {}
    else:
        return {"error": "No files uploaded"}, 400

    # Remove file from the JSON object
    if file_name in files_data.keys():
        files_data.pop(file_name)

    # Save updated data as JSON
    with open(report_file, 'w') as f:
        json.dump(files_data, f, indent=4)

    return {}, 204
