import pandas as pd
from langchain.pydantic_v1 import BaseModel, Field
from langchain.tools import tool

"""
SUPER HELPFUL DOCUMENTATION
https://python.langchain.com/docs/modules/tools/custom_tools/
"""

datapath: str = "data.csv"
class get_csv_line_paramaters(BaseModel):
    row: int = Field(description="Should be the row you want to access from the CSV-file. The rows are zero indexed")

# Return direct makes the chatbot only reply with the return value of the function
@tool("get-row-from-csv", args_schema=get_csv_line_paramaters, return_direct=False)
def get_csv_line(row: int) -> str:
    """A function for retrevieng a row from a csv-file as a string with marked data"""

    dataframe = pd.read_csv(datapath, nrows=int(row) + 1)
    data = dataframe.iloc[int(row)]
    data_string = ','.join(f"{col}: {val}" for col, val in data.items())

    return data_string

if __name__ == "__main__":
    print(get_csv_line.name)
    print(get_csv_line.description)
    print(get_csv_line.args)