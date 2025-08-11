import pandas as pd
import sys
from io import StringIO
import importlib
import streamlit as st

def load_data(file_path):
    """Load data from CSV file or file-like object"""
    return pd.read_csv(file_path)

def df_head_to_text(df, rows=3):
    """Convert dataframe head to string format"""
    return df.head(rows).to_string()

def execute_code_safely(code, df):
    """Execute generated code in a safe environment with automatic module imports"""
    import streamlit as st
    
    # Clean up code
    code = code.replace('```python', '').replace('```', '').strip()
    
    # Initialize execution environment with necessary imports
    exec_globals = {
        'pd': pd, 
        'df': df,
        'np': importlib.import_module('numpy'),
        'plt': importlib.import_module('matplotlib.pyplot'),
        'sns': importlib.import_module('seaborn'),
        'print': print  # Explicitly include print function
    }
    
    # Setup output capture
    output = StringIO()
    old_stdout = sys.stdout
    sys.stdout = output
    
    try:
        # Execute the code
        exec(code, exec_globals)
        
        # Get the output and reset stdout
        printed_output = output.getvalue()
        sys.stdout = old_stdout
        
        # Display outputs in Streamlit
        if printed_output and printed_output.strip():
            st.subheader("📋 Code Output")
            st.text(printed_output)
        
        # Get and display modified DataFrame
        modified_df = exec_globals.get('df', df)
        
        # Display current DataFrame state
        st.subheader("📊 Current Data State")
        st.dataframe(modified_df)
        
        return modified_df
        
    except Exception as e:
        sys.stdout = old_stdout
        raise Exception(f"Error executing code: {str(e)}")
        
    finally:
        sys.stdout = old_stdout