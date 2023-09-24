from main import http_llm
from create_vector_db import clone_repo

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

def test_clone_repo():
    git_url = 'https://github.com/sfncook/designGuiStatic'
    clone_repo(git_url)

if __name__ == '__main__':
    test_clone_repo()
#     test_llm_http()
