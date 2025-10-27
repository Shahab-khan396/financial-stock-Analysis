import os
from dotenv import load_dotenv
from llama_index.core import VectorStoreIndex, SimpleDirectoryReader, Settings
from llama_index.llms.openrouter import OpenRouter
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from pathlib import Path

# Load environment variables
load_dotenv()

def setup_openrouter_llm():
    """Set up OpenRouter LLM with an open-source model."""
    api_key = os.getenv("OPENROUTER_API_KEY")
    if not api_key:
        raise ValueError("OPENROUTER_API_KEY not found in .env file")
    # Use open-source Mixtral model (swap as needed, e.g., "meta-llama/llama-3.1-8b-instruct")
    llm = OpenRouter(
        api_key=api_key,
        model="mistralai/mixtral-8x7b-instruct",
        max_tokens=256,
        context_window=4096,
    )
    print("OpenRouter LLM configured with open-source model")
    return llm

def setup_huggingface_embeddings():
    """Set up open-source embeddings using HuggingFace."""
    embed_model = HuggingFaceEmbedding(
        model_name="sentence-transformers/all-MiniLM-L6-v2"  # Lightweight open-source embedder
    )
    print("HuggingFace embeddings configured")
    return embed_model

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

def create_and_save_index(documents: list, persist_dir: str = "storage"):
    """Create and persist a vector index from documents using open-source components."""
    try:
        # Global settings for LlamaIndex (uses open-source LLM and embeddings)
        Settings.llm = setup_openrouter_llm()
        Settings.embed_model = setup_huggingface_embeddings()
        
        # Create VectorStoreIndex
        index = VectorStoreIndex.from_documents(documents)
        print("Index created successfully with open-source LLM and embeddings")
        
        # Ensure persist directory exists
        Path(persist_dir).mkdir(exist_ok=True)
        
        # Persist the index
        index.storage_context.persist(persist_dir=persist_dir)
        print(f"Index saved to '{persist_dir}'")
        return index
    except Exception as e:
        raise Exception(f"Error creating or saving index: {e}")

def main():
    try:
        # Load documents from 'articles' directory
        documents = load_documents("articles")
        
        # Create and save index
        create_and_save_index(documents, persist_dir="storage")
        
    except Exception as e:
        print(f"Error: {e}")
        exit(1)

if __name__ == "__main__":
    main()