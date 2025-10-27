import streamlit as st
from src.utils import setup_open_source_components, load_index, query_index, create_index_if_missing

def main():
    try:
        # Configure global settings with open-source LLM and embeddings
        setup_open_source_components()

        # Create index if missing
        created_index = create_index_if_missing()
        if created_index:
            index = created_index
        else:
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
                        response = query_index(
                            index,
                            f"Write a report on the outlook for {symbol} stock from the years 2023-2027. "
                            f"Be sure to include potential risks and headwinds based on the indexed articles."
                        )
                        st.write(response.response)
                    except Exception as e:
                        st.error(f"Error generating report: {e}")

        elif report_type == "Competitor Analysis":
            col1, col2 = st.columns(2)
            with col1:
                symbol1 = st.text_input("Stock Symbol 1 (e.g., AAPL)")
            with col2:
                symbol2 = st.text_input("Stock Symbol 2 (e.g., MSFT)")
            if symbol1 and symbol2:
                with st.spinner(f"Generating report for {symbol1} vs. {symbol2}..."):
                    try:
                        response = query_index(
                            index,
                            f"Write a report on the competition between {symbol1} stock and {symbol2} stock "
                            f"based on the indexed articles."
                        )
                        st.write(response.response)
                    except Exception as e:
                        st.error(f"Error generating report: {e}")

    except FileNotFoundError as e:
        st.error(str(e))
    except Exception as e:
        st.error(f"Application error: {e}")

if __name__ == "__main__":
    main()