from flask import Flask, request
from main import http_llm

app = Flask(__name__)

@app.route('/llm/query_llm', methods=['POST'])
def hello():
    return http_llm(request)

if __name__ == '__main__':
    app.run(debug=True)
