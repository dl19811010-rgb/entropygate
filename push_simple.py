import requests
import os
import base64

GITHUB_TOKEN = os.getenv("GITHUB_TOKEN", "")
REPO_OWNER = "dl19811010-rgb"
REPO_NAME = "entropygate"
BRANCH = "main"

def upload_file(rel_path, content):
    url = f"https://api.github.com/repos/{REPO_OWNER}/{REPO_NAME}/contents/{rel_path}"
    headers = {"Authorization": f"token {GITHUB_TOKEN}", "Content-Type": "application/json"}
    
    b64_content = base64.b64encode(content).decode('utf-8')
    
    sha = None
    try:
        response = requests.get(url, headers=headers, timeout=10)
        if response.status_code == 200:
            sha = response.json()["sha"]
    except:
        pass
    
    payload = {
        "message": f"Update {rel_path}",
        "content": b64_content,
        "branch": BRANCH
    }
    if sha:
        payload["sha"] = sha
    
    try:
        response = requests.put(url, headers=headers, json=payload, timeout=30)
        if response.status_code in [200, 201]:
            return True
        else:
            print(f"  Failed {rel_path}: {response.status_code}")
            return False
    except Exception as e:
        print(f"  Error {rel_path}: {e}")
        return False

def collect_files(root_dir):
    files = []
    exclude_dirs = ['.git', 'node_modules', '__pycache__', '.vscode', 'dist', 'build', 'logs', 'venv']
    exclude_files = ['.env', '.db', '.sqlite', '.log', '.pyc', '.pyo']
    
    for dirpath, dirnames, filenames in os.walk(root_dir):
        dirnames[:] = [d for d in dirnames if d not in exclude_dirs]
        
        for filename in filenames:
            should_exclude = False
            for ext in exclude_files:
                if filename.endswith(ext):
                    should_exclude = True
                    break
            if should_exclude:
                continue
            
            filepath = os.path.join(dirpath, filename)
            rel_path = os.path.relpath(filepath, root_dir).replace("\\", "/")
            
            try:
                with open(filepath, 'rb') as f:
                    content = f.read()
                files.append((rel_path, content))
            except Exception as e:
                print(f"Skip {rel_path}: {e}")
    
    return files

def main():
    print("Collecting files...")
    files = collect_files(".")
    print(f"Total files: {len(files)}")
    
    print("\nUploading files to GitHub...")
    success_count = 0
    fail_count = 0
    
    for i, (rel_path, content) in enumerate(files):
        print(f"{i+1}/{len(files)}: {rel_path}")
        if upload_file(rel_path, content):
            success_count += 1
        else:
            fail_count += 1
    
    print(f"\nDone! Success: {success_count}, Failed: {fail_count}")

if __name__ == "__main__":
    main()
