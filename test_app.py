from main import http_llm

# Create a mock Flask request object to simulate an HTTP request
class MockRequest:
    def __init__(self, json_data=None, args=None):
        self.json_data = json_data
        self.args = args

    def get_json(self, silent=True):
        return self.json_data

# Test your Cloud Function
def test_hello_http():
    # Create a mock request with the desired JSON data or query parameters
    request = MockRequest(json_data={'name': 'Alice'})
    response = http_llm(request)

    print(response)
    # Assert that the response matches the expected output
    assert response == 'Hello Alice!'

if __name__ == '__main__':
    test_hello_http()
