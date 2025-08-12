from src.utils.data_utils import df_head_to_text
import pandas as pd


df = pd.read_csv("iris.csv")

text = df_head_to_text(df)


print(text)