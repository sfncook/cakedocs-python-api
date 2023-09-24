import functions_framework
from vector_db import doIt
from git_clone import clone_repo

@functions_framework.http
def http_llm(request):
    print(request.method)
    print(request.path)
    if request.method == 'POST' and 'git_clone' in request.path:
        request_json = request.get_json(silent=True)
        return clone_repo(request_json['git_url'])
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
