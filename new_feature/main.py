from llm_setup import call_llm

project_name = "React-Experiments"
project_path = "/home/singh/CODES/Secure-Vault/"

if __name__ == "__main__":
    
    user_feature_input = "Logic to create a new route as `blog`."

    prompt = f"""
    My project is {project_name}.
    
    I need a feature that does the following: {user_feature_input}
    
    My folder structure base_path is {project_path}.
    
    
    """