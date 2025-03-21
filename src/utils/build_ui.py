# importing required modules
import os
import subprocess


# Function to build React UI
def build_react():
    frontend_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../client"))
    
    print("⚡ Building Vite UI...")

    try:
        subprocess.run(["npm", "install"], cwd=frontend_path, check=True)
        subprocess.run(["npm", "run", "build"], cwd=frontend_path, check=True)
    except subprocess.CalledProcessError as e:
        print(f"❌ Vite build failed: {e}")
        return

    print("✅ Vite UI built successfully!")
