import os
import json
import openai

OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY", "null")
API_URL = "https://api.openai.com/v1/chat/completions"
model = "gpt-3.5-turbo"
# model = "gpt-4-0613"

openai.api_key = os.getenv("OPENAI_API_KEY")

init_system_prompt = """
    You are an expert software engineer who is explaining and sometimes writing documentation that describes a code repository.
    You will be provided with some code snippets or documents from the repository.  Answer the user's questions to the best of your ability.
    You can ask the user for clarifying information if it is unclear what they want.
    You should modify your response based on the user's level of experience.  You can ask the user for their level of experience with software.
    You should always try to provide examples from the code or documents provided in order to help support your answer.
    Do not mention the "context 0", "context 1", etc. in your response.  You may mention the filename of the context, but not the index of the context document.
"""

def query_llm(query, context_docs, msgs):
    print("Sending request to OpenAI API...")
    prompt = query + f"\n\nHere are some contexts about the question, which are ranked by the relevance to the question: \n\n"
    for idx, doc in enumerate(context_docs):
        prompt += f"Context {idx}:\n"
        prompt += str(doc)
        prompt += "\n\n"
    token_limit = 8000
    if len(prompt) > token_limit:
        prompt = inputs[:token_limit]

    messages = [{"role": 'system', "content": init_system_prompt}]
    for msg in msgs:
#         print(json.dumps(msg))
        messages.append({"role": msg['role'].lower(), "content": msg['msg']})
#     print(json.dumps(messages))

    # Add the user's current query to then end of messages
    messages.append({"role": "user", "content": f"{prompt}"})

    response = openai.ChatCompletion.create(
        model=model,
        messages=messages,
        temperature=1,
        top_p=0.5,
    )
    assistant_response = response.choices[0].message.content
    print(assistant_response)
    return assistant_response

def analyze_repo_for_language(repo_file_list):
    response = openai.ChatCompletion.create(
        model=model,
        messages=messages,
        temperature=1,
        top_p=0.5,
    )
    assistant_response = response.choices[0].message.content
    print(assistant_response)
    return assistant_response