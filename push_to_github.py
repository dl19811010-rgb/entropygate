import requests
import json
import os
import base64

GITHUB_TOKEN = os.getenv("GITHUB_TOKEN", "")
REPO_OWNER = "dl19811010-rgb"
REPO_NAME = "entropygate"
BRANCH = "main"

def get_branch_sha():
    url = f"https://api.github.com/repos/{REPO_OWNER}/{REPO_NAME}/git/refs/heads/{BRANCH}"
    headers = {"Authorization": f"token {GITHUB_TOKEN}"}
    try:
        response = requests.get(url, headers=headers, timeout=30)
        if response.status_code == 200:
            return response.json()["object"]["sha"]
        elif response.status_code == 404:
            return None
        else:
            print(f"Failed to get branch: {response.status_code}")
            return None
    except Exception as e:
        print(f"Error getting branch: {e}")
        return None

def get_tree(sha):
    url = f"https://api.github.com/repos/{REPO_OWNER}/{REPO_NAME}/git/trees/{sha}?recursive=1"
    headers = {"Authorization": f"token {GITHUB_TOKEN}"}
    try:
        response = requests.get(url, headers=headers, timeout=30)
        if response.status_code == 200:
            return response.json()["tree"]
        else:
            print(f"Failed to get tree: {response.status_code}")
            return []
    except Exception as e:
        print(f"Error getting tree: {e}")
        return []

def create_blob(content):
    url = f"https://api.github.com/repos/{REPO_OWNER}/{REPO_NAME}/git/blobs"
    headers = {"Authorization": f"token {GITHUB_TOKEN}", "Content-Type": "application/json"}
    payload = {
        "content": content,
        "encoding": "base64"
    }
    try:
        response = requests.post(url, headers=headers, data=json.dumps(payload), timeout=30)
        if response.status_code == 201:
            return response.json()["sha"]
        else:
            print(f"Failed to create blob: {response.status_code}, {response.text}")
            return None
    except Exception as e:
        print(f"Error creating blob: {e}")
        return None

def create_tree(base_tree_sha, items):
    url = f"https://api.github.com/repos/{REPO_OWNER}/{REPO_NAME}/git/trees"
    headers = {"Authorization": f"token {GITHUB_TOKEN}", "Content-Type": "application/json"}
    payload = {
        "base_tree": base_tree_sha,
        "tree": items
    }
    try:
        response = requests.post(url, headers=headers, data=json.dumps(payload), timeout=30)
        if response.status_code == 201:
            return response.json()["sha"]
        else:
            print(f"Failed to create tree: {response.status_code}, {response.text}")
            return None
    except Exception as e:
        print(f"Error creating tree: {e}")
        return None

def create_commit(parent_sha, tree_sha, message):
    url = f"https://api.github.com/repos/{REPO_OWNER}/{REPO_NAME}/git/commits"
    headers = {"Authorization": f"token {GITHUB_TOKEN}", "Content-Type": "application/json"}
    payload = {
        "message": message,
        "parents": [parent_sha] if parent_sha else [],
        "tree": tree_sha
    }
    try:
        response = requests.post(url, headers=headers, data=json.dumps(payload), timeout=30)
        if response.status_code == 201:
            return response.json()["sha"]
        else:
            print(f"Failed to create commit: {response.status_code}, {response.text}")
            return None
    except Exception as e:
        print(f"Error creating commit: {e}")
        return None

def update_ref(commit_sha):
    url = f"https://api.github.com/repos/{REPO_OWNER}/{REPO_NAME}/git/refs/heads/{BRANCH}"
    headers = {"Authorization": f"token {GITHUB_TOKEN}", "Content-Type": "application/json"}
    payload = {"sha": commit_sha, "force": True}
    try:
        response = requests.patch(url, headers=headers, data=json.dumps(payload), timeout=30)
        if response.status_code == 200:
            print(f"Successfully pushed to {BRANCH}!")
            return True
        else:
            print(f"Failed to update ref: {response.status_code}, {response.text}")
            return False
    except Exception as e:
        print(f"Error updating ref: {e}")
        return False

def collect_files(root_dir, exclude_dirs=None, exclude_files=None):
    files = []
    exclude_dirs = exclude_dirs or ['.git', 'node_modules', '__pycache__', '.vscode', 'dist', 'build', 'logs', 'venv']
    exclude_files = exclude_files or ['.env', '.db', '.sqlite', '.log', '.pyc', '.pyo']
    
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
                b64_content = base64.b64encode(content).decode('utf-8')
                files.append((rel_path, b64_content))
                print(f"Added: {rel_path}")
            except Exception as e:
                print(f"Skip {rel_path}: {e}")
    
    return files

def main():
    print("Collecting files...")
    files = collect_files(".")
    print(f"Total files to upload: {len(files)}")
    
    print("\nGetting branch info...")
    branch_sha = get_branch_sha()
    print(f"Current branch SHA: {branch_sha}")
    
    print("\nUploading files as blobs...")
    tree_items = []
    for rel_path, b64_content in files:
        sha = create_blob(b64_content)
        if sha:
            tree_items.append({
                "path": rel_path,
                "mode": "100644",
                "type": "blob",
                "sha": sha
            })
            print(f"Uploaded: {rel_path}")
    
    print(f"\nCreating tree with {len(tree_items)} items...")
    parent_tree_sha = None
    if branch_sha:
        try:
            commit_info = requests.get(
                f"https://api.github.com/repos/{REPO_OWNER}/{REPO_NAME}/git/commits/{branch_sha}",
                headers={"Authorization": f"token {GITHUB_TOKEN}"},
                timeout=30
            )
            if commit_info.status_code == 200:
                parent_tree_sha = commit_info.json()["tree"]["sha"]
                print(f"  Parent tree SHA: {parent_tree_sha}")
        except Exception as e:
            print(f"  Failed to get parent tree: {e}")
    
    tree_sha = None
    if parent_tree_sha:
        tree_sha = create_tree(parent_tree_sha, tree_items)
    else:
        url = f"https://api.github.com/repos/{REPO_OWNER}/{REPO_NAME}/git/trees"
        headers = {"Authorization": f"token {GITHUB_TOKEN}", "Content-Type": "application/json"}
        payload = {"tree": tree_items}
        try:
            response = requests.post(url, headers=headers, data=json.dumps(payload), timeout=30)
            if response.status_code == 201:
                tree_sha = response.json()["sha"]
                print(f"  Created new tree: {tree_sha}")
            else:
                print(f"  Failed to create tree: {response.status_code}, {response.text}")
        except Exception as e:
            print(f"  Error creating tree: {e}")
    
    if not tree_sha:
        print("Failed to create tree")
        return
    
    print(f"\nCreating commit...")
    commit_sha = create_commit(branch_sha, tree_sha, "Initial commit: AI News full stack project")
    
    if not commit_sha:
        print("Failed to create commit")
        return
    
    print(f"\nUpdating reference...")
    success = update_ref(commit_sha)
    
    if success:
        print(f"\n✅ Successfully pushed to https://github.com/{REPO_OWNER}/{REPO_NAME}")
    else:
        print("\n❌ Push failed")

if __name__ == "__main__":
    main()
