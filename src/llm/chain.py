from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain_google_genai import GoogleGenerativeAI
import os
from dotenv import load_dotenv

load_dotenv()

class LLMChainManager:
    _instance = None
    _chain = None

    @classmethod
    def get_chain(cls):
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance._chain

    def __init__(self):  # Fix: Properly indent __init__ method
        if not os.getenv("GOOGLE_API_KEY"):
            raise ValueError("GOOGLE_API_KEY not found in environment variables")
            
        llm = GoogleGenerativeAI(
            model="gemini-1.5-flash",
            google_api_key=os.getenv("GOOGLE_API_KEY")
        )

        prompt = PromptTemplate.from_template(
            "You are a helpful data scientist. Use the existing DataFrame 'df' that is already loaded. "
            "Given this data preview:\n\n{data_preview}\n\n"
            "The user wants to: {user_request}\n\n"
            "Write Python code to perform this operation on the existing 'df'. "
            "Only output the code needed for the specific operation. "
            "Do not create new example data or a new DataFrame."
        )

        self._chain = LLMChain(llm=llm, prompt=prompt)