import os
import requests

OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY", "null")
API_URL = "https://api.openai.com/v1/chat/completions"
model = "gpt-3.5-turbo"

init_system_prompt = """Now you are an expert programmer and teacher of a code repository.
    You will be asked to explain the code for a specific task in the repo.
    You will be provided with some related code snippets or documents related to the question.
    Please think the explanation step-by-step.
    Please answer the questions based on your knowledge, and you can also refer to the provided related code snippets.
    The README.md file and the repo structure are also available for your reference.
    If you need any details clarified, please ask questions until all issues are clarified. \n\n
"""

def query_llm(query, context_docs):
    print("Sending request to OpenAI API...")
    prompt = query + f"\n\nHere are some contexts about the question, which are ranked by the relevance to the question: \n\n"
    for idx, doc in enumerate(context_docs):
        prompt += f"Context {idx}:\n"
        prompt += str(doc)
        prompt += "\n\n"
    token_limit = 8000
    if len(prompt) > token_limit:
        prompt = inputs[:token_limit]

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {OPENAI_API_KEY}"
    }

    message = [{"role": "user", "content": f"{prompt}"}]
    temperature = 1
    top_p = 0.5
    payload = {
        "model": model,
        "messages": message,
        "temperature": temperature,
        "top_p": top_p,
        "n": 1,
        "presence_penalty": 0,
        "frequency_penalty": 0,
    }
    response = requests.post(API_URL, headers=headers, json=payload)
    response_content = response.json()['choices'][0]['message']['content']
    print(response_content)
    print("Response received.")
    return response_content
