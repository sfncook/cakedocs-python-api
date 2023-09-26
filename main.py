import os
import functions_framework
from vector_db import doIt
from clone_repo import clone_repo
from create_vdb import create_vdb
import pinecone

@functions_framework.http
def http_llm(request):
    print(request.method)
    print(request.path)

    TEMP_DIR = os.environ.get("TEMP_DIR", "/Users/shawncook/Projects/CakeDocsAi/pythonEnv_3.8/tmp")
    CODE_REPO_DIR = TEMP_DIR + "/code_repo"
#     PINECONE_API_KEY = os.environ.get("PINECONE_API_KEY", "PINECONE_API_KEY_NOT_SET")
#     PINECONE_ENVIRONMENT = os.environ.get("PINECONE_ENVIRONMENT", "PINECONE_ENVIRONMENT_NOT_SET")

    if 'clone_repo' in request.path and request.method == 'POST':
        request_json = request.get_json(silent=True)
        return clone_repo(request_json['git_url'], CODE_REPO_DIR)

    if 'create_vdb' in request.path and request.method == 'POST':
#         print(f"PINECONE_API_KEY: {PINECONE_API_KEY}")
#         print(f"PINECONE_ENVIRONMENT: {PINECONE_ENVIRONMENT}")
#         pinecone.init(api_key=PINECONE_API_KEY, environment=PINECONE_ENVIRONMENT)
#         print(pinecone.list_indexes())
#         return True
        request_json = request.get_json(silent=True)
        repo_name = request_json['git_url'].split('/')[-1]
        vdb_path = TEMP_DIR + "/vdb-" + repo_name + ".pkl"
        return create_vdb(request_json['git_url'], CODE_REPO_DIR, vdb_path)

#     return doIt()
#     request_json = request.get_json(silent=True)
#     request_args = request.args
#     if request_json and 'name' in request_json:
#         name = request_json['name']
#     elif request_args and 'name' in request_args:
#         name = request_args['name']
#     else:
#         name = 'World'
#     return 'Hello {}!'.format(name)
