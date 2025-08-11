from src.llm.chain import LLMChainManager
from src.utils.data_utils import load_data, df_head_to_text, execute_code_safely

def main():
    try:
        # Load data
        df = load_data("data/your_data.csv")
        data_preview = df_head_to_text(df)
        print("Data Preview:\n", data_preview)

        # Get chain and generate analysis
        chain = LLMChainManager.get_chain()
        response = chain.run({
            "data_preview": data_preview,
            "user_request": "Analyze this dataset and provide insights"
        })

        print("\nGenerated Code:\n", response)

        # Execute generated code
        df = execute_code_safely(response, df)
        
    except Exception as e:
        print(f"Error: {str(e)}")

if __name__ == "__main__":
    main()