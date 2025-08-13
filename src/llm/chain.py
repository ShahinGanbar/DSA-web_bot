from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain_google_genai import GoogleGenerativeAI
from langchain.output_parsers import PydanticOutputParser
from pydantic import BaseModel, Field
from typing import Union
from dotenv import load_dotenv
import os


load_dotenv()

class AnalysisResponse(BaseModel):
    """Schema for LLM response"""
    response_type: str = Field(description="Either 'code' or 'explanation'")
    content: str = Field(description="The actual code or explanation text")

class LLMChainManager:
    _instance = None
    _chain = None

    def __init__(self):
        if not os.getenv("GOOGLE_API_KEY"):
            raise ValueError("GOOGLE_API_KEY not found in environment variables")
            
        llm = GoogleGenerativeAI(
            model="gemini-1.5-flash",
            google_api_key=os.getenv("GOOGLE_API_KEY")
        )

        parser = PydanticOutputParser(pydantic_object=AnalysisResponse)

        prompt = PromptTemplate(
            template="""You are a helpful data scientist working strictly with the user's uploaded dataset.
            File name: {file_path}
            Data preview:\n\n{data_preview}\n\n
            Schema summary:\n{data_schema}\n\n
            User request: {user_request}\n\n
            Decision policy:
            - If the request asks a conceptual or descriptive question about the data (e.g., definitions, observations, interpretations) and does not require computation, return an explanation.
            - If the request requires computations, data transformations, statistics, or plots, return Python code.
            - If the request is ambiguous, ask a brief clarifying question in an explanation.

            Code policy when generating code:
            - The DataFrame is already loaded as variable 'df' - DO NOT recreate it with pd.DataFrame() or pd.read_csv().
            - ABSOLUTELY NO FILE OPERATIONS: Never call pd.read_csv(), open(), Path(), to_csv(), savefig(), write_html(), or any filesystem/network I/O.
            - Keep the code concise, safe, and assign final results back to df if you modify the dataset.
            - For plots: create Plotly figures assigned to variables (e.g., fig, figs list) or use matplotlib/seaborn so Streamlit can render them.
            - DO NOT call fig.show(), plt.show(), plotly.offline.plot(), plotly.io.show(), pio.show(), or anything that opens a new tab/window.
            - For correlation/statistics: use df.select_dtypes(include='number') if you need numeric-only operations.
            - Always work with the existing 'df' variable, never create a new one.
            - All data must come from the in-memory 'df' variable.

            {format_instructions}
            """,
            input_variables=["data_preview", "user_request", "file_path", "data_schema"],
            partial_variables={"format_instructions": parser.get_format_instructions()}
        )

        self._chain = LLMChain(llm=llm, prompt=prompt)
    @classmethod
    def get_chain(cls):
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance._chain