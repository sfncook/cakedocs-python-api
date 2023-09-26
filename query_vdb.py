import pinecone
from langchain.vectorstores import FAISS, Pinecone
from langchain.embeddings.openai import OpenAIEmbeddings

def query_vdb_for_context_docs(query, pinecone_index_name, repo_url):
    print("Querying VDB...")
    repo_name = repo_url.split('/')[-1]
    embeddings = OpenAIEmbeddings(disallowed_special=())
    pinecone_index = pinecone.Index(pinecone_index_name)
    pinecone_vdb = Pinecone(pinecone_index, embeddings.embed_query, repo_name)
    context_docs = pinecone_vdb.similarity_search(query)
    return context_docs
