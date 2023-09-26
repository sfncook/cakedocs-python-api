from main import http_llm

# Create a mock Flask request object to simulate an HTTP request
class MockRequest:
    def __init__(self, json_data=None, args=None):
        self.json_data = json_data
        self.args = args

    def get_json(self, silent=True):
        return self.json_data

def test_llm_clone_repo():
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
#     test_llm_clone_repo()
#     test_llm_create_vdb()
#     test_llm_query_vdb()
    test_llm_query_llm()
