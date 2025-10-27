import os
from dotenv import load_dotenv
from llama_index.core import VectorStoreIndex, StorageContext, load_index_from_storage, Settings
from llama_index.llms.openrouter import OpenRouter
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
import streamlit as st
from pathlib import Path

# Load environment variables
load_dotenv()

def setup_openrouter_llm():
    """Set up OpenRouter LLM with an open-source model."""
    api_key = os.getenv("OPENROUTER_API_KEY")
    if not api_key:
        raise ValueError("OPENROUTER_API_KEY not found in .env file")
    llm = OpenRouter(
        api_key=api_key,
        model="mistralai/mixtral-8x7b-instruct",
        max_tokens=2048,  # Reasonable for Mixtral; adjust as needed
        context_window=32768,  # Mixtral's context window
    )
    return llm

def setup_huggingface_embeddings():
    """Set up open-source embeddings using HuggingFace."""
    embed_model = HuggingFaceEmbedding(
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    )
    return embed_model

def load_index(persist_dir: str = "storage"):
    """Load the vector index from storage."""
    persist_path = Path(persist_dir)
    if not persist_path.exists():
        raise FileNotFoundError(f"Index storage directory '{persist_dir}' does not exist. Run 02_index_news.py first.")
    try:
        storage_context = StorageContext.from_defaults(persist_dir=persist_dir)
        index = load_index_from_storage(storage_context)
        print(f"Index loaded from '{persist_dir}'")
        return index
    except Exception as e:
        raise Exception(f"Error loading index: {e}")

def main():
    try:
        # Configure global settings with open-source LLM and embeddings
        Settings.llm = setup_openrouter_llm()
        Settings.embed_model = setup_huggingface_embeddings()

        # Load the index
        index = load_index(persist_dir="storage")
        query_engine = index.as_query_engine()

        # Streamlit UI
        st.title("Financial Stock Analysis using LlamaIndex")

        st.header("Reports:")
        report_type = st.selectbox(
            "What type of report do you want?",
            ("Single Stock Outlook", "Competitor Analysis")
        )

        if report_type == "Single Stock Outlook":
            symbol = st.text_input("Stock Symbol (e.g., AAPL)")
            if symbol:
                with st.spinner(f"Generating report for {symbol}..."):
                    try:
                        response = query_engine.query(
                            f"Write a report on the outlook for {symbol} stock from the years 2023-2027. Be sure to include potential risks and headwinds. "
                            f"Include potential risks and headwinds based on the indexed articles."
                        )
                        st.write(response.response)  # Access the response text
                    except Exception as e:
                        st.error(f"Error generating report: {e}")

        if report_type == "Competitor Analysis":
            symbol1 = st.text_input("Stock Symbol 1 (e.g., AAPL)")
            symbol2 = st.text_input("Stock Symbol 2 (e.g., MSFT)")
            if symbol1 and symbol2:
                with st.spinner(f"Generating report for {symbol1} vs. {symbol2}..."):
                    try:
                        response = query_engine.query(
                            f"  Write a report on the competition between {symbol1} stock and {symbol2} stock."
                            f"based on the indexed articles."
                        )
                        st.write(response.response)  # Access the response text
                    except Exception as e:
                        st.error(f"Error generating report: {e}")

    except Exception as e:
        st.error(f"Application error: {e}")

if __name__ == "__main__":
    main()