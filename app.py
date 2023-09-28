from flask import Flask, request
from main import http_llm

app = Flask(__name__)

@app.route('/llm/query_llm', methods=['POST'])
def query_llm():
    return http_llm(request)

@app.route('/llm/create_vdb', methods=['POST'])
def create_vdb():
    return http_llm(request)

@app.route('/llm/clone_repo', methods=['POST'])
def clone_repo():
    return http_llm(request)

if __name__ == '__main__':
    app.run(debug=True)
