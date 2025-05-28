#!/usr/bin/env python3
# uv: pyyaml


import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parent.parent))
from mcp.server.fastmcp import FastMCP
import yaml
from pathlib import Path
from ingestion.ingest import load_markdown_chunks
from splitters.splitter import split_chunks
from vectorstore import init_vectorstore
from config.config import DOCS_DIR, MKDOCS_YML, CHUNK_SIZE, CHUNK_OVERLAP, EMBEDDING_MODEL_NAME, COLLECTION_NAME

mcp = FastMCP("gpac-doc-mcp")

@mcp.tool()
def list_docs() -> list[str]:
    """
    Returns the list of Markdown file paths referenced in mkdocs.yml.
    Useful for navigating the GPAC documentation.
    """
    with open(MKDOCS_YML, encoding="utf-8") as f:
        nav = yaml.safe_load(f).get("nav", [])
    paths = []
    def walk_nav(items):
        for entry in items:
            if isinstance(entry, dict):
                for _, target in entry.items():
                    if isinstance(target, str):
                        paths.append(target)
                    else:
                        walk_nav(target)
    walk_nav(nav)
    return paths

@mcp.tool()
def get_doc(path: str) -> str:
    """
    Returns the raw content of a specified Markdown file (e.g., 'index.md').
    """
    p = Path(DOCS_DIR) / path
    return p.read_text(encoding="utf-8")

# RAG pipeline: ingestion + split + vectorstore (loaded at startup for performance)
docs = load_markdown_chunks()
chunks = split_chunks(docs, chunk_size=CHUNK_SIZE, chunk_overlap=CHUNK_OVERLAP)
store = init_vectorstore(chunks, embedding_model_name=EMBEDDING_MODEL_NAME, collection_name=COLLECTION_NAME)

@mcp.tool()
def search(query: str, top_k: int = 5) -> list[dict]:
    """
    Performs a semantic search in the GPAC documentation.

    Args:
        query (str): The search query (plain English).
        top_k (int): Number of top relevant chunks to return.

    Returns:
        List of dicts containing:
            - 'content': The text content of the chunk.
            - 'meta': Metadata (filename, position in doc, etc.).

    Example:
        search("How to use bsrw filter with tcsc=first")
    """
    hits = store.similarity_search(query, k=top_k)
    return [{"content": h.page_content, "meta": h.metadata} for h in hits]



if __name__ == "__main__":
    mcp.run()
