import os
import json
import openai

OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY", "null")
API_URL = "https://api.openai.com/v1/chat/completions"
# model = "gpt-3.5-turbo"
model = "gpt-4-0613"

openai.api_key = os.getenv("OPENAI_API_KEY")

init_system_prompt = """
    You are an expert software engineer who is explaining and sometimes writing documentation that describes a code repository.
    You will be provided with some code snippets or documents from the repository.  Answer the user's questions to the best of your ability.
    You can ask the user for clarifying information if it is unclear what they want.
    You should modify your response based on the user's level of experience.  You can ask the user for their level of experience with software.
    You should always try to provide examples from the code or documents provided in order to help support your answer.
"""

def query_llm(query, context_docs, msgs):
    print("Sending request to OpenAI API...")
    prompt = query + f"\n\nHere are a few files from the repository that are relevant to the question.  These files are ranked in order of relevance from most-to-least relevant: \n\n"
    for idx, doc in enumerate(context_docs):
        prompt += f"File {idx+1}:\n"
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
#     print("\nmsgs from client:")
#     for msg in msgs:
#         print(json.dumps(msg))
#
#     print("\nmessages sent to OAI:")
#     for msg in messages:
# #         print(json.dumps(msg))
#         print( msg['role'] + ":" + msg['content'][0:20])
#     print('\n')

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