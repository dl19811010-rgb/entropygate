import requests
import os

GITHUB_TOKEN = os.getenv("GITHUB_TOKEN", "")
REPO_OWNER = "dl19811010-rgb"
REPO_NAME = "entropygate"

proxies = {
    "http": "http://127.0.0.1:7890",
    "https": "http://127.0.0.1:7890"
}

def test_connection():
    url = f"https://api.github.com/repos/{REPO_OWNER}/{REPO_NAME}"
    headers = {"Authorization": f"token {GITHUB_TOKEN}"}
    
    print("Test 1: Direct connection...")
    try:
        response = requests.get(url, headers=headers, timeout=10)
        print(f"  Status: {response.status_code}")
        if response.status_code == 200:
            print("  SUCCESS!")
            return True
    except Exception as e:
        print(f"  FAILED: {e}")
    
    print("\nTest 2: With proxy...")
    try:
        response = requests.get(url, headers=headers, proxies=proxies, timeout=10)
        print(f"  Status: {response.status_code}")
        if response.status_code == 200:
            print("  SUCCESS!")
            return True
    except Exception as e:
        print(f"  FAILED: {e}")
    
    print("\nTest 3: ghproxy...")
    try:
        ghproxy_url = f"https://ghproxy.com/{url}"
        response = requests.get(ghproxy_url, headers=headers, timeout=10)
        print(f"  Status: {response.status_code}")
        if response.status_code == 200:
            print("  SUCCESS!")
            return True
    except Exception as e:
        print(f"  FAILED: {e}")
    
    return False

if __name__ == "__main__":
    test_connection()
