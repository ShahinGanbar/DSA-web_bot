import streamlit as st
import pandas as pd
import os
from llm.chain import LLMChainManager, AnalysisResponse
from utils.data_utils import load_data, df_head_to_text, execute_code_safely
from typing import Any
from pydantic import ValidationError


def initialize_session_state():
    """Initialize session state variables"""
    if 'df' not in st.session_state:
        st.session_state.df = None
        st.session_state.chat_history = []
        st.session_state.file_path = None
        st.session_state.execution_history = []


def reset_session():
    """Reset all session state variables"""
    st.session_state.df = None
    st.session_state.chat_history = []
    st.session_state.file_path = None
    st.session_state.execution_history = []
    st.experimental_rerun()


def _parse_llm_response(raw_response: Any) -> AnalysisResponse:
    """Parse LLM raw output into AnalysisResponse; fallback to explanation if parsing fails."""
    if isinstance(raw_response, AnalysisResponse):
        return raw_response
    if isinstance(raw_response, dict):
        return AnalysisResponse(**raw_response)

    text = str(raw_response).strip()

    # Strip optional code fences
    if text.startswith("```") and text.endswith("```"):
        text = text.strip("`")
        # Remove leading language tag if present (e.g., json)
        if text.startswith("json\n"):
            text = text[len("json\n"):]

    try:
        # Pydantic v2
        return AnalysisResponse.model_validate_json(text)  # type: ignore[attr-defined]
    except (ValidationError, AttributeError):
        try:
            # Pydantic v1
            return AnalysisResponse.parse_raw(text)  # type: ignore[attr-defined]
        except Exception:
            # Fallback – treat as plain explanation
            return AnalysisResponse(response_type="explanation", content=str(raw_response))


def process_user_request(user_request: str, df: pd.DataFrame):
    """Process user request and return LLM response"""
    chain = LLMChainManager.get_chain()
    data_preview = df_head_to_text(df)
    # Lazy import to avoid circular
    from utils.data_utils import df_schema_to_text
    data_schema = df_schema_to_text(df)
    
    # Format conversation history for LLM context
    conversation_history = LLMChainManager.format_conversation_history(st.session_state.chat_history)
    
    raw = chain.run({
        "data_preview": data_preview,
        "user_request": user_request,
        "file_path": st.session_state.file_path,
        "data_schema": data_schema,
        "conversation_history": conversation_history,
    })
    return _parse_llm_response(raw)


def main():
    # Page configuration
    st.set_page_config(page_title="Data Science Academy Assistant", page_icon="🤖")
    st.title("Data Science Academy Assistant 🤖")

    # Initialize session state
    initialize_session_state()

    # File upload section
    uploaded = st.file_uploader("Upload your dataset", type=['csv', 'xlsx', 'xls', 'json', 'parquet', 'pickle', 'feather', 'h5', 'hdf5'])

    if uploaded:
        try:
            # Load data if new upload
            if st.session_state.df is None:
                st.session_state.df = load_data(uploaded)
                st.session_state.chat_history = []
                st.session_state.file_path = uploaded.name  # Store file path in session state
                # No file saving - everything stays in memory
            
            df = st.session_state.df
            
            # Display current data preview
            st.subheader("📊 Current Data Preview")
            st.write(f"File: {st.session_state.file_path}")
            st.dataframe(df.head())
            
            # Display execution history
            if st.session_state.execution_history:
                st.subheader("🔧 Previous Operations")
                for i, result in enumerate(st.session_state.execution_history, 1):
                    with st.expander(f"Operation {i}: {result['code'][:50]}..."):
                        st.write(f"**Code:** {result['code']}")
                        if result['output']:
                            st.write(f"**Output:** {result['output']}")
                        if result['data_changes']:
                            st.write(f"**Data Changes:** {result['data_changes']}")
                        if result['plots_created'] > 0:
                            st.write(f"**Plots Created:** {result['plots_created']}")

            # Display chat history
            if st.session_state.chat_history:
                st.subheader("💬 Analysis History")
                for i, (query, response) in enumerate(st.session_state.chat_history, 1):
                    with st.expander(f"Operation {i}: {query}"):
                        # Be tolerant to legacy string responses
                        if isinstance(response, str):
                            st.write(response)
                        else:
                            if response.response_type == "code":
                                st.code(response.content, language='python')
                            else:
                                st.write(response.content)

            # User input section
            user_request = st.text_input(
                "Ask a question or request an analysis",
                placeholder="e.g., 'What's the average value?', 'show correlation matrix'"
            )

            # Process request
            if st.button("🔍 Analyze") and user_request:
                with st.spinner("Processing request..."):
                    try:
                        # Get and process LLM response
                        response = process_user_request(user_request, df)

                        # Update chat history
                        st.session_state.chat_history.append((user_request, response))

                        # Handle response based on type
                        if response.response_type == "code":
                            st.subheader("💻 Generated Code")
                            st.code(response.content, language='python')
                            # Execute code and get results
                            modified_df, execution_results = execute_code_safely(response, df)
                            st.session_state.df = modified_df
                            
                            # Store execution results for LLM context
                            if execution_results:
                                st.session_state.execution_history.append(execution_results)
                        else:
                            # Display explanation
                            st.subheader("💡 Answer")
                            st.write(response.content)

                    except Exception as e:
                        st.error("❌ Error")
                        st.exception(e)
                    
        except Exception as e:
            st.error("❌ Data Loading Error")
            st.exception(e)

    # Reset session button
    if st.session_state.df is not None:
        if st.button("🔄 Reset Session"):
            reset_session()

if __name__ == "__main__":
    main()