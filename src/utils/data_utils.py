import pandas as pd
import sys
import re
import subprocess
from io import StringIO
import importlib
import streamlit as st
from typing import Union, Any
from pydantic import BaseModel


def load_data(file_path: Union[str, Any]) -> pd.DataFrame:
    """Load data from CSV file or file-like object"""
    return pd.read_csv(file_path)


def df_head_to_text(df: pd.DataFrame, rows: int = 3) -> str:
    """Convert dataframe head to string format"""
    return df.head(rows).to_string()


def df_schema_to_text(df: pd.DataFrame) -> str:
    """Summarize dataframe columns and dtypes for LLM context."""
    lines = ["Columns (name: dtype, non_null_count):"]
    non_null_counts = df.notnull().sum()
    for col in df.columns:
        lines.append(f"- {col}: {df.dtypes[col]}, {int(non_null_counts[col])} non-null")
    return "\n".join(lines)


def execute_code_safely(response: BaseModel, df: pd.DataFrame) -> pd.DataFrame:
    """
    Execute generated code or display explanation based on response type with auto-package installation
    Args:
        response: LLM response with response_type and content
        df: Input DataFrame
    Returns:
        Modified or original DataFrame
    """
    if response.response_type == "explanation":
        st.subheader("💡 Answer")
        st.write(response.content)
        return df

    if response.response_type == "code":
        code = response.content.replace('```python', '').replace('```', '').strip()
        
        # Initialize execution environment
        exec_globals = {
            'pd': pd,
            'df': df,
            'print': print,
            'importlib': importlib,
            'file_path': getattr(st.session_state, 'file_path', None)
        }
        
        # Handle imports with auto-installation
        if 'import' in code:
            import_lines = [line for line in code.split('\n') if 'import' in line]
            if import_lines:
                import_code = '\n'.join(import_lines)
                try:
                    exec(import_code, exec_globals)
                except ImportError as e:
                    # Find and install missing package
                    match = re.search(r"No module named '([^']+)'", str(e))
                    if match:
                        missing_module = match.group(1).split('.')[0]
                        st.info(f"📦 Installing missing package: {missing_module}")
                        try:
                            subprocess.check_call([sys.executable, "-m", "pip", "install", missing_module])
                            exec(import_code, exec_globals)
                        except subprocess.CalledProcessError as e:
                            raise Exception(f"Failed to install {missing_module}: {str(e)}")
                    else:
                        raise
                
                # Remove import lines from main code
                code = '\n'.join(line for line in code.split('\n') if 'import' not in line)
        
        # Setup output capture
        output = StringIO()
        old_stdout = sys.stdout
        sys.stdout = output
        
        try:
            # Execute the main code
            exec(code, exec_globals)
            
            # Handle output
            printed_output = output.getvalue()
            sys.stdout = old_stdout

            if printed_output.strip():
                st.subheader("📋 Code Output")
                st.text(printed_output)

            # Try to render plots if any were created
            plotted = False
            # Plotly figures
            fig = exec_globals.get('fig')
            if fig is not None and hasattr(fig, 'to_plotly_json'):
                try:
                    st.subheader("📈 Plot")
                    st.plotly_chart(fig, use_container_width=True)
                    plotted = True
                except Exception:
                    pass
            # Matplotlib/seaborn figures
            plt = exec_globals.get('plt')
            if not plotted and plt is not None:
                try:
                    st.subheader("📈 Plot")
                    st.pyplot(plt.gcf(), clear_figure=True)
                    plotted = True
                except Exception:
                    pass
            # Matplotlib via axes handle
            if not plotted and 'ax' in exec_globals:
                ax = exec_globals.get('ax')
                try:
                    fig_obj = getattr(ax, 'figure', None)
                    if fig_obj is not None:
                        st.subheader("📈 Plot")
                        st.pyplot(fig_obj, clear_figure=True)
                        plotted = True
                except Exception:
                    pass
            
            # Display results
            modified_df = exec_globals.get('df', df)
            st.subheader("📊 Current Data State")
            st.dataframe(modified_df)
            
            return modified_df
            
        except Exception as e:
            sys.stdout = old_stdout
            raise Exception(f"Error executing code: {str(e)}")
            
        finally:
            sys.stdout = old_stdout
    
    return df