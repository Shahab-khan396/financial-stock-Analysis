import os
from dotenv import load_dotenv
from llama_index.core import StorageContext, load_index_from_storage, Settings
from llama_index.llms.openrouter import OpenRouter
from llama_index.embeddings.huggingface import HuggingFaceEmbedding

load_dotenv()

# Reuse the same open-source setup
Settings.llm = OpenRouter(api_key=os.getenv("OPENROUTER_API_KEY"), model="mistralai/mixtral-8x7b-instruct")
Settings.embed_model = HuggingFaceEmbedding(model_name="sentence-transformers/all-MiniLM-L6-v2")

# Load the saved index
storage_context = StorageContext.from_defaults(persist_dir="storage")
index = load_index_from_storage(storage_context)

# Query example (financial/stock themed)
query_engine = index.as_query_engine()
response = query_engine.query("What are the key trends in financial stocks mentioned in the articles?")
print(response)