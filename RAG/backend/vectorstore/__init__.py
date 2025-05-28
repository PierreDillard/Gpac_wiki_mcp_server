from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_qdrant import Qdrant
from config.config import QDRANT_URL, QDRANT_API_KEY, COLLECTION_NAME

def init_vectorstore(
    chunks,
    embedding_model_name,
    collection_name=COLLECTION_NAME,
    qdrant_url=QDRANT_URL,
    qdrant_api_key=QDRANT_API_KEY,
):
    """Vectorizes and stores the chunks in Qdrant, then returns the store ready for search."""
    embedder = HuggingFaceEmbeddings(model_name=embedding_model_name)
    store = Qdrant.from_documents(
        documents=chunks,
        embedding=embedder,
        url=qdrant_url,
        api_key=qdrant_api_key,
        collection_name=collection_name,
        prefer_grpc=False  
    )
    print(f"[Vectorstore] {len(chunks)} chunks indexed in '{collection_name}'")
    return store
