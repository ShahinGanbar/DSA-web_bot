from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain_google_genai import GoogleGenerativeAI
from langchain.chat_models import ChatOpenAI
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
        if not os.getenv("OPENAI_API_KEY"):
            raise ValueError("OPENAI_API_KEY not found in environment variables")
            
        # llm = GoogleGenerativeAI(
        #     model="gemini-2.5-flash",
        #     google_api_key=os.getenv("GOOGLE_API_KEY")
        # )
        llm = ChatOpenAI(
            model_name="gpt-4o-mini",  # <-- choose your OpenAI model
            temperature=0.7,
            openai_api_key=os.getenv("OPENAI_API_KEY")  
        )

        parser = PydanticOutputParser(pydantic_object=AnalysisResponse)

        prompt = PromptTemplate(
            template="""You are a helpful data scientist working strictly with the user's uploaded dataset.
            File name: {file_path}
            Data preview:\n\n{data_preview}\n\n
            Schema summary:\n{data_schema}\n\n
            Conversation history:\n{conversation_history}\n\n
            User request: {user_request}\n\n
            Decision policy:
            - If the request asks a conceptual or descriptive question about the data (e.g., definitions, observations, interpretations) and does not require computation, return an explanation.
            - If the request requires computations, data transformations, statistics, or plots, return Python code.
            - If the request is ambiguous, ask a brief clarifying question in an explanation.
            
            Conversation Context:
            - Always consider the conversation history when interpreting the current request
            - If the user is clarifying a previous request, build upon that context
            - Don't treat each request as completely independent - maintain continuity
            - If a previous request was incomplete, use the current request to complete it
            - Look for pronouns and references (e.g., "it", "that column", "now") that refer to previous context
            - If user says "it's the 'price' column", understand they're answering your previous question
            
            Examples:
            - "Drop the target column" → Generate code (df = df.drop('target', axis=1))
            - "Which column should I drop?" → Generate explanation asking for column name
            - "It's the 'price' column" → Generate code to drop 'price' column (understanding the context)
            - "Now show me the correlation matrix" → Generate code for correlation (knowing 'price' was dropped)

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
            input_variables=["data_preview", "user_request", "file_path", "data_schema", "conversation_history"],
            partial_variables={"format_instructions": parser.get_format_instructions()}
        )

        self._chain = LLMChain(llm=llm, prompt=prompt)
    @classmethod
    def get_chain(cls):
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance._chain

    @staticmethod
    def format_conversation_history(chat_history, max_exchanges=3):
        """Format conversation history for LLM context"""
        if not chat_history:
            return "No previous conversation."
        
        formatted = "Recent conversation:\n"
        # Get last N exchanges to maintain context without overwhelming the prompt
        recent_history = chat_history[-max_exchanges:]
        
        for i, (query, response) in enumerate(recent_history, 1):
            formatted += f"User {i}: {query}\n"
            if hasattr(response, 'response_type'):
                if response.response_type == "code":
                    formatted += f"Assistant {i}: Generated code to {query}\n"
                else:
                    formatted += f"Assistant {i}: {response.content}\n"
            else:
                formatted += f"Assistant {i}: {response}\n"
            formatted += "\n"
        
        return formatted