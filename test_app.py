from main import http_llm

# Create a mock Flask request object to simulate an HTTP request
class MockRequest:
    def __init__(self, json_data=None, args=None):
        self.json_data = json_data
        self.args = args

    def get_json(self, silent=True):
        return self.json_data

def test_llm_clone_repo():
    request = MockRequest(json_data={'repo_url': 'https://github.com/sfncook/hello'})
    request.path = '/clone_repo'
    request.method = 'POST'
    response = http_llm(request)
    print(response)

def test_llm_create_vdb():
    request = MockRequest(json_data={'repo_url': 'https://github.com/sfncook/hello'})
    request.path = '/create_vdb'
    request.method = 'POST'
    response = http_llm(request)
    print(response)

def test_llm_query_vdb():
    request = MockRequest(json_data={'repo_url': 'https://github.com/sfncook/gpt-interview-coach', 'query': 'What languages and tools are used in this repo?'})
    request.path = '/query_vdb'
    request.method = 'POST'
    response = http_llm(request)
    print(response)

def test_llm_query_llm():
    request = MockRequest(json_data={
        'repo_url': 'https://github.com/sfncook/gpt-interview-coach',
        'query': 'Describe this repo',
        'msgs':[{"id":"73593073-b7a6-499d-acf9-1545008e253e","msg":"asdf","role":"USER"},{"id":"4004b621-7517-4d24-a400-1dafe63c88e7","msg":"Based on the provided contexts, it is difficult to determine the relevance of the question \"asdf\" to any specific context. The question does not seem to be related to any of the provided contexts, which include CSS code, package.json file content, and font-face declarations.","role":"ASSISTANT"},{"id":"bcba013e-c4d9-4833-9671-6ea943e83b40","msg":"Testing","role":"USER"},{"id":"93f6f897-ea32-4d1d-850b-5aa6050d955e","msg":"Context 0 is the most relevant to the question as it contains the code snippet that defines the Response component. The code snippet includes the logic for rendering the rating, strengths, weaknesses, and example elements based on the provided props.\n\nContext 3 is also relevant as it provides additional information about the state variables and useEffect hook used in the Response component.\n\nContext 2 is less relevant as it contains code related to handling form submission and fetching data from an API, which is not directly related to the rendering logic of the Response component.\n\nContext 1 is not relevant to the question as it contains CSS styling code for the index page, which is unrelated to the Response component.","role":"ASSISTANT"},{"id":"de2fc906-cd56-49a4-879a-8f21675aa64f","msg":"qwer","role":"USER"},{"id":"6a284500-7836-405a-b275-567df1fc99a3","msg":"I'm sorry, but I'm not sure what you're asking. Can you please provide more information or clarify your question?","role":"ASSISTANT"},{"id":"23163c59-9428-4aaa-a56b-199a037c4cb8","msg":"Hola","role":"USER"},{"id":"4638ffc8-d024-40a0-b24e-3192d20c1ee0","msg":"Based on the relevance to the question, the most relevant context is Context 0.","role":"ASSISTANT"},{"id":"aa54837c-1e5a-4f64-bcdb-225a9d893877","msg":"yo mother","role":"USER"}]
    })
    request.path = '/query_llm'
    request.method = 'POST'
    response = http_llm(request)
    print(response)

if __name__ == '__main__':
    test_llm_query_llm()
