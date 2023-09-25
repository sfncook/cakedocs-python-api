import functions_framework
import os
from vector_db import doIt
from clone_repo import clone_repo
from create_vdb import create_vdb

TEMP_DIR = os.environ.get("TEMP_DIR", "/Users/shawncook/Projects/CakeDocsAi/pythonEnv_3.8/tmp")
CODE_REPO_DIR = TEMP_DIR + "/code_repo"

@functions_framework.http
def http_llm(request):
    print(request.method)
    print(request.path)
    if request.method == 'POST' and 'clone_repo' in request.path:
        request_json = request.get_json(silent=True)
        return clone_repo(request_json['git_url'], CODE_REPO_DIR)
    if request.method == 'POST' and 'create_vdb' in request.path:
        request_json = request.get_json(silent=True)
        return create_vdb(request_json['git_url'])
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
