import streamlit as st
import pandas as pd
from src.llm.chain import LLMChainManager
from src.utils.data_utils import load_data, df_head_to_text, execute_code_safely

# Page configuration
st.set_page_config(page_title="Data Analysis Assistant", page_icon="🤖")
st.title("Interactive Data Analysis Assistant 🤖")

# Initialize session state
if 'df' not in st.session_state:
    st.session_state.df = None
    st.session_state.chat_history = []

# File upload section
uploaded = st.file_uploader("Upload your CSV dataset", type="csv")

if uploaded:
    try:
        # Load data if new upload
        if st.session_state.df is None:
            st.session_state.df = load_data(uploaded)
            st.session_state.chat_history = []
            
        df = st.session_state.df
        
        # Display current data preview
        st.subheader("📊 Current Data Preview")
        st.dataframe(df.head())

        # Display chat history
        if st.session_state.chat_history:
            st.subheader("💬 Analysis History")
            for i, (query, code) in enumerate(st.session_state.chat_history, 1):
                with st.expander(f"Operation {i}: {query}"):
                    st.code(code, language='python')

        # User input section
        user_request = st.text_input(
            "What analysis would you like to perform?",
            placeholder="e.g., 'drop the target column', 'show correlation matrix', etc."
        )

        # Process request
        if st.button("🔍 Generate Analysis") and user_request:
            with st.spinner("Generating analysis..."):
                try:
                    # Get LLM response
                    chain = LLMChainManager.get_chain()
                    data_preview = df_head_to_text(df)
                    response = chain.run({
                        "data_preview": data_preview,
                        "user_request": user_request
                    })

                    # Update history
                    st.session_state.chat_history.append((user_request, response))

                    # Show generated code
                    st.subheader("💻 Generated Code")
                    st.code(response, language='python')

                    # Execute code
                    st.session_state.df = execute_code_safely(response, df)

                except Exception as e:
                    st.error("❌ Error")
                    st.exception(e)
                
    except Exception as e:
        st.error("❌ Data Loading Error")
        st.exception(e)

# Reset session button
if st.session_state.df is not None:
    if st.button("🔄 Reset Session"):
        st.session_state.df = None
        st.session_state.chat_history = []
        st.experimental_rerun()