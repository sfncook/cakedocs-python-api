import os
import functions_framework
from vector_db import doIt
from clone_repo import clone_repo
from create_vdb import create_vdb
from query_vdb import query_vdb_for_context_docs
from query_llm import query_llm
from dotenv import load_dotenv
import pinecone

load_dotenv()

TEMP_DIR = os.environ.get("TEMP_DIR", "/Users/shawncook/Projects/CakeDocsAi/pythonEnv_3.8/tmp")
CODE_REPO_DIR = TEMP_DIR + "/code_repo"

PINECONE_API_KEY = os.environ.get("PINECONE_API_KEY", "PINECONE_API_KEY_NOT_SET")
PINECONE_ENVIRONMENT = os.environ.get("PINECONE_ENVIRONMENT", "PINECONE_ENVIRONMENT_NOT_SET")
PINECONE_INDEX = os.environ.get("PINECONE_INDEX", "PINECONE_INDEX_NOT_SET")
pinecone.init(api_key=PINECONE_API_KEY, environment=PINECONE_ENVIRONMENT)

@functions_framework.http
def http_llm(request):
    print(request.method)
    print(request.path)

    # Just for testing/debugging - should be handled by create_vdb
    if 'clone_repo' in request.path and request.method == 'POST':
        request_json = request.get_json(silent=True)
        return clone_repo(request_json['git_url'], CODE_REPO_DIR)

    if 'create_vdb' in request.path and request.method == 'POST':
        request_json = request.get_json(silent=True)
        repo_url = request_json['git_url']
        return create_vdb(repo_url, CODE_REPO_DIR, TEMP_DIR, PINECONE_INDEX)

    if 'query_vdb' in request.path and request.method == 'POST':
        request_json = request.get_json(silent=True)
        repo_url = request_json['git_url']
        query = request_json['query']
        return query_vdb_for_context_docs(query, PINECONE_INDEX, repo_url)

    if 'query_llm' in request.path and request.method == 'POST':
        request_json = request.get_json(silent=True)
        repo_url = request_json['git_url']
        query = request_json['query']
        context_docs = query_vdb_for_context_docs(query, PINECONE_INDEX, repo_url)
        return query_llm(query, context_docs)

