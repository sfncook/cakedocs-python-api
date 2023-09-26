import os
from clone_repo import clone_repo
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.document_loaders import TextLoader, PyPDFLoader
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores import FAISS, Pinecone
import pickle
import pinecone

def get_file_chunks(filename):
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1500,
        chunk_overlap=200,
        length_function=len,
    )
    if filename.endswith(".pdf"):
        loader = PyPDFLoader(filename)
    else:
        loader = TextLoader(filename)
    documents = loader.load()
    chunks = text_splitter.split_documents(documents)
    print(f"Split {filename} into {len(chunks)} chunks")
    return chunks

def get_dir_chunks_recursively(dir_path):
    count = 0
    ignore_list = ['.git', 'node_modules', '__pycache__', '.idea', '.vscode', '.package-lock.json', 'yarn.lock']
    chunks = []
    for root, dirs, files in os.walk(dir_path):
        if count > 1:
            continue
        dirs[:] = [d for d in dirs if d not in ignore_list]  # modify dirs in-place
        for file in files:
            if file in ignore_list:
                continue
            print(f"Processing file {file}")
            filepath = os.path.join(root, file)
            try:
                chunks.extend(get_file_chunks(filepath))
            except Exception as e:
                print(f"Failed to process {filepath} due to error: {str(e)}")
    return chunks

def create_vdb_from_chunks(chunks, vdb_path):
    embedding = OpenAIEmbeddings(disallowed_special=())
    if os.path.exists(vdb_path):
        print(f"Deleting previous version of '{vdb_path}'")
        os.remove(vdb_path)
    print(f"Creating VDB {vdb_path}...")
    faiss_store = FAISS.from_documents(chunks, embedding=embedding)
    print(f"faiss_store: {faiss_store}")
    with open(vdb_path, "wb") as f:
        pickle.dump(faiss_store, f)
    return faiss_store



def store_chunks_in_pinecone(chunks, pinecone_index_name):
#     Delete does not work with "start-up" index
#     print("Deleting previous Pinecone index")
#     index = pinecone.Index(pinecone_index_name)
#     index.delete(delete_all=True)
#     print("Delete complete")

    print("Storing chunks in Pinecone...")
    embeddings = OpenAIEmbeddings(disallowed_special=())
    docsearch = Pinecone.from_documents(chunks, embeddings, index_name=pinecone_index)
    print("Done storing chunks in Pinecone!")

def create_vdb(repo_url, code_repo_path, vdb_path):
    PINECONE_API_KEY = os.environ.get("PINECONE_API_KEY", "PINECONE_API_KEY_NOT_SET")
    PINECONE_ENVIRONMENT = os.environ.get("PINECONE_ENVIRONMENT", "PINECONE_ENVIRONMENT_NOT_SET")
    PINECONE_INDEX = os.environ.get("PINECONE_INDEX", "PINECONE_INDEX")
    pinecone.init(api_key=PINECONE_API_KEY, environment=PINECONE_ENVIRONMENT)

#     repo_name = clone_repo(repo_url, code_repo_path)

    chunks = get_dir_chunks_recursively(code_repo_path)

#     create_vdb_from_chunks(chunks, vdb_path)
#     store_chunks_in_pinecone(chunks, PINECONE_INDEX)

    print("VDB generated!")
    return True
