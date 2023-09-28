import os
import shutil
import subprocess
from utils import get_repo_name_from_url

def clone_repo(git_url, code_repo_path):
    repo_name = get_repo_name_from_url(git_url)
    repo_clone_dir = code_repo_path + "/" + repo_name
    print("Cloning the repo:[", git_url, "] repo_clone_dir:[", repo_clone_dir,"]")

    if not os.path.exists(code_repo_path):
        os.makedirs(code_repo_path)

    if os.path.exists(repo_clone_dir):
        shutil.rmtree(repo_clone_dir)
        print(f"Deleted directory '{repo_clone_dir}'")

    try:
        subprocess.check_call(['git', 'clone', git_url, repo_name], cwd=code_repo_path)
        print(f"Successfully cloned {git_url} into {repo_clone_dir}")
    except subprocess.CalledProcessError as e:
        print(f"Error: {e.output}")

    return repo_clone_dir
