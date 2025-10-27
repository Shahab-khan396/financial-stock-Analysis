import os
from dotenv import load_dotenv
from llama_index.core import StorageContext, load_index_from_storage, Settings, SimpleDirectoryReader, VectorStoreIndex
from llama_index.llms.openrouter import OpenRouter
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from pathlib import Path

# Load environment variables
load_dotenv()

def setup_open_source_components():
    """Configure global settings with open-source LLM and embeddings."""
    api_key = os.getenv("OPENROUTER_API_KEY")
    if not api_key:
        raise ValueError("OPENROUTER_API_KEY not found in .env file! Get it from https://openrouter.ai/keys")
    
    Settings.llm = OpenRouter(
        api_key=api_key,
        model="mistralai/mixtral-8x7b-instruct",
        max_tokens=256,
        context_window=4096,
    )
    
    
    
def setup_huggingface_embeddings():
    """Set up open-source embeddings using HuggingFace."""
    embed_model = HuggingFaceEmbedding(
        model_name="sentence-transformers/all-MiniLM-L6-v2"  # Lightweight open-source embedder
    )
    print("HuggingFace embeddings configured")
    return embed_model

Settings.embed_model = setup_huggingface_embeddings()

def load_documents(directory: str) -> list:
    """Load documents from the specified directory."""
    directory_path = Path(directory)
    if not directory_path.is_dir():
        raise FileNotFoundError(f"Directory '{directory}' does not exist")
    try:
        documents = SimpleDirectoryReader(directory).load_data()
        if not documents:
            raise ValueError(f"No valid files found in '{directory}'")
        print(f"Loaded {len(documents)} documents from '{directory}'")
        return documents
    except Exception as e:
        raise Exception(f"Error loading documents: {e}")

def load_index(persist_dir: str = "storage"):
    """Load the saved index from the specified persist directory."""
    storage_context = StorageContext.from_defaults(persist_dir=persist_dir)
    try:
        index = load_index_from_storage(storage_context)
        print(f"Index loaded from {persist_dir}/")
        return index
    except FileNotFoundError:
        raise FileNotFoundError(
            f"Index files (e.g., docstore.json) not found in '{persist_dir}'. "
            f"Attempting to create index..."
        )
    except Exception as e:
        raise Exception(f"Error loading index: {e}")

def create_and_save_index(documents: list, persist_dir: str = "storage"):
    """Create and persist a vector index from documents."""
    try:
        # Ensure persist directory exists
        Path(persist_dir).mkdir(exist_ok=True)
        index = VectorStoreIndex.from_documents(documents)
        print("Index created successfully with open-source LLM and embeddings")
        index.storage_context.persist(persist_dir=persist_dir)
        print(f"Index saved to '{persist_dir}'")
        return index
    except Exception as e:
        raise Exception(f"Error creating or saving index: {e}")

def create_index_if_missing(directory: str = "articles", persist_dir: str = "storage"):
    """Create and save a new index if it doesn't exist in the persist directory."""
    storage_path = Path(persist_dir)
    if not storage_path.exists() or not any(storage_path.iterdir()):
        print(f"No index found in '{persist_dir}'. Creating a new one...")
        documents = load_documents(directory)
        return create_and_save_index(documents, persist_dir)
    return None

def query_index(index, query_text: str):
    """Query the index and return the response."""
    query_engine = index.as_query_engine()
    response = query_engine.query(query_text)
    return response