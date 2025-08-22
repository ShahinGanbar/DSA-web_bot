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
    """Load data from various file formats (CSV, Excel, JSON, etc.)"""
    try:
        # Handle file-like objects (Streamlit uploads)
        if hasattr(file_path, 'name'):
            file_extension = file_path.name.lower().split('.')[-1]
        else:
            # Handle string paths
            file_extension = str(file_path).lower().split('.')[-1]
        
        # Load based on file extension
        if file_extension == 'csv':
            return pd.read_csv(file_path)
        elif file_extension in ['xlsx', 'xls']:
            return pd.read_excel(file_path)
        elif file_extension == 'json':
            return pd.read_json(file_path)
        elif file_extension == 'parquet':
            return pd.read_parquet(file_path)
        elif file_extension == 'pickle':
            return pd.read_pickle(file_path)
        elif file_extension == 'feather':
            return pd.read_feather(file_path)
        elif file_extension == 'h5' or file_extension == 'hdf5':
            return pd.read_hdf(file_path)
        else:
            # Try to infer format
            try:
                return pd.read_csv(file_path)
            except Exception:
                try:
                    return pd.read_excel(file_path)
                except Exception:
                    raise ValueError(f"Unsupported file format: {file_extension}. Supported formats: CSV, Excel (xlsx/xls), JSON, Parquet, Pickle, Feather, HDF5")
    except Exception as e:
        raise Exception(f"Error loading file: {str(e)}")


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


def execute_code_safely(response: BaseModel, df: pd.DataFrame) -> tuple[pd.DataFrame, dict]:
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
        return df, {}

    if response.response_type == "code":
        code = response.content.replace('```python', '').replace('```', '').strip()
        

        
        # Initialize execution environment
        exec_globals = {
            'pd': pd,
            'df': df,
            'print': print,
            'importlib': importlib
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

        # Prevent external windows/tabs by stripping explicit show() calls (e.g., fig.show(), plt.show())
        # and Plotly offline calls that auto-open a browser tab
        # This keeps all plots rendered via Streamlit components only
        code = re.sub(r'(?m)^\s*.*\.show\s*\([^)]*\)\s*;?\s*$', '', code)
        code = re.sub(r'(?m)^\s*plotly\.(?:offline|io)\.(?:plot|show)\s*\([^)]*\)\s*;?\s*$', '', code)
        code = re.sub(r'(?m)^\s*pio\.show\s*\([^)]*\)\s*;?\s*$', '', code)
        code = re.sub(r'(?m)^\s*.*write_html\s*\([^)]*auto_open\s*=\s*True[^)]*\)\s*;?\s*$', '', code)
        
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

            # Try to render plots (all of them) if any were created
            displayed_any_plot = False
            plotly_figs = []
            fig_nums = []  # Initialize matplotlib figure numbers

            # Collect Plotly figures present in the global namespace
            for value in list(exec_globals.values()):
                try:
                    if hasattr(value, 'to_plotly_json'):
                        plotly_figs.append(value)
                    elif isinstance(value, (list, tuple)):
                        for item in value:
                            if hasattr(item, 'to_plotly_json'):
                                plotly_figs.append(item)
                except Exception:
                    pass

            # Deduplicate while preserving order
            seen_ids = set()
            unique_plotly_figs = []
            for f in plotly_figs:
                if id(f) not in seen_ids:
                    unique_plotly_figs.append(f)
                    seen_ids.add(id(f))

            if unique_plotly_figs:
                st.subheader("📈 Plots")
                for f in unique_plotly_figs:
                    try:
                        st.plotly_chart(f, use_container_width=True)
                        displayed_any_plot = True
                    except Exception:
                        pass

            # Matplotlib/seaborn figures (render all open figures)
            plt = exec_globals.get('plt')
            if plt is not None:
                try:
                    fig_nums = plt.get_fignums()
                except Exception:
                    fig_nums = []
                if fig_nums:
                    if not displayed_any_plot:
                        st.subheader("📈 Plots")
                    for num in fig_nums:
                        try:
                            fig_obj = plt.figure(num)
                            st.pyplot(fig_obj, clear_figure=False)
                            displayed_any_plot = True
                        except Exception:
                            pass

            # Matplotlib via axes handle (if any)
            if 'ax' in exec_globals:
                ax = exec_globals.get('ax')
                try:
                    fig_obj = getattr(ax, 'figure', None)
                    if fig_obj is not None:
                        if not displayed_any_plot:
                            st.subheader("📈 Plots")
                        st.pyplot(fig_obj, clear_figure=False)
                        displayed_any_plot = True
                except Exception:
                    pass
            
            # Display results
            modified_df = exec_globals.get('df', df)
            st.subheader("📊 Current Data State")
            st.dataframe(modified_df)
            
            # Prepare execution results for LLM context (not for response mixing)
            # Ensure all variables are defined before using them
            plots_created = len(unique_plotly_figs) + len(fig_nums) + (1 if 'ax' in exec_globals else 0)
            
            # Enhanced data change detection
            data_changes = []
            if df.shape != modified_df.shape:
                data_changes.append(f"Shape changed from {df.shape} to {modified_df.shape}")
            
            # Check for column changes
            original_cols = set(df.columns)
            new_cols = set(modified_df.columns)
            if original_cols != new_cols:
                added = new_cols - original_cols
                removed = original_cols - new_cols
                if added:
                    data_changes.append(f"Added columns: {list(added)}")
                if removed:
                    data_changes.append(f"Removed columns: {list(removed)}")
            
            # Check for data type changes
            type_changes = []
            for col in df.columns.intersection(modified_df.columns):
                if df[col].dtype != modified_df[col].dtype:
                    type_changes.append(f"{col}: {df[col].dtype} → {modified_df[col].dtype}")
            
            if type_changes:
                data_changes.append(f"Type changes: {', '.join(type_changes)}")
            
            # Check for filtering/row changes
            if len(df) != len(modified_df):
                data_changes.append(f"Row count changed from {len(df)} to {len(modified_df)}")
            
            execution_results = {
                'code': code,
                'output': printed_output.strip(),
                'data_changes': '; '.join(data_changes) if data_changes else "No structural changes detected",
                'plots_created': plots_created
            }
            
            return modified_df, execution_results
            

        except Exception as e:
            sys.stdout = old_stdout
            raise Exception(f"Error executing code: {str(e)}")
            
        finally:
            sys.stdout = old_stdout
    
    return df, {}