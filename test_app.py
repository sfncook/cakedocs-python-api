from main import http_llm
from clone_repo import clone_repo
from upload_vdb import upload_vdb
import yaml
import os

try:
    with open('../.env.yaml', 'r') as yaml_file:
        env_vars = yaml.safe_load(yaml_file)
        print("setting env vars")
        for key, value in env_vars.items():
            os.environ[key] = value

except FileNotFoundError:
    print(f"YAML file '{yaml_file_path}' not found.")

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

def test_llm_upload_vdb():
    upload_vdb("/Users/shawncook/Projects/CakeDocsAi/pythonEnv_3.8/tmp/vdb-designGuiStatic.pkl", 'vdb-designGuiStatic.pkl')

def test_clone_repo():
    git_url = 'https://github.com/sfncook/designGuiStatic'
    print(clone_repo(git_url))

if __name__ == '__main__':
#     test_clone_repo()
#     test_llm_http()
#     test_llm_git_clone()
    test_llm_create_vdb()
#     test_llm_upload_vdb()
