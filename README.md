Repository Description
Financial Stock Analysis with LlamaIndex
This project is a powerful financial stock analysis tool built using LlamaIndex, an advanced framework for building context-augmented applications with large language models (LLMs). Leveraging open-source components like OpenRouter's mistralai/mixtral-8x7b-instruct LLM and HuggingFace's sentence-transformers/all-MiniLM-L6-v2 embeddings, it enables users to generate insightful reports on stock outlooks and competitor analyses based on indexed financial news articles.
Features

Single Stock Outlook: Generate detailed reports on a stock's potential risks, headwinds, and outlook (2023-2027) using indexed data.
Competitor Analysis: Compare two stocks (e.g., AAPL vs. MSFT) based on competitive trends and insights from articles.
Dynamic UI: Interactive Streamlit interface for easy report generation and input.
Automated Indexing: Automatically creates and loads a vector index from a directory of articles if none exists.
Modular Design: Reusable utility functions for LLM setup, document loading, and querying, housed in src/utils.py.

Tech Stack

LlamaIndex: For indexing and querying documents with vector search.
OpenRouter: Provides access to the Mixtral 8x7B Instruct model.
HuggingFace Embeddings: Uses all-MiniLM-L6-v2 for efficient text embeddings.
Streamlit: Powers the interactive web application.
Python: Core language with dependencies managed via Conda.

Getting Started

Clone the Repository:
bashgit clone <https://github.com/your-username/financial-stock-Analysis.git>
cd financial-stock-Analysis

Set Up Environment:

Create a Conda environment:
bashconda create -n myenv python=3.9
conda activate myenv

Install dependencies:
bashpip install -r requirements.txt

Configure API Key:

Obtain an API key from OpenRouter.
Create a .env file in the project root with:
textOPENROUTER_API_KEY=your_api_key_here

Prepare Data:

Place financial news articles (e.g., .txt, .pdf) in the articles/ directory.

Run the Application:
bashstreamlit run app.py

Access the app in your browser (default: <http://localhost:8501>).

Project Structure

src/: Contains utility scripts and modules.

utils.py: Core functions for LLM setup, indexing, and querying.
02_index_news.py: Indexes documents from articles/.
03_query_news.py: Example script for querying the index.

app.py: Main Streamlit application.
articles/: Directory for input documents.
storage/: Persisted index files (auto-generated).
requirements.txt: Dependency list.
