import os
import functions_framework
from vector_db import doIt
from clone_repo import clone_repo
from create_vdb import create_vdb

@functions_framework.http
def http_llm(request):
    print(request.method)
    print(request.path)

    TEMP_DIR = os.environ.get("TEMP_DIR", "/Users/shawncook/Projects/CakeDocsAi/pythonEnv_3.8/tmp")
    CODE_REPO_DIR = TEMP_DIR + "/code_repo"

    if 'clone_repo' in request.path and request.method == 'POST':
        request_json = request.get_json(silent=True)
        return clone_repo(request_json['git_url'], CODE_REPO_DIR)

    if 'create_vdb' in request.path and request.method == 'POST':
        request_json = request.get_json(silent=True)
        repo_name = request_json['git_url'].split('/')[-1]
        vdb_path = TEMP_DIR + "/vdb-" + repo_name + ".pkl"
        return create_vdb(request_json['git_url'], CODE_REPO_DIR, vdb_path)

