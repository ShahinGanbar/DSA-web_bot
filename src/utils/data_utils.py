import pandas as pd

def load_data(file_path):
    """Load data from CSV file or file-like object"""
    return pd.read_csv(file_path)

def df_head_to_text(df, rows=3):
    """Convert dataframe head to string format"""
    return df.head(rows).to_string()

import re
import importlib

def execute_code_safely(code, df):
    """Execute generated code in a safe environment with automatic module imports"""
    import streamlit as st
    
    # Clean up code by removing markdown code block syntax
    code = code.replace('```python', '').replace('```', '')
    code = code.strip()
    
    # Initialize execution environment
    exec_globals = {'pd': pd, 'df': df, 'st': st}
    
    # Define safe modules that can be automatically imported
    SAFE_MODULES = {
        'numpy': 'np',
        'matplotlib.pyplot': 'plt',
        'seaborn': 'sns',
        'scipy': 'scipy',
        'sklearn': 'sklearn'
    }
    
    # Detect module usage in code
    for module_name, alias in SAFE_MODULES.items():
        if alias in code or module_name in code:
            try:
                module = importlib.import_module(module_name)
                exec_globals[alias] = module
            except ImportError as e:
                print(f"Warning: Could not import {module_name}: {str(e)}")
    
    try:
        # Execute the cleaned code
        exec(code, exec_globals)
        
        # Handle plot display for Streamlit
        if 'plt' in exec_globals:
            st.pyplot(exec_globals['plt'].gcf())
            exec_globals['plt'].close()
            
    except Exception as e:
        raise Exception(f"Error executing code: {str(e)}")
    
    return exec_globals.get('df', df)