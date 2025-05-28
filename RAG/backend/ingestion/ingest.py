import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parent.parent))

from splitters.splitter import split_chunks
from vectorstore import init_vectorstore
from config.config import EMBEDDING_MODEL_NAME, COLLECTION_NAME, CHUNK_SIZE, CHUNK_OVERLAP
from pathlib import Path
from langchain_community.document_loaders import TextLoader
from config.config import DOCS_DIR, EXCLUDE_DIRS, EXCLUDE_FILES

def is_valid(path: Path) -> bool:
    """Check if a path should be included in ingestion."""
    if path.name in EXCLUDE_FILES:
        return False
    if any(part in EXCLUDE_DIRS for part in path.parts):
        return False
    return True

def load_markdown_chunks() -> list:
    """Loads and filters markdown documents from DOCS_DIR."""
    md_paths = [p for p in Path(DOCS_DIR).rglob("*.md") if is_valid(p)]
    docs = []
    for p in md_paths:
        try:
            loader = TextLoader(str(p), encoding="utf-8")
            loaded_docs = loader.load()
            for doc in loaded_docs:
                doc.metadata.setdefault("source", str(p))
                doc.metadata.setdefault("filename", p.name)
                docs.append(doc)
        except Exception as e:
            print(f"[Ingest] Error loading {p}: {e}")
    return docs

def ingest_and_index():
    """
    Loads, splits, and indexes all markdown files into the vector database.
    Returns the vectorstore ready for search.
    """
    docs = load_markdown_chunks()
    print(f"[Ingest] {len(docs)} markdown documents loaded.")
    chunks = split_chunks(docs, chunk_size=CHUNK_SIZE, chunk_overlap=CHUNK_OVERLAP)
    print(f"[Split] {len(chunks)} chunks generated.")
    store = init_vectorstore(
        chunks,
        embedding_model_name=EMBEDDING_MODEL_NAME,
        collection_name=COLLECTION_NAME
    )
    print(f"[Vectorstore] {len(chunks)} chunks indexed in Qdrant.")
    return store

if __name__ == "__main__":
    ingest_and_index()
