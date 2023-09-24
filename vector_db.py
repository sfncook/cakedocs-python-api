import pickle
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

def load_local_vdb(vdb_path):
    with open(vdb_path, "rb") as f:
        faiss_store = pickle.load(f)
    return faiss_store

def generate_or_load_knowledge_from_repo():
    vdb_path = "vector-db.pkl"
    vdb = load_local_vdb(vdb_path)
    return vdb

def get_repo_context(query, vdb):
    matched_docs = vdb.similarity_search(query, k=10)
    output = ""
    for idx, docs in enumerate(matched_docs):
        output += f"Context {idx}:\n"
        output += str(docs)
        output += "\n\n"
    return output

def user_input_handler(input):
    vdb = generate_or_load_knowledge_from_repo()
    context = get_repo_context(input, vdb)
    prompt = input + "\n\n" + \
             f"Here are some contexts about the question, which are ranked by the relevance to the question: \n\n" + context
    return prompt

def generate_response(system_msg, inputs, top_p, temperature, chat_counter, chatbot=[], history=[]):
    orig_inputs = inputs

    # Inputs are pre-processed with extra tools
    inputs = user_input_handler(inputs)

    token_limit = 8000
    if len(inputs) > token_limit:
        inputs = inputs[:token_limit]

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {OPENAI_API_KEY}"
    }

    if system_msg.strip() == '':
        initial_message = [{"role": "user", "content": f"{inputs}"}]
        multi_turn_message = []
    else:
        initial_message = [{"role": "system", "content": system_msg},
                           {"role": "user", "content": f"{inputs}"}]
        multi_turn_message = [{"role": "system", "content": init_system_prompt}]

    if chat_counter == 0:
        payload = {
            "model": model,
            "messages": initial_message,
            "temperature": temperature,
            "top_p": top_p,
            "n": 1,
            "presence_penalty": 0,
            "frequency_penalty": 0,
        }
    else:
        messages = multi_turn_message
        for data in chatbot:
            user = {"role": "user", "content": data[0]}
            assistant = {"role": "assistant", "content": data[1]}
            messages.extend([user, assistant])
        temp = {"role": "user", "content": inputs}
        messages.append(temp)

        payload = {
            "model": model,
            "messages": messages,
            "temperature": temperature,
            "top_p": top_p,
            "n": 1,
            "presence_penalty": 0,
            "frequency_penalty": 0, }

    chat_counter += 1
    history.append(orig_inputs)
    print("Sending request to OpenAI API...")
    response = requests.post(API_URL, headers=headers, json=payload)
    print(response.json()['choices'][0]['message']['content'])
    return response
#     token_counter = 0
#     partial_words = ""
#
#     response_complete = False
#
#     counter = 0
#     for chunk in response.iter_lines():
#         if counter == 0:
#             counter += 1
#             continue
#
#         if response_complete:
#             print(colored("Response: ", "yellow"), colored(partial_words, "yellow"))
#
#         if chunk.decode():
#             chunk = chunk.decode()
#             if chunk.startswith("error:"):
#                 print(colored("Chunk: ", "red"), colored(chunk, "red"))
#
#             # Check if the chatbot is done generating the response
#             try:
#                 if len(chunk) > 12 and "finish_reason" in json.loads(chunk[6:])['choices'][0]:
#                     response_complete = json.loads(chunk[6:])['choices'][0].get("finish_reason", None) == "stop"
#             except:
#                 print("Error in response_complete check")
#                 pass
#
#             try:
#                 if len(chunk) > 12 and "content" in json.loads(chunk[6:])['choices'][0]['delta']:
#                     partial_words = partial_words + json.loads(chunk[6:])['choices'][0]["delta"]["content"]
#                     if token_counter == 0:
#                         history.append(" " + partial_words)
#                     else:
#                         history[-1] = partial_words
#                     chat = [(history[i], history[i + 1]) for i in range(0, len(history) - 1, 2)]
#                     token_counter += 1
#                     yield chat, history, chat_counter, response
#             except:
#                 print("Error in partial_words check")
#                 pass

def doIt():
    system_msg = init_system_prompt
    inputs = "What is the usage of this repo?"
    top_p = 0.5
    temperature = 1
    chat_counter = 0
    chatbot = []
    history = []
    return generate_response(system_msg, inputs, top_p, temperature, chat_counter, chatbot, history)