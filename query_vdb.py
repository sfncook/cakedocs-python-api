import pinecone
from langchain.vectorstores import FAISS, Pinecone

def get_contexts_from_pinecone(query):


def query_vdb(query, pinecone_api_key, pinecone_environment, pinecone_index_name):
    print("Querying VDB...")
    pinecone.init(api_key=pinecone_api_key, environment=pinecone_environment)
    matched_docs = Pinecone.similarity_search(query, k=10)
    output = ""
    for idx, docs in enumerate(matched_docs):
        output += f"Context {idx}:\n"
        output += str(docs)
        output += "\n\n"
    return output