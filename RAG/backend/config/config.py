import os
from dotenv import load_dotenv
from pathlib import Path

load_dotenv()
BASE_DIR = Path(__file__).parent.parent.resolve()
# Source directory
DOCS_DIR = str(BASE_DIR / "docs")
MKDOCS_YML = str(BASE_DIR / "mkdocs.yml")
# Exclude
EXCLUDE_FILES = {  "index.md", "tags.md", "check_spaell.sh","aspell_dict_gpac.txt"}
EXCLUDE_DIRS = {"images", "javascripts", "__pycache__"}

# --- Optional: Configuration for ingest.py ---
# Qdrant Configuration
QDRANT_URL = "http://localhost:6333"  # Or your Qdrant cloud URL/local setup
QDRANT_API_KEY = os.getenv("QDRANT_API_KEY")  
COLLECTION_NAME = "gpac_docs"

# Embedding Model Configuration
# Using a lightweight, effective model suitable for general text
# See https://huggingface.co/spaces/mteb/leaderboard for options
EMBEDDING_MODEL_NAME = "all-MiniLM-L6-v2"

# Text Splitting Configuration
CHUNK_SIZE = 1000
CHUNK_OVERLAP = 200