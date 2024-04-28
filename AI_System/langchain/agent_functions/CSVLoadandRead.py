from langchain_community.document_loaders.csv_loader import CSVLoader
from langchain.pydantic_v1 import BaseModel, Field
from langchain.tools import tool



class load_csv_paramaters(BaseModel):
    file_path: str = Field(description="The path to the csv file that should be loaded")
@tool("load_csv", args_schema=load_csv_paramaters)
def load_csv(file_path: str) -> dict:
    """
    A function for loading a csv file
    """
    loader = CSVLoader(file_path)
    loaded_csv = loader.load()
    return loaded_csv


