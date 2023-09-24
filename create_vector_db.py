import os
import json
from langchain.text_splitter import RecursiveCharacterTextSplitter, CharacterTextSplitter
from langchain.document_loaders import TextLoader, PyPDFLoader
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores import FAISS, SupabaseVectorStore
import pickle
import subprocess
from langchain.chat_models import ChatOpenAI
from langchain.schema import HumanMessage, SystemMessage
from pathlib import Path
from collections import deque

TEMP_DIR = os.environ.get("TEMP_DIR", "/Users/shawncook/Projects/CakeDocsAi/pythonEnv_3.8/tmp")

def local_vdb(knowledge, vdb_path=None):
    embedding = OpenAIEmbeddings(disallowed_special=())
    print("Embedding documents...")
    faiss_store = FAISS.from_documents(knowledge["known_docs"], embedding=embedding)
    if vdb_path is not None:
        with open(vdb_path, "wb") as f:
            pickle.dump(faiss_store, f)
    return faiss_store

def load_documents(filenames):
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1500,
        chunk_overlap=200,
        length_function=len,
    )
    docs = []
    for filename in filenames:
        if filename.endswith(".pdf"):
            loader = PyPDFLoader(filename)
        else:
            loader = TextLoader(filename)
        documents = loader.load()
        splits = text_splitter.split_documents(documents)
        docs.extend(splits)
        print(f"Split {filename} into {len(splits)} chunks")
    return docs

def generate_knowledge_from_repo(dir_path, ignore_list):
    knowledge = {"known_docs": [], "known_text": {"pages": [], "metadatas": []}}
    for root, dirs, files in os.walk(dir_path):
        dirs[:] = [d for d in dirs if d not in ignore_list]  # modify dirs in-place
        for file in files:
            if file in ignore_list:
                continue
            filepath = os.path.join(root, file)
            try:
                # Using a more general way for code file parsing
                knowledge["known_docs"].extend(load_documents([filepath]))

            except Exception as e:
                print(f"Failed to process {filepath} due to error: {str(e)}")

    return knowledge

def get_repo_names(dir_path):
    folder_names = [name for name in os.listdir(dir_path) if os.path.isdir(os.path.join(dir_path, name))]
    concatenated_names = "-".join(folder_names)
    return concatenated_names

def generate_or_load_knowledge_from_repo(code_repo_path):
    vdb_path = "./vdb-" + get_repo_names(code_repo_path) + ".pkl"
    ignore_list = ['.git', 'node_modules', '__pycache__', '.idea', '.vscode']
    knowledge = generate_knowledge_from_repo(code_repo_path, ignore_list)
    vdb = local_vdb(knowledge, vdb_path=vdb_path)
    print("VDB generated!")
    return vdb

def find_readme(repo_folder):
    # Search for the README file within the found folder
    for filename in os.listdir(repo_folder):
        if filename.lower().startswith('readme'):
            readme_path = os.path.join(repo_folder, filename)
            print("README found in folder:", repo_folder)
            return readme_path

    print("README not found in folder:", repo_folder)
    return None

def find_repo_folder(directory):
    # Find the name of the folder in the specified directory
    folder_name = None
    for item in os.listdir(directory):
        item_path = os.path.join(directory, item)
        if os.path.isdir(item_path):
            folder_name = item
            break
    return os.path.join(directory, folder_name)

def get_chat_response(system_prompt, user_prompt):
    chat = ChatOpenAI(model_name=model, temperature=temperature)
    messages = [
        SystemMessage(content=system_prompt),
        HumanMessage(content=user_prompt)
    ]
    response = chat(messages)
    print(response)
    return response.content

def summarize_readme(readme_path):
    if readme_path:
        print("Summarizing README...")

        system_prompt = """You are an expert developer and programmer.
            Please infer the programming languages from the README.
            You are asked to summarize the README file of the code repository in detail.
            Provide enough information about the code repository.
            Please also mention the framework used in the code repository.
            """
        readme_content = open(readme_path, "r").read()
        user_prompt = f'Here is the README content: {readme_content}'
        return get_chat_response(system_prompt, user_prompt)

def get_readme(code_repo_path="./code_repo"):
    repo_folder = find_repo_folder(code_repo_path)
    print("Repo folder: " + repo_folder)
    readme_path = find_readme(repo_folder)
    if readme_path is None:
        return "README not found"
    else:
        summary = summarize_readme(readme_path)
        print("README Summary: ", summary)
        return summary

def bfs_folder_search(text_length_limit=4000, folder_path="./code_repo"):
    if not Path(folder_path).is_dir():
        return "Invalid directory path"

    root = Path(folder_path).resolve()
    file_structure = {str(root): {}}
    queue = deque([(root, file_structure[str(root)])])

    while queue:
        current_dir, parent_node = queue.popleft()
        try:
            for path in current_dir.iterdir():
                if path.is_dir():
                    if str(path.name) == ".git":
                        continue
                    parent_node[str(path.name)] = {"files": []}
                    queue.append((path, parent_node[str(path.name)]))
                else:
                    if "files" not in parent_node:
                        parent_node["files"] = []
                    parent_node["files"].append(str(path.name))

                # Check if we've exceeded the text length limit
                file_structure_text = json.dumps(file_structure)
                if len(file_structure_text) >= text_length_limit:
                    return file_structure_text

        except PermissionError:
            # This can happen in directories the user doesn't have permission to read.
            continue

    return json.dumps(file_structure)

def get_repo_structure(code_repo_path="./code_repo"):
    return bfs_folder_search(4000, code_repo_path)

def clone_repo(git_url):
    code_repo_path = TEMP_DIR + "/code_repo"
    print("Cloning the repo:[", git_url, "] code_repo_path:[", code_repo_path,"]")
    # Check if directory exists
    if not os.path.exists(code_repo_path):
        os.makedirs(code_repo_path)
    try:
        subprocess.check_call(['git', 'clone', git_url], cwd=code_repo_path)
        print(f"Successfully cloned {git_url} into {code_repo_path}")
    except subprocess.CalledProcessError as e:
        print(f"Error: {e.output}")

    print("Summarizing the repo...")
    readme_info = get_readme(code_repo_path)
    if readme_info is not None:
        readme_info = """The README.md file is as follows: """ + readme_info + "\n\n"

    print("Parsing repo structure...")
    repo_structure = get_repo_structure(code_repo_path)
    if repo_structure is not None:
        repo_structure = """The repo structure is as follows: """ + get_repo_structure(code_repo_path) + "\n\n"

    return readme_info + repo_structure

def analyze_repo(repo_url):
    repo_information = clone_repo(repo_url)
    generate_or_load_knowledge_from_repo()

    if repo_information is not None:
        return init_system_prompt + repo_information, "Analysis completed"
    else:
        return init_system_prompt, "Analysis failed"

