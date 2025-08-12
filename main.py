from src.llm.chain import LLMChainManager, AnalysisResponse
from src.utils.data_utils import load_data, df_head_to_text, df_schema_to_text, execute_code_safely
from typing import Any
from pydantic import ValidationError
import json


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
        # Try to parse as JSON first
        parsed = json.loads(text)
        return AnalysisResponse(**parsed)
    except (json.JSONDecodeError, ValidationError):
        # Fallback – treat as plain explanation
        return AnalysisResponse(response_type="explanation", content=str(raw_response))


def main():
    try:
        # Load data
        df = load_data("elebele.csv")
        data_preview = df_head_to_text(df)
        data_schema = df_schema_to_text(df)
        file_path = "elebele.csv"
        print("Data Preview:\n", data_preview)

        # Get chain and generate analysis
        chain = LLMChainManager.get_chain()
        raw_response = chain.run({
            "data_preview": data_preview,
            "user_request": "Analyze this dataset and provide insights",
            "file_path": file_path,
            "data_schema": data_schema
        })

        # Parse the response
        response = _parse_llm_response(raw_response)
        print("\nGenerated Code:\n", response.content)

        # Execute generated code
        df = execute_code_safely(response, df)
        
    except Exception as e:
        print(f"Error: {str(e)}")

if __name__ == "__main__":
    main()