from main import http_llm
from clone_repo import clone_repo
from upload_vdb import upload_vdb
import os

# Create a mock Flask request object to simulate an HTTP request
class MockRequest:
    def __init__(self, json_data=None, args=None):
        self.json_data = json_data
        self.args = args

    def get_json(self, silent=True):
        return self.json_data

def test_llm_http():
    request = MockRequest(json_data={'name': 'Alice'})
    response = http_llm(request)
    print(response)

# I think this is deprecated and not used anymore
def test_llm_upload_vdb():
    upload_vdb("/Users/shawncook/Projects/CakeDocsAi/pythonEnv_3.8/tmp/vdb-designGuiStatic.pkl", 'vdb-designGuiStatic.pkl')

def test_llm_git_clone():
    request = MockRequest(json_data={'git_url': 'https://github.com/sfncook/hello'})
    request.path = '/clone_repo'
    request.method = 'POST'
    response = http_llm(request)
    print(response)

def test_llm_create_vdb():
    request = MockRequest(json_data={'git_url': 'https://github.com/sfncook/hello'})
    request.path = '/create_vdb'
    request.method = 'POST'
    response = http_llm(request)
    print(response)

def test_llm_query_vdb():
    request = MockRequest(json_data={'git_url': 'https://github.com/sfncook/hello', 'query': 'Describe this repo'})
    request.path = '/query_vdb'
    request.method = 'POST'
    response = http_llm(request)
    print(response)

def test_llm_query_llm():
    request = MockRequest(json_data={'git_url': 'https://github.com/sfncook/hello', 'query': 'Describe this repo'})
    request.path = '/query_llm'
    request.method = 'POST'
    response = http_llm(request)
    print(response)

if __name__ == '__main__':
#     test_clone_repo()
#     test_llm_http()
#     test_llm_git_clone()
#     test_llm_create_vdb()
#     test_llm_query_vdb()
    test_llm_query_llm()
