"""Test Hugging Face API connectivity and basic operations."""
import sys

HF_USER = "dl1010"
HF_TOKEN = "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"
SPACE_NAME = "entropygate-api"

print("[1/3] Testing HF API import and login...")
try:
    from huggingface_hub import HfApi, whoami
    api = HfApi(token=HF_TOKEN)
    user = whoami(token=HF_TOKEN)
    print(f"  Logged in as: {user['name']}")
except Exception as e:
    print(f"  FAILED: {e}")
    sys.exit(1)

print("\n[2/3] Testing repo listing...")
try:
    repos = api.list_repos(
        repo_type="space",
        author=HF_USER,
    )
    repo_list = list(repos)
    print(f"  Found {len(repo_list)} spaces:")
    for r in repo_list[:5]:
        print(f"    - {r.id}")
except Exception as e:
    print(f"  FAILED: {e}")
    import traceback
    traceback.print_exc()

print("\n[3/3] Testing file upload (small test file)...")
try:
    import tempfile, os
    with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False, encoding='utf-8') as f:
        f.write("test file for deployment\n")
        test_file = f.name
    
    print(f"  Uploading test file to {HF_USER}/{SPACE_NAME}...")
    api.upload_file(
        path_or_fileobj=test_file,
        path_in_repo="test_deploy.txt",
        repo_id=f"{HF_USER}/{SPACE_NAME}",
        repo_type="space",
        commit_message="test upload",
    )
    print("  Upload SUCCESS!")
    os.unlink(test_file)
except Exception as e:
    print(f"  FAILED: {e}")
    import traceback
    traceback.print_exc()

print("\nDone!")
