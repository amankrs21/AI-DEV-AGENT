import json
import requests

import chromadb
from sentence_transformers import SentenceTransformer

# Initialize ChromaDB and Embeddings
embedding_model = SentenceTransformer("all-MiniLM-L6-v2")
chroma_client = chromadb.PersistentClient(path="./chroma_db")


def fetch_relevant_code(project_name, user_request):
    """
    Fetches relevant files from ChromaDB based on the user query.
    """
    collection_name = f"project_{project_name.lower()}"

    try:
        collection = chroma_client.get_collection(name=collection_name)
    except:
        print(f"Error: Project '{project_name}' not found in ChromaDB.")
        return None

    # Embed the user request to find relevant files
    query_embedding = embedding_model.encode(user_request).tolist()
    results = collection.query(query_embeddings=[query_embedding], n_results=5)

    if not results["documents"][0]:
        print("⚠️ No relevant code found.")
        return None

    relevant_files = {
        results["metadatas"][0][i]["file"]: results["documents"][0][i]
        for i in range(len(results["documents"][0]))
    }

    return relevant_files




LLM_API_URL = "http://localhost:11434/api/generate"

def decide_files_to_update(project_name, user_request):
    """
    Uses LLM to decide which files need to be modified.
    """
    relevant_files = fetch_relevant_code(project_name, user_request)

    if not relevant_files:
        print("⚠️ No files found. LLM will create a new one.")
        return {"new_file": f"./{project_name}/blog.js"}

    # Format files for the LLM
    file_data = "\n\n".join(
        [f"### {file_path} ###\n```{code}```" for file_path, code in relevant_files.items()]
    )

    prompt = f"""
    You are analyzing a project and need to update it based on the following request:
    "{user_request}"

    Here are the relevant files in the project:
    {file_data}

    Based on the request, decide which files need modification.
    Provide a JSON response in the format:
    {{
        "update_files": ["file1.js", "file2.js"],
        "new_files": ["new_file.js"]
    }}
    """

    data = json.dumps({"model": "deepseek-r1:8b", "prompt": prompt, "stream": False})
    headers = {"Content-Type": "application/json"}
    response = requests.post(LLM_API_URL, headers=headers, data=data)

    print(response)
    if response.status_code == 200:
        return json.loads(response.json().get("response", "{}"))
    else:
        return {"error": "LLM decision-making failed."}


def update_project_based_on_llm_decision(project_name, user_request):
    """
    Gets files to update from LLM and modifies them.
    """
    decision = decide_files_to_update(project_name, user_request)

    if "error" in decision:
        print("❌ Error:", decision["error"])
        return

    updated_files = []

    # # Modify existing files
    # for file_path in decision.get("update_files", []):
    #     existing_code = open(file_path, "r", encoding="utf-8").read()
    #     new_code = generate_code_with_llm(existing_code, user_request)

    #     if "Error" not in new_code:
    #         with open(file_path, "w", encoding="utf-8") as file:
    #             file.write(new_code)
    #         updated_files.append(file_path)
    #         print(f"✅ Updated: {file_path}")

    # # Create new files if needed
    # for new_file_path in decision.get("new_files", []):
    #     new_code = generate_code_with_llm("", user_request)
    #     with open(new_file_path, "w", encoding="utf-8") as file:
    #         file.write(new_code)
    #     updated_files.append(new_file_path)
    #     print(f"🆕 Created new file: {new_file_path}")

    print("\n🎉 Project successfully updated!", decision)


# ** Example Usage **
if __name__ == "__main__":
    project_name = "React-Experiments"
    user_query = "Add a blog page at `/blog` route"

    update_project_based_on_llm_decision(project_name, user_query)
