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
    ignore_list = ['.git', 'node_modules', '__pycache__', '.idea', '.vscode', 'package-lock.json', 'yarn.lock']
    chunks = []
    for root, dirs, files in os.walk(dir_path):
        # Just for testing/debugging
        if count > 1:
            continue
        count += 1

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

def create_vdb_from_chunks(chunks, temp_dir, repo_name):
    print("Creating VDB from chunks...")
    vdb_path = temp_dir + "/vdb-" + repo_name + ".pkl"
    embedding = OpenAIEmbeddings(disallowed_special=())
    if os.path.exists(vdb_path):
        print(f"Deleting previous version of '{vdb_path}'")
        os.remove(vdb_path)
    print(f"Creating VDB {vdb_path}...")
    faiss_store = FAISS.from_documents(chunks, embedding=embedding)
    print(f"faiss_store: {faiss_store}")
    with open(vdb_path, "wb") as f:
        pickle.dump(faiss_store, f)
    print("Done creating VDB from chunks!")
    return faiss_store



def store_chunks_in_pinecone(chunks, pinecone_index_name, repo_name):
    print("Storing chunks in Pinecone...")
    embeddings = OpenAIEmbeddings(disallowed_special=())
    pinecone_index = pinecone.Index(pinecone_index_name)
    pinecone_vdb = Pinecone(pinecone_index, embeddings.embed_query, repo_name)
    pinecone_vdb.add_documents(chunks)
#     docsearch = Pinecone.from_documents(chunks, embeddings, index_name=pinecone_index_name)
    print("Done storing chunks in Pinecone!")

def create_vdb(repo_url, code_repo_path, temp_dir, pinecone_index_name):
    repo_name = repo_url.split('/')[-1]

    clone_repo(repo_url, code_repo_path)

    chunks = get_dir_chunks_recursively(code_repo_path)

    # Pick one:
#     create_vdb_from_chunks(chunks, temp_dir, repo_name)
    store_chunks_in_pinecone(chunks, pinecone_index_name, repo_name)

    print("VDB generated!")
    return True
