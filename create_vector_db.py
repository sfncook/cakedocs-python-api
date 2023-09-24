import os
import json
from langchain.text_splitter import RecursiveCharacterTextSplitter, CharacterTextSplitter
from langchain.document_loaders import TextLoader, PyPDFLoader
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores import FAISS, SupabaseVectorStore
import pickle
import subprocess

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

def analyze_repo(repo_url):
    repo_information = clone_repo(repo_url)
    generate_or_load_knowledge_from_repo()

    if repo_information is not None:
        return init_system_prompt + repo_information, "Analysis completed"
    else:
        return init_system_prompt, "Analysis failed"

