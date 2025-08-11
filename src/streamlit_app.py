import streamlit as st
import pandas as pd
from llm.chain import LLMChainManager
from utils.data_utils import load_data, df_head_to_text, execute_code_safely

st.title("Your Data Analyst 🤖")

uploaded = st.file_uploader("Upload your CSV dataset", type="csv")

if uploaded:
    try:
        df = load_data(uploaded)
        st.subheader("📊 Data Preview")
        st.dataframe(df.head())

        # Add text input for user's analysis request
        user_request = st.text_input(
            "What would you like to analyze in this dataset?",
            placeholder="e.g., Show the correlation between columns, Create a scatter plot, etc."
        )

        if st.button("🔍 Ask Gemini to Analyze") and user_request:  # Only proceed if there's a request
            chain = LLMChainManager.get_chain()
            data_preview = df_head_to_text(df)
            
            response = chain.run({
                "data_preview": data_preview,
                "user_request": user_request  # Use the user's input instead of hardcoded request
            })

            st.subheader("💬 Gemini's Suggested Code")
            st.code(response, language='python')

            try:
                df = execute_code_safely(response, df)
            except Exception as e:
                st.error("Code Execution Error")
                st.exception(e)
                
    except Exception as e:
        st.error("Data Loading Error")
        st.exception(e)