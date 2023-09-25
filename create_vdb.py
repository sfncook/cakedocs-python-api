import os
from clone_repo import clone_repo
from langchain.text_splitter import RecursiveCharacterTextSplitter, CharacterTextSplitter
from langchain.document_loaders import TextLoader, PyPDFLoader
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores import FAISS, SupabaseVectorStore
import pickle

TEMP_DIR = os.environ.get("TEMP_DIR", "/Users/shawncook/Projects/CakeDocsAi/pythonEnv_3.8/tmp")

def tokenize_chunks(filenames):
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1500,
        chunk_overlap=200,
        length_function=len,
    )
    chunks = []
    for filename in filenames:
        if filename.endswith(".pdf"):
            loader = PyPDFLoader(filename)
        else:
            loader = TextLoader(filename)
        documents = loader.load()
        splits = text_splitter.split_documents(documents)
        chunks.extend(splits)
        print(f"Split {filename} into {len(splits)} chunks")
    return chunks

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
                knowledge["known_docs"].extend(tokenize_chunks([filepath]))
            except Exception as e:
                print(f"Failed to process {filepath} due to error: {str(e)}")
    return knowledge

def local_vdb(knowledge, vdb_path=None):
    embedding = OpenAIEmbeddings(disallowed_special=())
    print("Embedding documents...")
    faiss_store = FAISS.from_documents(knowledge["known_docs"], embedding=embedding)
    if vdb_path is not None:
        with open(vdb_path, "wb") as f:
            pickle.dump(faiss_store, f)
    return faiss_store

def get_repo_names(dir_path):
    folder_names = [name for name in os.listdir(dir_path) if os.path.isdir(os.path.join(dir_path, name))]
    concatenated_names = "-".join(folder_names)
    return concatenated_names

def generate_or_load_knowledge_from_repo(code_repo_path):
    vdb_path = TEMP_DIR + "/vdb-" + get_repo_names(code_repo_path) + ".pkl"
    ignore_list = ['.git', 'node_modules', '__pycache__', '.idea', '.vscode']
    knowledge = generate_knowledge_from_repo(code_repo_path, ignore_list)
    vdb = local_vdb(knowledge, vdb_path=vdb_path)
    print("VDB generated!")
    return vdb_path

def create_vdb(repo_url):
    code_repo_path = TEMP_DIR + "/code_repo"
    repo_information = clone_repo(repo_url, code_repo_path)
    vdb_path = generate_or_load_knowledge_from_repo(code_repo_path)
    return vdb_path
