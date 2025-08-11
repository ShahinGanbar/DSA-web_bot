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

    def __init__(self):
        if not os.getenv("GOOGLE_API_KEY"):
            raise ValueError("GOOGLE_API_KEY not found in environment variables")
            
        llm = GoogleGenerativeAI(
            model="gemini-1.5-flash",
            google_api_key=os.getenv("GOOGLE_API_KEY")
        )

        prompt = PromptTemplate.from_template(
            "You are a helpful data scientist. Given this data preview:\n\n{data_preview}\n\n"
            "and the user wants to: {user_request}\n\n"
            "Write Python code to analyze the data accordingly. Output only the code because it will be sent to the interpreter to run directly.Make sure that your generated code will work when it will run when the user copy and paste it to interpreter.Don't write 'python [your generated code]'.Just write the code"
        )

        self._chain = LLMChain(llm=llm, prompt=prompt)