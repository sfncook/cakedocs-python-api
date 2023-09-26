import pinecone
from langchain.vectorstores import FAISS, Pinecone

def get_contexts_from_pinecone(query):


def query_vdb(query):
    print("Querying VDB...")
    matched_docs = Pinecone.similarity_search(query, k=10)
    output = ""
    for idx, docs in enumerate(matched_docs):
        output += f"Context {idx}:\n"
        output += str(docs)
        output += "\n\n"
    return output